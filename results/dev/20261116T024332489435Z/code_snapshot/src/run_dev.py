"""Dev-only execution and post-run gold scoring. Test is deliberately unavailable."""
import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import statistics
import time
from .agent import run
from .provider import DeepSeek
from .retrieval import DenseRetriever, HybridRetriever, LexicalRetriever, load_day6
from starter.baseline import hit, pack_context, validate

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path, value, secret=''):
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(value, ensure_ascii=False, indent=2)+'\n'
    if secret:
        text = text.replace(secret, '[REDACTED]')
    temporary = path.with_suffix(path.suffix+'.tmp')
    temporary.write_text(text, encoding='utf-8')
    temporary.replace(path)


def validate_queries(queries):
    if not isinstance(queries, list) or not queries:
        raise ValueError('Missing query-only dev cases')
    ids = set()
    for q in queries:
        if set(q) != {'id', 'split', 'question'} or q['split'] != 'dev':
            raise ValueError('Runner accepts only query-only dev records')
        if not isinstance(q['id'], str) or q['id'] in ids or not isinstance(q['question'], str) or not q['question'].strip():
            raise ValueError('Invalid query ID/text')
        ids.add(q['id'])


def fraction(n, total):
    return {'n': n, 'N': total, 'rate': n/total if total else None}


