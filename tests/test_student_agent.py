"""Offline behavior tests; these are not benchmark/model quality results."""
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

try:
    from src.retrieval import LexicalRetriever, fuse_rrf
    from src.agent import run
except ImportError:
    LexicalRetriever = fuse_rrf = run = None


def chunk(cid, text='Evidence here', chapter=4):
    return dict(id=cid, text=text, source_id='doc', source='https://example.org',
                page='unit1', metadata={'chapter': chapter}, score=0.9)


class RetrievalTests(unittest.TestCase):
    def test_lexical_does_not_invent_zero_overlap_hits_and_applies_filter(self):
        self.assertIsNotNone(LexicalRetriever, 'retrieval adapter missing')
        r = LexicalRetriever([chunk('a','keyword',3),chunk('b','keyword',4)])
        self.assertEqual(r.search('absent', top_k=3, filters=None), [])
        self.assertEqual([x['id'] for x in r.search('keyword',top_k=3,filters={'chapter':4})],['b'])
        with self.assertRaises(ValueError):r.search('keyword',top_k=3,filters={'gold_page':'unit1'})

    def test_fusion_deduplicates_each_ranking_and_is_stable(self):
        self.assertIsNotNone(fuse_rrf, 'fusion missing')
        result=fuse_rrf([[chunk('b'),chunk('b'),chunk('a')],[chunk('a'),chunk('b')]],top_k=3)
        self.assertEqual([x['id'] for x in result],['a','b'])
        self.assertAlmostEqual(result[0]['score'],1/61+1/62)


class ScriptedProvider:
    def __init__(self, replies):self.replies=iter(replies);self.messages=[];self.records=[]
    def complete(self,messages,tools,choice):
        import json
        self.messages.append(json.loads(json.dumps(messages)))
        self.records.append({'usage':{'total_tokens':10}})
        reply=next(self.replies)
        if isinstance(reply,Exception):raise reply
        return reply


def search(query='term',cid='call1'):
    import json
    return {'role':'assistant','content':None,'tool_calls':[{'id':cid,'type':'function','function':{'name':'search_documents','arguments':json.dumps({'query':query})}}]}


def answer(text='Evidence here [c1]',citations=None,abstain=False):
    import json
    return {'role':'assistant','content':json.dumps({'answer':text,'citations':['c1'] if citations is None else citations,'abstain':abstain})}


