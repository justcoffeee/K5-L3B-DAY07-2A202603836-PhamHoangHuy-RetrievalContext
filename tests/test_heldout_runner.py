"""Offline gates; never read real held-out questions or call providers."""
import unittest
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))


class HeldoutGateTests(unittest.TestCase):
    def functions(self):
        try:
            from src.run_test import validate_test_queries,verify_frozen_runtime
        except ImportError:
            self.fail('held-out runner not implemented')
        return validate_test_queries,verify_frozen_runtime

    def test_query_gate_requires_seven_test_records_without_labels(self):
        validate,_=self.functions()
        qs=[{'id':f'T{i:02d}','split':'test','question':'query'} for i in range(1,8)]
        validate(qs)
        for invalid in (qs[:6],[{**q,'gold':[]} for q in qs],[{**q,'split':'dev'} for q in qs]):
            with self.assertRaises(ValueError):validate(invalid)

    def test_runtime_gate_checks_every_frozen_dependency_and_allows_new_runner(self):
        _,verify=self.functions()
        verify({'src/agent.py':'same'},{'src/agent.py':'same','src/run_test.py':'new'})
        with self.assertRaises(ValueError):verify({'src/agent.py':'same'},{'src/agent.py':'changed'})
        with self.assertRaises(ValueError):verify({'day6/store.py':'same'},{})


if __name__=='__main__':unittest.main()
