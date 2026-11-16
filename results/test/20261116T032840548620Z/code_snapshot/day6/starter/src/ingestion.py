"""Read physical PDF pages or the frozen, normalized HTML source units."""
from pathlib import Path
import hashlib
import json
import logging
import unicodedata
from .models import DocumentPage


def load_pdf(path: Path, document_id: str, source: str) -> list[DocumentPage]:
    from pypdf import PdfReader
    pages = []
    for number, page in enumerate(PdfReader(path).pages, 1):
        try:
            text = normalize_text(page.extract_text() or '')
            status = 'ok' if text.strip() else 'empty'
        except Exception as error:
            text, status = '', 'extraction_error:' + type(error).__name__
        if status != 'ok':
            logging.warning('PDF document=%s page=%s status=%s', document_id, number, status)
        pages.append(DocumentPage(document_id, source, number, text, {'extraction_status':status}))
    return pages


def normalize_text(text: str) -> str:
    return unicodedata.normalize('NFC', text.replace('\r\n','\n').replace('\r','\n'))


def load_source_units(root: Path) -> list[DocumentPage]:
    manifest = json.loads((root/'data/manifest.json').read_text(encoding='utf-8'))
    chapter_blocks = {}
    for source in manifest['sources']:
        if hashlib.sha256((root/source['local_path']).read_bytes()).hexdigest() != source['sha256']:
            raise ValueError('Raw source hash mismatch: ' + source['source_id'])
        chapter_path = root/source['normalized_path']
        if hashlib.sha256(chapter_path.read_bytes()).hexdigest() != source['normalized_sha256']:
            raise ValueError('Normalized source hash mismatch')
        chapter_blocks[source['source_id']] = json.loads(chapter_path.with_suffix('.blocks.json').read_text(encoding='utf-8'))
    pages = []
    for unit in manifest['units']:
        text = (root/unit['local_path']).read_text(encoding='utf-8')
        if len(text) < 1500 or hashlib.sha256(text.encode('utf-8')).hexdigest() != unit['sha256']:
            raise ValueError('Source unit invalid: ' + unit['unit_id'])
        blocks = [{'start':b['char_start']-unit['char_start'], 'end':b['char_end']-unit['char_start'],
                   'kind':b['kind'], 'section_id':b['section_id']} for b in chapter_blocks[unit['document_id']]
                  if unit['char_start'] <= b['char_start'] and b['char_end'] <= unit['char_end']]
        if not blocks:
            raise ValueError('Source unit has no typed blocks')
        pages.append(DocumentPage(unit['document_id'], unit['source'], unit['unit_id'], text,
            {'chapter':unit['chapter'], 'version':unit['version'], 'language':unit['language'],
             'unit_char_start_in_chapter':unit['char_start'], 'blocks':blocks}))
    if len(pages) < 30:
        raise ValueError('Corpus must have at least 30 validated source units')
    return pages
