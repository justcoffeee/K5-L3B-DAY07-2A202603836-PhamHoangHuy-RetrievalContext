"""Reproducible A/B/C runner. Default dev; heldout requires an explicit gate."""
import argparse
import csv
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import statistics
import time

from .chunking import fixed_size, by_paragraph
from .embeddings import MyEmbedder
from .evaluation import evaluate_query, summarize
from .ingestion import load_source_units
from .store import PgVectorStore

ROOT = Path(__file__).resolve().parents[2]


def json_write(path, value):
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')


def jsonl_read(path):
    return [json.loads(line) for line in path.read_text(encoding='utf-8').splitlines() if line.strip()]


def fingerprint_inputs():
    paths = [*sorted((ROOT/'starter/src').glob('*.py')), ROOT/'configs/strategies.json', ROOT/'requirements-lock.txt']
    protocol = json.loads((ROOT/'benchmark/manifest.json').read_text(encoding='utf-8'))
    for name, digest in protocol['files_sha256'].items():
        path = ROOT/name
        if hashlib.sha256(path.read_bytes()).hexdigest() != digest:
            raise ValueError('Frozen input was changed: ' + name)
        paths.append(path)
    return {p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}


def chunk_pages(pages, config):
    return [chunk for page in pages for chunk in
        (fixed_size(page,config['chunk_size'],config['overlap']) if config['chunking']=='fixed_size'
         else by_paragraph(page,config['chunk_size']))]


def export_coherence(output, pages, chunks_by_strategy):
    # Fixed positions spread across sorted units, chosen without gold/rankings.
    chosen = [pages[round(i*(len(pages)-1)/9)] for i in range(10)]
    rows = []
    for number,page in enumerate(chosen,1):
        position = len(page.text)//2
        while position < len(page.text)-1 and page.text[position].isspace():
            position += 1
        for strategy,chunks in chunks_by_strategy.items():
            matches = [c for c in chunks if c.document_id==page.document_id and c.page==page.page
                       and c.metadata['char_start']<=position<c.metadata['char_end']]
            chunk = min(matches,key=lambda c:(c.metadata['char_start'],c.chunk_id))
            rows.append({'sample_id':f'P{number:02d}','strategy':strategy,'document_id':page.document_id,
                'page':page.page,'source':page.source,'source_position':position,'chunk_id':chunk.chunk_id,
                'chunk_text':chunk.text,'label_0_2':'','reason':''})
    with (output/'coherence_audit.csv').open('w',encoding='utf-8',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=list(rows[0])); writer.writeheader(); writer.writerows(rows)


