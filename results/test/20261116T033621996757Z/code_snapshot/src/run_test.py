"""One registered held-out run: frozen baseline and selected I1, never tune here."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import time
import uuid
from .agent import run
from .provider import DeepSeek
from .retrieval import DenseRetriever, load_day6
from .run_dev import ROOT, read, write, digest, runtime_hashes, snapshot_runtime, summarize
from starter.baseline import validate


def validate_test_queries(queries):
    if not isinstance(queries, list) or len(queries) != 7:
        raise ValueError('Expected exactly seven held-out queries')
    if {q.get('id') for q in queries} != {f'T{i:02d}' for i in range(1,8)}:
        raise ValueError('Unexpected held-out IDs')
    for q in queries:
        if set(q) != {'id','split','question'} or q['split'] != 'test':
            raise ValueError('Test execution accepts query-only records')
        if not isinstance(q['question'], str) or not q['question'].strip():
            raise ValueError('Empty query')


def verify_frozen_runtime(frozen, actual):
    for name, sha in frozen.items():
        if actual.get(name) != sha:
            raise ValueError('Approved runtime changed: '+name)


def check_protocol(provider):
    """Two consecutive real tool cycles within four attempts, no benchmark data."""
    tools=[{'type':'function','function':{'name':'connection_probe','description':'Return a local connection test marker.',
           'parameters':{'type':'object','properties':{},'required':[],'additionalProperties':False}}}]
    start=len(provider.records)
    results=[]
    consecutive=0
    for attempt in range(4):
        marker='PROBE_'+uuid.uuid4().hex[:12]
        messages=[{'role':'system','content':'Call connection_probe once, then reply with exactly its marker, no other text. This is a protocol probe, not retrieval.'},
                  {'role':'user','content':'Run the connection probe.'}]
        entry={'attempt':attempt+1}
        try:
            message=provider.complete(messages,tools,{'type':'function','function':{'name':'connection_probe'}})
            calls=message.get('tool_calls') or []
            if len(calls)!=1 or calls[0]['function']['name']!='connection_probe' or json.loads(calls[0]['function']['arguments'])!={}:
                raise ValueError('Invalid probe tool call')
            messages.append({'role':'assistant','content':message.get('content'),'tool_calls':calls})
            messages.append({'role':'tool','tool_call_id':calls[0]['id'],'content':json.dumps({'marker':marker})})
            final=provider.complete(messages,tools,'none')
            ok=(final.get('content') or '').strip()==marker
            entry['ok']=ok
            consecutive=consecutive+1 if ok else 0
        except Exception as exc:
            entry.update(ok=False,error_type=type(exc).__name__,http_status=getattr(exc,'status',None))
            consecutive=0
        results.append(entry)
        print(f"Protocol probe {attempt+1}: {entry['ok']}",flush=True)
        if consecutive==2:
            break
    return {'ok':consecutive==2,'attempts':results,'model_calls':provider.records[start:],
            'scope':'Connection probes only; no held-out data or gold'}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--day6',type=Path,default=ROOT.parent/'K5-L3B-DAY06-PhamHoangHuy-2A202603836-DataIngestion')
    parser.add_argument('--resume',type=Path,help='Only fill missing cases in the registered run; never replace errors')
    args=parser.parse_args()
    approved_path=ROOT/'configs/selected_for_test.json'
    approved=read(approved_path)
    if approved.get('status')!='approved_frozen_for_test' or approved.get('test_authorized') is not True:
        raise ValueError('Missing user approval')
    for name, field in (('configs/dev_review_approval.json','dev_review_approval_sha256'),
                        ('configs/dev_selected_candidate.json','source_candidate_sha256'),
                        ('benchmark/manifest.json','benchmark_manifest_sha256')):
        if digest(ROOT/name)!=approved[field]:
            raise ValueError('Approved provenance changed: '+name)
    current_hashes=runtime_hashes(args.day6)
    verify_frozen_runtime(approved['candidate']['config']['code_sha256'],current_hashes)
    if approved['runner_sha256']!=digest(Path(__file__)):
        raise ValueError('Runner changed after approval freeze')
    benchmark=read(ROOT/'benchmark/manifest.json')
    for name in ('queries/test.json','test.json'):
        if digest(ROOT/'benchmark'/name)!=benchmark['files_sha256'][name]:
            raise ValueError('Frozen test changed')
    if digest(ROOT/'data/day6/chunks.json')!=benchmark['corpus_sha256']:
        raise ValueError('Frozen corpus changed')
    expected={'method':'dense','model':'deepseek-flash','thinking':'disabled','budget_chars':2000,
              'context_policy':'arrival','top_k':3,'max_searches':3,'model_temperature':0}
    if any(approved['candidate'].get(k)!=v for k,v in expected.items()):
        raise ValueError('Selected configuration does not match approved I1')
    registry_path=ROOT/'results/test/registry.json'
    if args.resume:
        output=args.resume.resolve()
        if not output.is_relative_to(ROOT/'results/test') or not registry_path.exists():
            raise ValueError('Resume requires the registered test directory')
        if read(registry_path)['run_directory']!=str(output):
            raise ValueError('Different registered run')
        manifest=read(output/'manifest.json')
        if manifest['status']=='complete':
            raise ValueError('Test already complete; inspect existing results')
        if manifest['runtime_sha256']!=current_hashes or manifest['approval_sha256']!=digest(approved_path):
            raise ValueError('Resume inputs/runtime changed')
    else:
        if registry_path.exists():
            raise ValueError('A held-out run is already registered; only resume missing cases')
        output=ROOT/'results/test'/datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
        output.mkdir(parents=True,exist_ok=False)
        manifest={'status':'preflight','started_at_utc':datetime.now(timezone.utc).isoformat(),
                  'approval_sha256':digest(approved_path),'runtime_sha256':current_hashes,
                  'query_sha256':benchmark['files_sha256']['queries/test.json'],
                  'test_gold_sha256':benchmark['files_sha256']['test.json'],'corpus_sha256':benchmark['corpus_sha256'],
                  'index_sha256':benchmark['index_sha256'],
                  'configurations':{'baseline':{'method':'dense','budget_chars':800,'context_policy':'arrival'},
                                    'I1':{'method':'dense','budget_chars':2000,'context_policy':'arrival'}},
                  'top_k':3,'max_searches':3,'model':'deepseek-flash','thinking':'disabled','temperature':0,
                  'test_evaluated':False,'semantic_review':'pending','failed_cases_replaced':False}
        write(output/'manifest.json',manifest)
        snapshot_runtime(output,args.day6,current_hashes)
        write(output/'approval_snapshot.json',approved)
    from dotenv import dotenv_values
    provider=DeepSeek(dotenv_values(ROOT/'.env'))
    print('Test directory: '+str(output),flush=True)
    preflight=check_protocol(provider)
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    write(output/('preflight_'+stamp+'.json'),preflight,provider.key)
    if not preflight['ok']:
        manifest.update(status='preflight_failed')
        write(output/'manifest.json',manifest)
        print('Preflight failed; no additional held-out queries executed.',flush=True)
        return
    chunks=read(ROOT/'data/day6/chunks.json')
    dense=load_day6(args.day6,benchmark['index_sha256'])
    retrievers={'baseline':dense,'I1':DenseRetriever(dense.store,dense.embedder)}
    if not registry_path.exists():
        write(registry_path,{'run_directory':str(output),'registered_at_utc':datetime.now(timezone.utc).isoformat(),
                             'approval_sha256':digest(approved_path),'no_test_tuning':True})
    queries=read(ROOT/'benchmark/queries/test.json')
    validate_test_queries(queries)
    manifest.update(status='running',test_evaluated=True)
    write(output/'manifest.json',manifest)
    for label,config in manifest['configurations'].items():
        for q in queries:
            target=output/label/(q['id']+'.json')
            if target.exists():
                continue
            begin=time.perf_counter()
            try:
                original=retrievers[label].search(q['question'],filters=None,top_k=3)
            except Exception as exc:
                original=[]
                result={'status':'error','error_stage':'original_retrieval','error_type':type(exc).__name__,
                        'answer':'','citations':[],'events':[],'context':'','context_ids':[],
                        'context_chars':0,'budget_chars':config['budget_chars'],'context_policy':'arrival',
                        'model_calls':[],'elapsed_seconds':time.perf_counter()-begin}
            else:
                original_seconds=time.perf_counter()-begin
                result=run(q['question'],provider,retrievers[label],budget=config['budget_chars'],
                           context_policy=config['context_policy'],top_k=3,max_searches=3)
                result['original_retrieval_seconds']=original_seconds
            result.update(query_id=q['id'],split='test',question=q['question'],configuration=label,
                          method='dense',original_results=original)
            write(target,result,provider.key)
            print(f"{label} {q['id']}: {result['status']} ({len(result['model_calls'])} requests)",flush=True)
    # No gold is passed into the execution above. Label access starts after both runs.
    cases=read(ROOT/'benchmark/test.json')
    if [{k:q[k] for k in ('id','split','question')} for q in cases]!=queries:
        raise ValueError('Test query/gold alignment mismatch')
    validate(chunks,[q for q in cases if q['answerable']])
    summaries={}
    for label in manifest['configurations']:
        traces=[read(output/label/(q['id']+'.json')) for q in queries]
        summaries[label]=summarize(cases,traces)
        write(output/label/'traces.json',traces,provider.key)
        write(output/label/'summary.json',summaries[label])
        if not (output/label/'reviews.json').exists():
            write(output/label/'reviews.json',[{'query_id':q['id'],'answer_grade':None,'context_grade':None,
                  'citation_support':[None for _ in t['citations']],'abstention_correct':None,'reason':'',
                  'review_origin':'pending'} for q,t in zip(cases,traces)])
    write(output/'summary.json',summaries)
    manifest.update(status='complete',trace_count=14,completed_at_utc=datetime.now(timezone.utc).isoformat())
    write(output/'manifest.json',manifest)
    print(json.dumps(summaries,ensure_ascii=False,indent=2),flush=True)


if __name__=='__main__':main()