class AgentBehaviorTests(unittest.TestCase):
    def test_latest_context_can_replace_stale_chunk_within_same_budget(self):
        class R:
            def search(self,query,**kwargs):return [chunk('c1' if query=='first' else 'c2')]
        provider=ScriptedProvider([search('first'),search('second','call2'),answer('Evidence here [c2]',['c2'])])
        out=run('question',provider,R(),budget=85,context_policy='latest')
        self.assertEqual(out['status'],'answered')
        self.assertEqual(out['context_ids'],['c2'])
        self.assertEqual(out['events'][0]['context_ids'],['c1'])
        self.assertLessEqual(len(out['context']),85)

    def test_arrival_context_preserves_existing_behavior_and_rejects_unknown_policy(self):
        class R:
            def search(self,query,**kwargs):return [chunk('c1' if query=='first' else 'c2')]
        provider=ScriptedProvider([search('first'),search('second','call2'),answer()])
        out=run('question',provider,R(),budget=85,context_policy='arrival')
        self.assertEqual(out['status'],'answered')
        self.assertEqual(out['context_ids'],['c1'])
        with self.assertRaises(ValueError):run('q',ScriptedProvider([]),R(),context_policy='gold')

    def test_two_searches_keep_only_latest_active_context(self):
        self.assertIsNotNone(run,'real agent loop missing')
        p=ScriptedProvider([search(),search('again','call2'),answer()])
        class R:
            def search(self,query,**kwargs):return [chunk('c1')]
        out=run('question',p,R(),budget=100)
        self.assertEqual(out['status'],'answered')
        self.assertEqual(len([e for e in out['events'] if e['event']=='search']),2)
        import json
        tools=[json.loads(m['content']) for m in p.messages[-1] if m['role']=='tool']
        self.assertEqual(sum('context' in m for m in tools),1)
        self.assertLessEqual(len(out['context']),100)

    def test_unknown_citation_is_error_not_correct_abstention(self):
        self.assertIsNotNone(run,'real agent loop missing')
        class R:
            def search(self,*args,**kwargs):return [chunk('c1')]
        out=run('question',ScriptedProvider([search(),answer('claim [bad]',['bad'])]),R())
        self.assertEqual(out['status'],'error')
        self.assertEqual(out['error_stage'],'protocol')
        self.assertEqual(out['events'][0]['event'],'search')

    def test_store_error_keeps_request_trace_and_does_not_fake_refusal(self):
        self.assertIsNotNone(run,'real agent loop missing')
        class R:
            def search(self,*args,**kwargs):raise ConnectionError('sensitive connection details')
        out=run('question',ScriptedProvider([search()]),R())
        self.assertEqual(out['status'],'error')
        self.assertEqual(out['error_stage'],'retrieval')
        self.assertNotIn('sensitive',str(out))
        self.assertEqual(out['events'][0]['query'],'term')

    def test_explicit_refusal_after_search_is_preserved_for_later_review(self):
        self.assertIsNotNone(run,'real agent loop missing')
        class R:
            def search(self,*args,**kwargs):return []
        out=run('question',ScriptedProvider([search(),answer('Không đủ bằng chứng trong tài liệu.',[],True)]),R())
        self.assertEqual(out['status'],'abstain')
        self.assertEqual(out['reason'],'model_abstention')

    def test_provider_failure_keeps_prior_search_and_usage(self):
        self.assertIsNotNone(run,'real agent loop missing')
        class R:
            def search(self,*args,**kwargs):return [chunk('c1')]
        p=ScriptedProvider([search(),TimeoutError('secret')])
        out=run('question',p,R())
        self.assertEqual(out['status'],'error')
        self.assertEqual(out['error_stage'],'provider')
        self.assertEqual(len(out['events']),1)
        self.assertEqual(len(out['model_calls']),2)


class ProviderTests(unittest.TestCase):
    def test_transient_socket_timeout_retries_without_losing_failed_attempt(self):
        import io,json,urllib.error
        from unittest.mock import patch
        from src.provider import DeepSeek
        p=DeepSeek({'API_ENDPOINT':'https://api.deepseek.com','API_MODEL':'deepseek-flash',
                    'API_THINKING':'disabled','API_KEY':'private-test-key'})
        response={'model':'deepseek-flash','choices':[{'message':{'role':'assistant','content':'OK'}}],'usage':{'total_tokens':2}}
        with patch('urllib.request.urlopen',side_effect=[urllib.error.URLError(TimeoutError(10060,'sensitive details')),io.BytesIO(json.dumps(response).encode())]) as http,patch('time.sleep'):
            self.assertEqual(p.complete([],[],'none')['content'],'OK')
        self.assertEqual(http.call_count,2)
        self.assertEqual([r['status'] for r in p.records],['error','ok'])
        self.assertEqual(p.records[0]['transport_errno'],10060)
        self.assertNotIn('sensitive',json.dumps(p.records))

    def test_transport_retries_are_bounded_and_permission_error_is_not_retried(self):
        import urllib.error
        from unittest.mock import patch
        from src.provider import DeepSeek,ProviderError
        settings={'API_ENDPOINT':'https://api.deepseek.com','API_MODEL':'deepseek-flash',
                  'API_THINKING':'disabled','API_KEY':'private-test-key'}
        p=DeepSeek(settings)
        with patch('urllib.request.urlopen',side_effect=urllib.error.URLError(TimeoutError(10060,'timeout'))) as http,patch('time.sleep'):
            with self.assertRaises(ProviderError):p.complete([],[],'none')
        self.assertEqual(http.call_count,3)
        self.assertEqual(len(p.records),3)
        p=DeepSeek(settings)
        with patch('urllib.request.urlopen',side_effect=urllib.error.URLError(PermissionError(10013,'denied'))) as http,patch('time.sleep'):
            with self.assertRaises(ProviderError):p.complete([],[],'none')
        self.assertEqual(http.call_count,1)

    def test_malformed_choices_do_not_discard_known_billable_usage(self):
        import io,json
        from unittest.mock import patch
        from src.provider import DeepSeek,ProviderError
        p=DeepSeek({'API_ENDPOINT':'https://api.deepseek.com','API_MODEL':'deepseek-flash',
                    'API_THINKING':'disabled','API_KEY':'private-test-key'})
        with patch('urllib.request.urlopen',return_value=io.BytesIO(json.dumps({'choices':[], 'usage':{'total_tokens':127}}).encode())):
            with self.assertRaises(ProviderError):p.complete([],[],'none')
        self.assertEqual(p.records[0].get('usage',{}).get('total_tokens'),127)

    def test_logged_request_is_immutable_and_never_contains_authorization(self):
        import io,json
        from unittest.mock import patch
        from src.provider import DeepSeek
        p=DeepSeek({'API_ENDPOINT':'https://api.deepseek.com','API_MODEL':'deepseek-flash',
                    'API_THINKING':'disabled','API_KEY':'private-test-key'})
        messages=[{'role':'user','content':'first'}]
        response={'model':'deepseek-flash','choices':[{'message':{'role':'assistant','content':'{}'},'finish_reason':'stop'}],'usage':{'total_tokens':1}}
        with patch('urllib.request.urlopen',return_value=io.BytesIO(json.dumps(response).encode())):
            p.complete(messages,[], 'none')
        messages.append({'role':'user','content':'later'})
        self.assertEqual(len(p.records[0]['request']['messages']),1)
        self.assertNotIn('private-test-key',json.dumps(p.records))