def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--split',choices=['dev','test'],default='dev')
    parser.add_argument('--confirm-heldout',action='store_true')
    parser.add_argument('--dev-run',type=Path)
    args=parser.parse_args()
    if args.split=='test' and (not args.confirm_heldout or args.dev_run is None):
        parser.error('Heldout is locked. After approval supply --confirm-heldout and --dev-run PATH; no test tuning.')
    from dotenv import dotenv_values
    settings=dotenv_values(ROOT/'.env')
    database=dotenv_values(ROOT/'starter/.env').get('DATABASE_URL')
    if not database:
        raise ValueError('Missing starter/.env DATABASE_URL')
    expected={'EMBEDDING_MODEL':'intfloat/multilingual-e5-small',
        'EMBEDDING_REVISION':'614241f622f53c4eeff9890bdc4f31cfecc418b3',
        'EMBEDDING_DIMENSIONS':'384','EMBEDDING_DEVICE':'cpu','EMBEDDING_MAX_TOKENS':'512',
        'EMBEDDING_QUERY_PREFIX':'query: ','EMBEDDING_DOCUMENT_PREFIX':'passage: ',
        'EMBEDDING_NORMALIZE':'true','VECTOR_STORE':'pgvector','VECTOR_DISTANCE':'cosine'}
    for name,value in expected.items():
        if settings.get(name)!=value:
            raise ValueError('Environment differs from approved configuration: '+name)
    inputs=fingerprint_inputs()
    configs=json.loads((ROOT/'configs/strategies.json').read_text(encoding='utf-8'))
    if {k:v for k,v in configs['B'].items() if k!='metadata_filter'} != {k:v for k,v in configs['C'].items() if k!='metadata_filter'}:
        raise ValueError('B and C must differ only by metadata_filter')
    frozen=None
    if args.split=='test':
        frozen=json.loads((args.dev_run/'run_manifest.json').read_text(encoding='utf-8'))
        if frozen['inputs_sha256']!=inputs or frozen['status']!='complete' or frozen['split']!='dev':
            raise ValueError('Code/config/input differs from completed dev run; heldout blocked')
    queries=jsonl_read(ROOT/f'benchmark/queries/{args.split}.jsonl')
    if any(set(q)!={'id','split','question','filter'} for q in queries):
        raise ValueError('Query-only file contains forbidden fields')
    run_id=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    output=ROOT/'results'/args.split/run_id
    output.mkdir(parents=True,exist_ok=False)
    run={'run_id':run_id,'split':args.split,'status':'started','inputs_sha256':inputs,'configs':configs,
         'model':expected,'store':'PostgreSQL + pgvector, exact cosine SQL ORDER BY; no ANN index',
         'cost_usd':0,'notes':'CPU only; timing includes computation, excludes model load; C recomputes documents like B. No test evaluated during dev.'}
    json_write(output/'run_manifest.json',run)
    try:
        print('Loading frozen corpus and local model...',flush=True)
        pages=load_source_units(ROOT)
        embedder=MyEmbedder(expected['EMBEDDING_MODEL'])
        store=PgVectorStore(database,embedder.dimensions)
        store.create_schema()
        chunks_by_strategy={}
        stats={}
        b_vectors=None
        for strategy,config in configs.items():
            started=time.perf_counter(); chunks=chunk_pages(pages,config)
            chunk_seconds=time.perf_counter()-started
            chunks_by_strategy[strategy]=chunks
            if strategy=='C' and chunks!=chunks_by_strategy['B']:
                raise ValueError('B/C chunks differ')
            if args.split=='test':
                if store.fingerprint(strategy)!=frozen['index_sha256'][strategy]:
                    raise ValueError('Database index differs from frozen dev run; test blocked')
                stats[strategy]=frozen['ingestion'][strategy]
                continue
            print(f'{strategy}: embedding {len(chunks)} chunks...',flush=True)
            started=time.perf_counter(); vectors=embedder.embed_documents([c.text for c in chunks])
            embedding_seconds=time.perf_counter()-started
            if strategy=='B':
                b_vectors=vectors
            if strategy=='C' and vectors!=b_vectors:
                raise ValueError('B/C vectors differ despite same inputs; stop before comparison')
            started=time.perf_counter(); store.upsert(strategy,chunks,vectors)
            store_seconds=time.perf_counter()-started
            first_count=store.count(strategy)
            store.upsert(strategy,chunks,vectors)
            if store.count(strategy)!=first_count or first_count!=len(chunks):
                raise ValueError('Reingestion duplicated or lost chunks')
            sizes=[len(c.text) for c in chunks]
            stats[strategy]={'chunk_count':len(chunks),'min_characters':min(sizes),'median_characters':statistics.median(sizes),
                'max_characters':max(sizes),'total_characters':sum(sizes),'embedding_tokens':sum(embedder.last_token_lengths),
                'max_embedding_tokens':max(embedder.last_token_lengths),'chunk_seconds':chunk_seconds,
                'embedding_seconds':embedding_seconds,'store_seconds':store_seconds,
                'ingest_seconds':chunk_seconds+embedding_seconds+store_seconds,'idempotent_reingestion':True,'cost_usd':0}
            print(f'{strategy}: stored {first_count}, repeated upsert verified',flush=True)
            json_write(output/'ingestion.json',stats)
        if args.split=='dev':
            export_coherence(output,pages,chunks_by_strategy)
        print(f'Embedding {len(queries)} {args.split} questions once for all strategies...',flush=True)
        started=time.perf_counter(); query_vectors=embedder.embed_queries([q['question'] for q in queries])
        run['query_embedding_seconds']=time.perf_counter()-started
        run['query_embedding_tokens']=sum(embedder.last_token_lengths)
        gold={q['id']:q for q in jsonl_read(ROOT/f'benchmark/{args.split}.jsonl')}
        traces=[]
        for strategy,config in configs.items():
            for query,vector in zip(queries,query_vectors):
                filters=query['filter'] if config['metadata_filter'] else {}
                started=time.perf_counter(); hits=store.search(strategy,vector,3,filters)
                seconds=time.perf_counter()-started
                trace=evaluate_query(gold[query['id']],hits)
                trace.update({'strategy':strategy,'question':query['question'],'requested_filter':query['filter'],
                              'applied_filter':filters,'search_seconds':seconds})
                if filters and any(h['metadata']['chapter']!=filters['chapter'] for h in hits):
                    raise AssertionError('SQL filter returned out-of-scope metadata')
                traces.append(trace)
        if args.split=='dev':
            for query in queries:
                if not query['filter']:
                    b=next(t for t in traces if t['strategy']=='B' and t['id']==query['id'])
                    c=next(t for t in traces if t['strategy']=='C' and t['id']==query['id'])
                    if b['hits']!=c['hits']:
                        raise AssertionError('B/C unfiltered retrieval differs')
        with (output/'traces.jsonl').open('w',encoding='utf-8',newline='\n') as stream:
            for trace in traces:
                stream.write(json.dumps(trace,ensure_ascii=False)+'\n')
        metrics=summarize(traces)
        json_write(output/'metrics.json',metrics)
        if args.split=='dev':
            chosen=min(configs,key=lambda s:(-metrics[s]['dev']['evidence_hit_at_3']['n'],
                -metrics[s]['dev']['hit_at_1']['n'],stats[s]['chunk_count'],stats[s]['ingest_seconds'],s))
        else:
            chosen=frozen['selected_on_dev']
        run.update({'status':'complete','ingestion':stats,'selected_on_dev':chosen,
            'selection_protocol':'dev Evidence Hit@3, dev Hit@1, fewer chunks, shorter measured ingest',
            'index_sha256':{s:store.fingerprint(s) for s in configs},'query_count':len(queries),
            'trace_count':len(traces),'human_audit':'not scored; coherence CSV labels remain blank'})
        json_write(output/'run_manifest.json',run)
        rows=['# Kết quả '+args.split,'',f'Run: `{run_id}`. Model E5 local + PostgreSQL/pgvector; dữ liệu thật đã chạy.','',
            '| Cấu hình | Hit@1 | Evidence Hit@3 | Số chunk | Ingest (giây) | Chi phí API |',
            '|---|---|---|---:|---:|---:|']
        for strategy in configs:
            metric=metrics[strategy][args.split]; a=metric['hit_at_1']; b=metric['evidence_hit_at_3']
            rows.append(f"| {strategy} | {a['n']}/{a['N']} | {b['n']}/{b['N']} | {stats[strategy]['chunk_count']} | {stats[strategy]['ingest_seconds']:.2f} | $0 |")
        rows += ['',f'Chọn theo dev: **{chosen}**. Không dùng test để đổi lựa chọn.',
            '', 'Chỉ số trên là khớp evidence trong một chunk, không phải độ chính xác câu trả lời LLM. Nhãn coherence/grounding/metadata thủ công chưa chấm.',
            '', 'Giới hạn: tập nhỏ, query tiếng Việt/nguồn tiếng Anh; cả ba index cùng lúc trên máy nên cache/CPU làm nhiễu thời gian. Ingest = chunk + embedding + lần store đầu, không tính lần upsert thứ hai dùng kiểm tra không trùng.',
            '', 'Xem `traces.jsonl`, `metrics.json`, `ingestion.json`, `run_manifest.json`; dev có thêm `coherence_audit.csv` để người học chấm.',
            '', 'Chưa chạy test; dừng chờ duyệt bước tiếp.' if args.split=='dev' else 'Đã chạy holdout sau khóa cấu hình; không tuning.', '']
        (output/'SUMMARY.md').write_text('\n'.join(rows),encoding='utf-8',newline='\n')
        json_write(ROOT/'results'/f'latest_{args.split}.json',{'path':output.relative_to(ROOT).as_posix(),'selected_on_dev':chosen})
        if args.split=='dev':
            with (ROOT/'artifacts/experiment_log.csv').open('w',encoding='utf-8',newline='') as stream:
                fields=['strategy','chunking','chunk_size','overlap','metadata','filter','vectorizer','hypothesis','dev_hit1','dev_hit3','test_hit1','test_hit3','notes']
                writer=csv.DictWriter(stream,fieldnames=fields); writer.writeheader()
                for s,config in configs.items():
                    writer.writerow({'strategy':s,'chunking':config['chunking'],'chunk_size':config['chunk_size'],'overlap':config['overlap'],
                        'metadata':'document_id,source,page,chapter,version,language,offsets','filter':config['metadata_filter'],
                        'vectorizer':embedder.model_name+'@'+embedder.revision,'hypothesis':{'A':'fixed baseline','B':'whole-block boundaries retain context','C':'explicit chapter filter narrows scope'}[s],
                        'dev_hit1':metrics[s]['dev']['hit_at_1']['rate'],'dev_hit3':metrics[s]['dev']['evidence_hit_at_3']['rate'],
                        'notes':'dev only; '+output.relative_to(ROOT).as_posix()})
        print(json.dumps({'output':str(output),'selected_on_dev':chosen,'metrics':metrics},ensure_ascii=False,indent=2),flush=True)
    except Exception as error:
        run.update({'status':'failed','error_type':type(error).__name__})
        json_write(output/'run_manifest.json',run)
        raise


if __name__ == "__main__":
    main()
