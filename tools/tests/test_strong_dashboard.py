import copy
from fractions import Fraction
import importlib.util
import json
from pathlib import Path
import unittest

spec=importlib.util.spec_from_file_location('dashboard',Path(__file__).resolve().parents[1]/'strong_dashboard.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)


def domain():
    return dict(current={k:[2,2,2,1] for k in m.WEIGHTS},tests_passed=True,
                independent_review=True,scope_breadth_confirmed=True,
                critical_errors=[],mandatory_blockers=[])


class DashboardTests(unittest.TestCase):
    def test_exact_weighted_arithmetic(self):
        d=domain();d['current']['implementation']=[2,2,2,2]
        criteria,total=m.scores(d)
        self.assertEqual(criteria['instruction'],Fraction(175,2))
        self.assertEqual(total,Fraction(90))

    def test_overall_threshold_is_insufficient(self):
        d=domain();d['current']={k:[2]*4 for k in m.WEIGHTS}
        d['current']['prerequisites']=[2,1,1,1]
        self.assertGreater(m.scores(d)[1],85)
        self.assertEqual(m.rating(d),'PARTIAL')

    def test_each_non_numeric_gate_matters(self):
        for field in ('tests_passed','independent_review','scope_breadth_confirmed'):
            d=domain();d[field]=False
            self.assertEqual(m.rating(d),'PARTIAL')

    def test_critical_error_cannot_be_averaged_away(self):
        d=domain();d['critical_errors']=['incorrect foundational example']
        self.assertEqual(m.rating(d),'PARTIAL')

    def test_genuine_blocker_is_visible(self):
        d=domain();d['mandatory_blockers']=['required compiler unavailable']
        self.assertEqual(m.rating(d),'BLOCKED')

    def test_reject_changed_denominator_and_non_marks(self):
        for value in ([2,2,2], [2,2,2,2,2], [2,2,2,True], [2,2,2,3]):
            d=domain();d['current']['instruction']=value
            with self.assertRaises(ValueError):m.scores(d)

    def test_scope_and_weight_changes_are_rejected(self):
        bad={'weights':dict(m.WEIGHTS,instruction=30),'domains':[]}
        with self.assertRaises(ValueError):m.validate(bad)
        d=domain();d.update(id='x',strong_scope='changed',full_mandate_scope='original',scope_sha256='0'*64)
        with self.assertRaisesRegex(ValueError,'scope changed'):
            m.validate({'weights':m.WEIGHTS,'domains':[d]})

    def test_threshold_does_not_count_as_gate(self):
        a=domain();a['original_mandate_excellent_gate_closed']=False
        b=copy.deepcopy(a);b['scope_breadth_confirmed']=False
        summary=m.aggregates({'domains':[a,b]})
        self.assertEqual(summary['strong_count'],1)
        self.assertEqual(summary['strong_readiness_percent'],87.5)
        self.assertEqual(m.computed(b)['remaining_to_strong_threshold'],0)
        self.assertEqual(m.computed(b)['rating'],'PARTIAL')

    def test_all33_denominator_and_stale_accounting(self):
        data=json.loads((m.ROOT/'registries/strong_progress.json').read_text())
        m.validate(data)
        bad=copy.deepcopy(data);bad['domains'].pop()
        with self.assertRaisesRegex(ValueError,'all33'):m.validate(bad)
        bad=copy.deepcopy(data);bad['domains'][0]['computed']['readiness_percent']=100
        with self.assertRaisesRegex(ValueError,'stale derived'):m.validate(bad)


if __name__=='__main__':unittest.main(verbosity=2)