class RunnerTests(unittest.TestCase):
    def test_resume_hashes_cover_imported_runtime_dependencies(self):
        import tempfile
        try:
            from src.run_dev import runtime_hashes
        except ImportError:
            self.fail('runtime dependency hashes missing')
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder)/'day7';day6=Path(folder)/'day6'
            for p in (root/'src/agent.py',root/'starter/baseline.py',day6/'starter/src/store.py',day6/'requirements-lock.txt'):
                p.parent.mkdir(parents=True,exist_ok=True);p.write_text('before',encoding='utf-8')
            before=runtime_hashes(day6,root)
            (root/'starter/baseline.py').write_text('changed',encoding='utf-8')
            (day6/'starter/src/store.py').write_text('changed',encoding='utf-8')
            after=runtime_hashes(day6,root)
            self.assertNotEqual(before['starter/baseline.py'],after['starter/baseline.py'])
            self.assertNotEqual(before['day6/starter/src/store.py'],after['day6/starter/src/store.py'])

    def test_query_gate_rejects_labels_and_test(self):
        try:
            from src.run_dev import validate_queries
        except ImportError:
            self.fail('dev-only runner missing')
        validate_queries([{'id':'D01','split':'dev','question':'q'}])
        for bad in ({'id':'D01','split':'dev','question':'q','gold':[]},
                    {'id':'T01','split':'test','question':'q'}):
            with self.assertRaises(ValueError):validate_queries([bad])

    def test_metrics_exclude_unanswerable_from_retrieval_denominator(self):
        try:
            from src.run_dev import summarize
        except ImportError:
            self.fail('dev-only scorer missing')
        c=chunk('c1')
        cases=[{'id':'D01','answerable':True,'gold':[{'source_id':'doc','page':'unit1','evidence':'Evidence here'}]},
               {'id':'D02','answerable':False}]
        traces=[{'query_id':'D01','status':'answered','original_results':[c],'context_ids':['c1'],
                 'context':'Evidence here','events':[{'event':'search','results':[c]}],
                 'model_calls':[],'elapsed_seconds':1,'citations':['c1']},
                {'query_id':'D02','status':'abstain','original_results':[],'context_ids':[],
                 'context':'','events':[{'event':'search','results':[]}],'model_calls':[],'elapsed_seconds':1,'citations':[]}]
        s=summarize(cases,traces)
        self.assertEqual(s['original_query']['hit3'],{'n':1,'N':1,'rate':1.0})
        self.assertEqual(s['final_context_evidence'],{'n':1,'N':1,'rate':1.0})
        self.assertIsNone(s['semantic_quality'])


if __name__=='__main__':unittest.main()
