"""Regression tests for prerequisite and evidence gates added by expansion."""
import copy
import json
from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from learning_gate import missing
from validate import ROOT, validate_catalog, STATES
from validate_expansion import validate


class ExpansionTests(unittest.TestCase):
    def setUp(self):
        self.data=json.loads((ROOT/'registries/catalog.json').read_text())
    def test_artifacts_valid(self):
        self.assertEqual(validate(self.data),[])
    def test_no_agent_mastery(self):
        self.assertEqual(self.data['mastery'],[])
        self.assertTrue(all(u['state']=='NOT STARTED' for u in self.data['units']))
    def test_unearned_prerequisites_block(self):
        gaps=missing(self.data,'U-CEX')
        self.assertIn('F-COUNT',gaps)
        self.assertIn('F-CENTRY',gaps)
    def test_entry_bridge_has_no_hidden_gate(self):
        self.assertEqual(missing(self.data,'F-COUNT'),[])
    def test_progress_label_without_review_is_insufficient(self):
        u=next(u for u in self.data['units'] if u['id']=='F-CENTRY')
        u.update(state='MASTERED',evidence=['AGENTS.md'])
        self.assertIn('F-CENTRY',missing(self.data,'U-CEX'))
    def test_cycle_rejected_by_reporter(self):
        self.data['units'][0]['required']=['U01']
        with self.assertRaises(ValueError):missing(self.data,'U01')
    def test_missing_bridge_rejected(self):
        self.data['lessons'][0]['bridge']='does-not-exist.md'
        errors,_=validate_catalog(self.data)
        self.assertTrue(any('does-not-exist' in e for e in errors))
    def test_quota_not_satisfied_by_scaffold(self):
        self.data['expansion_plan']['completed_algorithm_topics']=['strings']
        self.assertTrue(any('20 real problems' in e for e in validate(self.data)))
    def test_paper_metadata_cannot_be_invented_by_status(self):
        self.data['expansion_plan']['completed_paper_domains']=['compilers']
        self.assertTrue(any('ten verified papers' in e for e in validate(self.data)))
    def test_production_states_require_specific_evidence(self):
        self.assertIn('SCALABILITY-TESTED',STATES)
        self.data['mastery'].append(dict(id='M-PROD-TEST',unit_id='U-PROD',state='SCALABILITY-TESTED',assessed_on='2026-09-27',assessor='fixture',evidence=['AGENTS.md'],assistance='fixture',gaps=[],next_review='2026-10-01',criteria={}))
        errors,_=validate_catalog(self.data)
        self.assertTrue(any('missing state criterion baseline' in e for e in errors))
    def test_mastered_applied_unit_needs_operational_scope(self):
        keys=['delayed_recall','transfer','mechanism','failure_analysis','implementation','experiment','debugging','reconstruction','applied_scope']
        self.data['mastery'].append(dict(id='M-APPLIED-TEST',unit_id='U-PROD',state='MASTERED',assessed_on='2026-09-27',assessor='fixture',evidence=['AGENTS.md'],assistance='fixture',gaps=[],next_review='2026-10-01',criteria={k:'fixture' for k in keys}))
        errors,_=validate_catalog(self.data)
        self.assertTrue(any('missing mastery criterion operations' in e for e in errors))
    def test_original_dependencies_retained(self):
        units={u['id']:u for u in self.data['units']}
        self.assertTrue({'U04','U06'}.issubset(units['U07']['required']))
        self.assertTrue({'U09','U10','U11','U12'}.issubset(units['U17']['required']))
        self.assertTrue({'U03','U08','U12','U13'}.issubset(units['U19']['required']))


if __name__=='__main__':unittest.main()
