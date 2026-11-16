"""Real lexical, dense and reciprocal-rank-fusion retrieval."""
import importlib
import importlib.util
from pathlib import Path
import sys
from starter.baseline import TfidfIndex


def check_request(filters, top_k):
    if type(top_k) is not int or not 1 <= top_k <= 100:
        raise ValueError('top_k must be 1..100')
    if filters and (set(filters) != {'chapter'} or type(filters['chapter']) is not int):
        raise ValueError('Only an explicit integer chapter filter is allowed')


class LexicalRetriever:
    def __init__(self, chunks):
        self.chunks = chunks
        self.index = TfidfIndex(chunks)

    def search(self, query, *, filters=None, top_k=3):
        check_request(filters, top_k)
        if not filters:
            return self.index.search(query, top_k)
        return TfidfIndex([c for c in self.chunks if c['metadata'].get('chapter') == filters['chapter']]).search(query, top_k)


def fuse_rrf(rankings, *, top_k=3, k=60):
    check_request(None, top_k)
    scores, chunks, components = {}, {}, {}
    for index, ranking in enumerate(rankings):
        seen = set()
        for chunk in ranking:
            cid = chunk['id']
            if cid in seen:
                continue
            seen.add(cid)
            rank = len(seen)
            chunks[cid] = chunk
            scores[cid] = scores.get(cid, 0) + 1 / (k + rank)
            components.setdefault(cid, []).append({'ranking': index, 'rank': rank, 'score': chunk.get('score')})
    return [{**chunks[cid], 'score': scores[cid], 'strategy': 'hybrid_rrf', 'components': components[cid]}
            for cid in sorted(scores, key=lambda cid: (-scores[cid], cid))[:top_k]]


class DenseRetriever:
    def __init__(self, store, embedder, strategy='C'):
        self.store, self.embedder, self.strategy = store, embedder, strategy
        self.query_cache = {}
        self.embedding_calls = 0

    def search(self, query, *, filters=None, top_k=3):
        check_request(filters, top_k)
        if query not in self.query_cache:
            self.query_cache[query] = self.embedder.embed_query(query)
            self.embedding_calls += 1
        rows = self.store.search(self.strategy, self.query_cache[query], top_k=top_k, filters=filters)
        return [dict(id=r['chunk_id'], text=r['text'], source_id=r['metadata']['document_id'],
                     source=r['metadata']['source'], page=r['metadata']['page'], metadata=r['metadata'],
                     score=r['score'], strategy='dense') for r in rows]


class HybridRetriever:
    def __init__(self, dense, lexical, depth=20, k=60):
        self.dense, self.lexical, self.depth, self.k = dense, lexical, depth, k

    def search(self, query, *, filters=None, top_k=3):
        check_request(filters, top_k)
        depth = max(self.depth, top_k)
        return fuse_rrf([self.dense.search(query, filters=filters, top_k=depth),
                         self.lexical.search(query, filters=filters, top_k=depth)], top_k=top_k, k=self.k)


def load_day6(day6, expected_fingerprint):
    """Reuse pinned offline runtime under a distinct package name; never ingest."""
    day6 = Path(day6).resolve()
    package = 'day6_runtime'
    if package not in sys.modules:
        spec = importlib.util.spec_from_file_location(package, day6 / 'starter/src/__init__.py',
                                                      submodule_search_locations=[str(day6 / 'starter/src')])
        module = importlib.util.module_from_spec(spec)
        sys.modules[package] = module
        spec.loader.exec_module(module)
    from dotenv import dotenv_values
    store_class = importlib.import_module(package + '.store').PgVectorStore
    embedder_class = importlib.import_module(package + '.embeddings').MyEmbedder
    store = store_class(dotenv_values(day6 / 'starter/.env')['DATABASE_URL'], 384)
    if store.fingerprint('C') != expected_fingerprint:
        raise ValueError('Day06 index changed; refusing evaluation')
    return DenseRetriever(store, embedder_class('intfloat/multilingual-e5-small'))
