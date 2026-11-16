"""Replay verified real model traces; no API, database or simulated agent calls."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CASES = {
    'answer': ('results/test/20261116T034326996108Z/I1', 'T02', 'configs/test_review_approval.json'),
    'abstain': ('results/test/20261116T034326996108Z/I1', 'T06', 'configs/test_review_approval.json'),
    'error': ('results/dev/20261116T024332489435Z/dense', 'D07', 'configs/dev_review_approval.json'),
}


def load(path):
    return json.loads(path.read_text(encoding='utf-8'))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replay(kind):
    directory, ident, approval_name = CASES[kind]
    directory = ROOT / directory
    review_path = directory / 'reviews_ai_assisted.json'
    approval = load(ROOT / approval_name)
    key = review_path.relative_to(ROOT).as_posix()
    if kind == 'error':
        expected_review = approval['review_file_sha256'][key]
    else:
        expected_review = approval['review_files_sha256']['I1/reviews_ai_assisted.json']
    if digest(review_path) != expected_review:
        raise ValueError('Confirmed review file changed')
    review = next(r for r in load(review_path) if r['query_id'] == ident)
    trace_path = directory / (ident + '.json')
    if digest(trace_path) != review['trace_sha256']:
        raise ValueError('Recorded trace changed')
    trace = load(trace_path)
    expected_status = {'answer': 'answered', 'abstain': 'abstain', 'error': 'error'}[kind]
    if trace['status'] != expected_status:
        raise ValueError('Unexpected recorded outcome')
    searches = [e for e in trace['events'] if e['event'] == 'search']
    result = {
        'mode': 'REPLAY — recorded real model run; no new inference or benchmark score',
        'demo_case': kind, 'query_id': ident,
        'trace_file': trace_path.relative_to(ROOT).as_posix(),
        'trace_sha256_verified': True,
        'question': trace['question'], 'status': trace['status'],
        'tool_calls': [{'query': e['query'], 'result_ids': [c['id'] for c in e.get('results', [])],
                        'context_ids': e.get('context_ids', [])} for e in searches],
        'context': trace['context'], 'answer': trace['answer'], 'citations': trace['citations'],
        'confirmed_review': {k: review.get(k) for k in ('answer_grade','context_grade','abstention_correct','reason')},
        'new_api_cost_usd': 0,
    }
    if kind == 'error':
        result.update(error_stage=trace['error_stage'], error_type=trace['error_type'],
                      rejected_model_output=trace['model_calls'][-1]['response']['content'],
                      explanation='Real earlier protocol error: refusal returned nonempty citations. Kept as error, not a correct refusal or a new failure.')
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--case', choices=('all', *CASES), default='all')
    parser.add_argument('--export', type=Path, help='Write replay JSON to a local artifact')
    args = parser.parse_args()
    chosen = list(CASES) if args.case == 'all' else [args.case]
    values = [replay(kind) for kind in chosen]
    text = json.dumps(values, ensure_ascii=False, indent=2) + '\n'
    if args.export:
        args.export.parent.mkdir(parents=True, exist_ok=True)
        args.export.write_text(text, encoding='utf-8')
    print(text, end='')


if __name__ == '__main__':
    main()