def summarize(cases, traces):
    by_id = {t['query_id']: t for t in traces}
    if set(by_id) != {q['id'] for q in cases} or len(by_id) != len(traces):
        raise ValueError('Missing or duplicate traces')
    yes = [q for q in cases if q['answerable']]
    original1 = original3 = raw_context_hit = context_hit = first1 = first3 = any_search_hit = 0
    misses = []
    for q in yes:
        t = by_id[q['id']]
        raw = t['original_results']
        original1 += bool(raw and hit(raw[0], q['gold']))
        original3 += any(hit(c, q['gold']) for c in raw[:3])
        raw_context, raw_ids = pack_context(raw, t.get('budget_chars', 800))
        raw_context_hit += any(c['id'] in raw_ids and hit(c, q['gold']) for c in raw)
        searches = [e for e in t['events'] if e['event'] == 'search' and 'results' in e]
        first = searches[0]['results'] if searches else []
        first1 += bool(first and hit(first[0], q['gold']))
        first3 += any(hit(c, q['gold']) for c in first[:3])
        any_search_hit += any(hit(c, q['gold']) for e in searches for c in e['results'])
        all_results = [c for e in searches for c in e['results']]
        found = (t['status'] != 'error' and any(c['id'] in t['context_ids'] and hit(c, q['gold'])
                 and any(g['evidence'] in t['context'] for g in q['gold']
                         if c['source_id'] == g['source_id'] and c['page'] == g['page']) for c in all_results))
        context_hit += found
        if not found:
            misses.append(q['id'])
    successes = [t for t in traces if t['status'] != 'error']
    records = [call for t in traces for call in t['model_calls']]
    usage = Counter()
    for call in records:
        for key in ('prompt_tokens', 'completion_tokens', 'total_tokens', 'prompt_cache_hit_tokens', 'prompt_cache_miss_tokens'):
            usage[key] += call.get('usage', {}).get(key, 0)
    cache_hit = usage['prompt_cache_hit_tokens']
    cache_miss = max(0, usage['prompt_tokens']-cache_hit)
    cost_base = (cache_hit*0.003 + cache_miss*0.15 + usage['completion_tokens']*0.6)/1_000_000
    return {
        'cases': len(cases), 'answerable': len(yes), 'statuses': dict(Counter(t['status'] for t in traces)),
        'original_query': {'hit1': fraction(original1,len(yes)), 'hit3': fraction(original3,len(yes)),
                           'context_evidence': fraction(raw_context_hit,len(yes))},
        'agent_first_search': {'hit1': fraction(first1,len(yes)), 'hit3': fraction(first3,len(yes))},
        'agent_any_search_evidence': fraction(any_search_hit,len(yes)),
        'final_context_evidence': fraction(context_hit,len(yes)), 'final_context_miss_ids': misses,
        'tool_use': fraction(sum(any(e['event']=='search' for e in t['events']) for t in successes),len(successes)),
        'search_call_distribution': dict(Counter(str(sum(e['event']=='search' for e in t['events'])) for t in traces)),
        'errors': [{'id':t['query_id'],'stage':t.get('error_stage'),'type':t.get('error_type')} for t in traces if t['status']=='error'],
        'median_agent_seconds': statistics.median(t['elapsed_seconds'] for t in traces),
        'model_requests_including_retries': len(records), 'known_usage': dict(usage),
        'failed_requests_without_usage': sum(c.get('status')=='error' and not c.get('usage') for c in records),
        'estimated_api_cost_usd_range': [cost_base, cost_base*2],
        'cost_note': 'Estimate using published Flash off-peak/peak prices: cache-hit input 0.003/0.006, other input 0.15/0.30, output 0.60/1.20 USD per million. Actual billing may differ. Local embedding/retrieval API cost is zero.',
        'semantic_quality': None, 'review_status': 'pending; grounded answer/citation support/abstention correctness require reading outputs',
        'denominator_policy': 'All answerable cases stay in retrieval denominator, failures count as misses. Tool use excludes and separately reports failed cases.',
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--day6', type=Path, default=ROOT.parent/'K5-L3B-DAY06-PhamHoangHuy-2A202603836-DataIngestion')
    parser.add_argument('--methods', nargs='+', choices=('dense','tfidf','hybrid'), default=['dense','tfidf','hybrid'])
    parser.add_argument('--resume', type=Path, help='Resume missing cases only if code/config/input hashes match')
    args = parser.parse_args()
    benchmark = read(ROOT/'benchmark/manifest.json')
    if benchmark.get('status') != 'approved_frozen_before_dev':
        raise ValueError('Benchmark needs user-approved frozen status')
    query_path = ROOT/'benchmark/queries/dev.json'
    if digest(query_path) != benchmark['files_sha256']['queries/dev.json'] or digest(ROOT/'data/day6/chunks.json') != benchmark['corpus_sha256']:
        raise ValueError('Frozen query/corpus changed')
    if digest(ROOT/'benchmark/dev.json') != benchmark['files_sha256']['dev.json']:
        raise ValueError('Frozen dev labels changed')
    queries = read(query_path)
    validate_queries(queries)
    if len(queries) != 17 or len(set(args.methods)) != len(args.methods):
        raise ValueError('Expected 17 queries and unique methods')
    chunks = read(ROOT/'data/day6/chunks.json')
    from dotenv import dotenv_values
    settings = dotenv_values(ROOT/'.env')
    provider = DeepSeek(settings)
    config = {'split':'dev','methods':args.methods,'top_k':3,'max_searches':3,'budget_chars':800,
              'model':provider.model,'thinking':'disabled','temperature':0,'max_output_tokens':640,
              'rrf_k':60,'hybrid_candidate_depth':20,'index_strategy':'C','filters':None,
              'query_sha256':digest(query_path),'corpus_sha256':benchmark['corpus_sha256'],
              'dev_labels_sha256':benchmark['files_sha256']['dev.json'],
              'index_sha256':benchmark['index_sha256'],
              'code_sha256':{p.relative_to(ROOT).as_posix():digest(p) for p in sorted((ROOT/'src').glob('*.py'))}}
    if args.resume:
        output = args.resume.resolve()
        manifest = read(output/'manifest.json')
        if manifest['config'] != config:
            raise ValueError('Cannot resume changed code/config/inputs')
    else:
        output = ROOT/'results/dev'/datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
        output.mkdir(parents=True, exist_ok=False)
        manifest = {'status':'started','started_at_utc':datetime.now(timezone.utc).isoformat(),'config':config,
                    'test_evaluated':False,'benchmark_approval':benchmark.get('user_confirmation'),
                    'latency_note':'Model loading excluded. Query embeddings cached within each dense adapter; hybrid has its own cache. All timings are actual observed warm/local timings, not a controlled hardware benchmark.'}
        write(output/'manifest.json', manifest)
    print('Run directory: '+str(output), flush=True)
    init_start = time.perf_counter()
    dense = load_day6(args.day6, benchmark['index_sha256'])
    lexical = LexicalRetriever(chunks)
    retrievers = {'dense':dense,'tfidf':lexical,'hybrid':HybridRetriever(DenseRetriever(dense.store,dense.embedder),lexical)}
    manifest['last_initialization_seconds'] = time.perf_counter()-init_start
    write(output/'manifest.json',manifest)
    for method in args.methods:
        directory = output/method
        for q in queries:
            target = directory/(q['id']+'.json')
            if target.exists():
                continue
            begin = time.perf_counter()
            try:
                original = retrievers[method].search(q['question'], filters=None, top_k=3)
            except Exception as exc:
                # Pre-agent store failures do not become an apparently successful refusal.
                trace = {'status':'error','error_stage':'original_retrieval','error_type':type(exc).__name__,
                         'answer':'','citations':[],'events':[],'context':'','context_ids':[],
                         'model_calls':[],'elapsed_seconds':time.perf_counter()-begin,'budget_chars':800}
                original = []
            else:
                original_seconds = time.perf_counter()-begin
                trace = run(q['question'],provider,retrievers[method],budget=800,top_k=3,max_searches=3)
                trace['original_retrieval_seconds'] = original_seconds
            trace.update(query_id=q['id'],split='dev',question=q['question'],method=method,original_results=original)
            write(target,trace,provider.key)
            print(f"{method} {q['id']}: {trace['status']} ({len(trace['model_calls'])} requests)",flush=True)
    # Execution above sees query-only data. Gold is loaded only now for deterministic scoring.
    cases = read(ROOT/'benchmark/dev.json')
    if [{k:q[k] for k in ('id','split','question')} for q in cases] != queries:
        raise ValueError('Query/gold alignment mismatch')
    validate(chunks,[q for q in cases if q['answerable']])
    summaries = {}
    for method in args.methods:
        traces = [read(output/method/(q['id']+'.json')) for q in queries]
        summaries[method] = summarize(cases,traces)
        write(output/method/'traces.json',traces,provider.key)
        write(output/method/'summary.json',summaries[method])
        reviews = [{'query_id':q['id'],'answer_grade':None,'context_grade':None,
                    'citation_support':[None for _ in t['citations']], 'abstention_correct':None,
                    'reason':'','review_origin':'pending'} for q,t in zip(cases,traces)]
        if not (output/method/'reviews.json').exists():
            write(output/method/'reviews.json',reviews)
    write(output/'summary.json',summaries)
    manifest.update(status='complete',completed_at_utc=datetime.now(timezone.utc).isoformat(),
                    trace_count=len(queries)*len(args.methods),semantic_review='pending')
    write(output/'manifest.json',manifest)
    (output.parent/'LATEST.txt').write_text(output.name+'\n',encoding='utf-8')
    print(json.dumps(summaries,ensure_ascii=False,indent=2),flush=True)


if __name__=='__main__':main()
