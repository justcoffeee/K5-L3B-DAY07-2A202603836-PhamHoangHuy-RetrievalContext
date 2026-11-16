"""Read-only Day06 verification and Day07 data export; no benchmark/model API calls."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import shutil
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--day6', required=True, type=Path)
    args = parser.parse_args()
    day6 = args.day6.resolve()
    root = Path(__file__).resolve().parents[1]
    output = root / 'data/day6'
    sys.path.insert(0, str(root / 'starter'))
    from convert_day6 import convert_chunk
    sys.path.insert(0, str(day6 / 'starter'))
    from dotenv import dotenv_values
    from src.embeddings import MyEmbedder
    from src.store import PgVectorStore

    frozen = json.loads((day6 / 'results/dev/20261114T035115831944Z/run_manifest.json').read_text(encoding='utf-8'))
    strategy = frozen['selected_on_dev']
    store = PgVectorStore(dotenv_values(day6 / 'starter/.env')['DATABASE_URL'], 384)
    # Inspect the existing store, never create a schema or ingest/re-embed documents.
    with store.connect() as connection, connection.cursor() as cursor:
        cursor.execute('SET TRANSACTION READ ONLY')
        cursor.execute("SELECT extversion FROM pg_extension WHERE extname='vector'")
        extension_version = cursor.fetchone()[0]
        cursor.execute('SELECT strategy,count(*) FROM public.lab_chunks GROUP BY strategy ORDER BY strategy')
        counts = dict(cursor.fetchall())
        cursor.execute('SELECT chunk_id,document_id,source,page,content,metadata,embedding::text FROM public.lab_chunks WHERE strategy=%s ORDER BY chunk_id', (strategy,))
        rows = cursor.fetchall()
    fingerprint = hashlib.sha256(json.dumps(rows, ensure_ascii=False, sort_keys=True).encode('utf-8')).hexdigest()
    if fingerprint != frozen['index_sha256'][strategy]:
        raise ValueError('Day06 index differs from the frozen dev snapshot')
    units_path = day6 / 'data/processed/source_units.jsonl'
    units = [json.loads(line) for line in units_path.read_text(encoding='utf-8').splitlines() if line.strip()]
    by_page = {(u['document_id'], str(u['page'])): u for u in units}
    chunks = []
    for chunk_id, document_id, source, page, content, metadata, vector_text in rows:
        vector = json.loads(vector_text)
        if len(vector) != 384 or not all(math.isfinite(x) for x in vector):
            raise ValueError('Invalid stored embedding')
        if abs(math.sqrt(sum(x*x for x in vector)) - 1) > 0.001:
            raise ValueError('Stored embedding is not normalized')
        unit = by_page[(document_id, page)]
        start, end = metadata['char_start'], metadata['char_end']
        if unit['source'] != source or unit['text'][start:end] != content:
            raise ValueError('Chunk no longer matches its original source offsets')
        chunks.append(convert_chunk(dict(chunk_id=chunk_id, document_id=document_id,
                                         source=source, page=page, text=content, metadata=metadata)))
    if not chunks or len({c['id'] for c in chunks}) != len(chunks):
        raise ValueError('Missing/duplicate chunks')
    embedder = MyEmbedder('intfloat/multilingual-e5-small')
    query = 'How do I add an item to the end of a Python list?'
    query_vector = embedder.embed_query(query)
    results = store.search(strategy, query_vector, top_k=3)
    valid_ids = {c['id'] for c in chunks}
    if len(query_vector) != 384 or len(results) != 3 or any(r['chunk_id'] not in valid_ids for r in results):
        raise ValueError('Dense retrieval smoke check failed')
    output.mkdir(parents=True, exist_ok=True)
    (output / 'chunks.json').write_text(json.dumps(chunks, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    copies = {'source_units.jsonl': units_path, 'source_manifest.json': day6 / 'data/manifest.json',
              'license.html': day6 / 'data/raw/python-3.14/license.html',
              'copyright.html': day6 / 'data/raw/python-3.14/copyright.html'}
    for name, source in copies.items():
        shutil.copyfile(source, output / name)
    manifest = {
        'stage': 'step1_data_prepared_awaiting_review',
        'verified_at_utc': datetime.now(timezone.utc).isoformat(),
        'day6_repository': 'https://github.com/justcoffeee/K5-L3B-DAY06-PhamHoangHuy-2A202603836-DataIngestion',
        'day6_commit': subprocess.check_output(['git', '-C', str(day6), 'rev-parse', 'HEAD'], text=True).strip(),
        'strategy': strategy, 'selection': 'Reuse Day06 dev-selected C; no Day07 benchmark evaluated',
        'store_counts': counts, 'pgvector_version': extension_version,
        'index_sha256': fingerprint, 'matches_frozen_day6_index': True,
        'chunks': len(chunks), 'source_units': len(units),
        'documents': len({c['source_id'] for c in chunks}),
        'all_chunks_match_source_offsets': True,
        'all_vectors_finite_normalized_384d': True,
        'embedding': frozen['model'],
        'smoke_check': {'query': query, 'query_dimensions': len(query_vector),
                        'top3': results, 'note': 'Connectivity check only; not a scored benchmark or quality claim'},
        'api_cost_usd': 0, 'database_modified': False,
        'files_sha256': {name: hashlib.sha256((output / name).read_bytes()).hexdigest()
                         for name in ['chunks.json', *copies]},
        'page_semantics': 'page is the stable Day06 source-unit ID, not a printed page number',
        'benchmark': 'Not created; Day06 test was already inspected; prepare a new Day07 held-out set later',
    }
    (output / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k: manifest[k] for k in ('stage', 'store_counts', 'chunks', 'source_units', 'documents',
          'matches_frozen_day6_index', 'all_chunks_match_source_offsets', 'all_vectors_finite_normalized_384d')}, indent=2))


if __name__ == '__main__':
    main()
