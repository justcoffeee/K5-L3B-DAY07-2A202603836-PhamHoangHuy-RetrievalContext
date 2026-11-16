"""Deterministic chunks; text always remains a literal source substring."""
import hashlib
from .models import Chunk, DocumentPage


def fixed_size(page: DocumentPage, size: int, overlap: int) -> list[Chunk]:
    if size <= 0 or overlap < 0 or overlap >= size:
        raise ValueError('Require 0 <= overlap < size')
    chunks = []
    for start in range(0, len(page.text), size - overlap):
        end = min(start + size, len(page.text))
        if page.text[start:end].strip():
            chunks.append(make_chunk(page, start, end))
        if end == len(page.text):
            break
    return chunks


def by_paragraph(page: DocumentPage, max_size: int) -> list[Chunk]:
    if max_size <= 0:
        raise ValueError('max_size must be positive')
    spans = page.metadata.get('blocks')
    if spans is None:
        spans, offset = [], 0
        for part in page.text.split('\n\n'):
            if part.strip():
                spans.append({'start':offset, 'end':offset+len(part), 'kind':'paragraph', 'section_id':''})
            offset += len(part) + 2
    chunks = []
    pending = None
    section = None
    for block in spans:
        start, end = block['start'], block['end']
        if not 0 <= start < end <= len(page.text):
            raise ValueError('Invalid source block boundary')
        current_section = block.get('section_id', '')
        if pending is not None and (end - pending[0] > max_size or current_section != section):
            chunks.append(make_chunk(page, *pending))
            pending = None
        if end - start > max_size:
            while start < end:
                stop = min(start + max_size, end)
                if stop < end:
                    newline = page.text.rfind('\n', start, stop)
                    space = page.text.rfind(' ', start, stop)
                    boundary = newline if newline >= start + max_size // 2 else space
                    if boundary >= start + max_size // 2:
                        stop = boundary + 1
                chunks.append(make_chunk(page, start, stop))
                start = stop
        else:
            pending = (pending[0] if pending else start, end)
            section = current_section
    if pending is not None:
        chunks.append(make_chunk(page, *pending))
    return chunks


def make_chunk(page: DocumentPage, start: int, end: int) -> Chunk:
    text = page.text[start:end]
    identity = f'{page.document_id}\0{page.page}\0{start}\0{end}\0{text}'
    chunk_id = hashlib.sha256(identity.encode('utf-8')).hexdigest()[:32]
    blocks = [b for b in page.metadata.get('blocks', []) if b['start'] < end and b['end'] > start]
    metadata = {k:v for k,v in page.metadata.items() if k != 'blocks'}
    metadata.update({'char_start':start, 'char_end':end,
        'section_ids':list(dict.fromkeys(b.get('section_id','') for b in blocks)),
        'block_kinds':list(dict.fromkeys(b.get('kind','') for b in blocks))})
    return Chunk(chunk_id, page.document_id, page.source, page.page, text, metadata)
