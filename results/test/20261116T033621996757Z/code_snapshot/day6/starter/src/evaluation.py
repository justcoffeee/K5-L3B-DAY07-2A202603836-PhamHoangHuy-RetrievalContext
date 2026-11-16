"""Evidence retrieval metrics, explicitly separate from human audit labels."""
from collections import defaultdict
from typing import Any


def evaluate_query(question: dict[str, Any], hits: list[dict[str, Any]]) -> dict[str, Any]:
    options = [question, *question.get('alternative_gold_evidence', [])]
    clean = lambda text: ' '.join(text.split())
    matches = []
    for hit in hits[:3]:
        meta = hit['metadata']
        matches.append(any(meta['document_id'] == gold['gold_source_id'] and str(meta['page']) == str(gold['gold_page'])
            and bool(clean(gold['evidence_quote'])) and clean(gold['evidence_quote']) in clean(hit['text']) for gold in options))
    return {'id':question['id'], 'split':question['split'],
            'hit_at_1':bool(matches and matches[0]), 'hit_at_3':any(matches),
            'evidence_match_by_rank':matches, 'hits':hits[:3], 'gold':question}


def summarize(traces: list[dict[str, Any]]) -> dict[str, Any]:
    grouped = defaultdict(lambda: defaultdict(list))
    for trace in traces:
        grouped[trace['strategy']][trace['split']].append(trace)
    return {strategy:{split:{name:{'n':sum(bool(t[field]) for t in rows), 'N':len(rows),
        'rate':sum(bool(t[field]) for t in rows)/len(rows)}
        for name,field in [('hit_at_1','hit_at_1'),('evidence_hit_at_3','hit_at_3')]}
        for split,rows in splits.items()} for strategy,splits in grouped.items()}
