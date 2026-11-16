"""Persistent exact cosine search; full-snapshot upsert within one strategy."""
import hashlib
import json
import math
from typing import Any
from .models import Chunk


class PgVectorStore:
    def __init__(self, database_url: str, dimensions: int) -> None:
        if type(dimensions) is not int or not 0 < dimensions <= 16000:
            raise ValueError('Invalid vector dimensions')
        self.database_url, self.dimensions = database_url, dimensions

    def connect(self):
        import psycopg
        return psycopg.connect(self.database_url, connect_timeout=10)

    def vector(self, values):
        if len(values) != self.dimensions or not all(math.isfinite(float(v)) for v in values) or not any(float(v) != 0 for v in values):
            raise ValueError('Vector must be finite, nonzero and match dimensions')
        return '[' + ','.join(format(float(v),'.9g') for v in values) + ']'

    def create_schema(self) -> None:
        from psycopg import sql
        with self.connect() as connection, connection.cursor() as cursor:
            cursor.execute("SELECT extversion FROM pg_extension WHERE extname='vector'")
            if cursor.fetchone() is None:
                raise RuntimeError('Enable pgvector through starter setup before running pipeline')
            cursor.execute(sql.SQL('''CREATE TABLE IF NOT EXISTS public.lab_chunks (
                strategy text NOT NULL, chunk_id text NOT NULL, document_id text NOT NULL,
                source text NOT NULL, page text NOT NULL, content text NOT NULL, metadata jsonb NOT NULL,
                embedding vector({}) NOT NULL, PRIMARY KEY(strategy,chunk_id))''').format(sql.Literal(self.dimensions)))
            cursor.execute("SELECT atttypmod FROM pg_attribute WHERE attrelid='public.lab_chunks'::regclass AND attname='embedding'")
            if cursor.fetchone()[0] != self.dimensions:
                raise ValueError('Existing lab_chunks vector dimension differs; do not drop data automatically')

    def upsert(self, strategy: str, chunks: list[Chunk], vectors: list[list[float]]) -> None:
        if len(chunks) != len(vectors) or len({c.chunk_id for c in chunks}) != len(chunks):
            raise ValueError('Chunk/vector counts or IDs are invalid')
        literals = [self.vector(v) for v in vectors]
        from psycopg.types.json import Jsonb
        rows = [(strategy,c.chunk_id,c.document_id,c.source,str(c.page),c.text,Jsonb(c.metadata),v)
                for c,v in zip(chunks,literals)]
        with self.connect() as connection, connection.cursor() as cursor:
            cursor.execute('SELECT pg_advisory_xact_lock(hashtextextended(%s,0))', ('day6:' + strategy,))
            if rows:
                cursor.executemany('''INSERT INTO public.lab_chunks VALUES(%s,%s,%s,%s,%s,%s,%s,%s::vector)
                    ON CONFLICT(strategy,chunk_id) DO UPDATE SET document_id=EXCLUDED.document_id, source=EXCLUDED.source,
                    page=EXCLUDED.page, content=EXCLUDED.content, metadata=EXCLUDED.metadata, embedding=EXCLUDED.embedding''',rows)
            cursor.execute('DELETE FROM public.lab_chunks WHERE strategy=%s AND NOT (chunk_id=ANY(%s::text[]))',
                           (strategy,[c.chunk_id for c in chunks]))

    def search(self, strategy: str, query_vector: list[float], top_k: int = 3,
               filters: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        vector = self.vector(query_vector)
        if not 1 <= top_k <= 100:
            raise ValueError('top_k must be 1..100')
        filters = filters or {}
        if set(filters) - {'chapter'} or ('chapter' in filters and type(filters['chapter']) is not int):
            raise ValueError('Only explicit integer chapter filter is supported; gold/source filters are forbidden')
        where, params = 'strategy=%s', [strategy]
        if filters:
            where += " AND metadata->>'chapter'=%s"
            params.append(str(filters['chapter']))
        statement = '''SELECT chunk_id,content,document_id,source,page,metadata,1-(embedding <=> %s::vector)
            FROM public.lab_chunks WHERE ''' + where + ' ORDER BY embedding <=> %s::vector,chunk_id LIMIT %s'
        with self.connect() as connection, connection.cursor() as cursor:
            cursor.execute(statement,[vector,*params,vector,top_k])
            return [{'chunk_id':r[0],'text':r[1],'metadata':{**r[5],'document_id':r[2],'source':r[3],'page':r[4]},'score':float(r[6])}
                    for r in cursor.fetchall()]

    def count(self, strategy):
        with self.connect() as connection, connection.cursor() as cursor:
            cursor.execute('SELECT count(*) FROM public.lab_chunks WHERE strategy=%s',(strategy,))
            return cursor.fetchone()[0]

    def fingerprint(self, strategy):
        with self.connect() as connection, connection.cursor() as cursor:
            cursor.execute('SELECT chunk_id,document_id,source,page,content,metadata,embedding::text FROM public.lab_chunks WHERE strategy=%s ORDER BY chunk_id',(strategy,))
            return hashlib.sha256(json.dumps(cursor.fetchall(),ensure_ascii=False,sort_keys=True).encode('utf-8')).hexdigest()
