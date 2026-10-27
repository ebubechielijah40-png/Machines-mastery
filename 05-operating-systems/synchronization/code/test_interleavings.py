from collections import Counter
import itertools
import json
import unittest

from experiment import observe
from conditions import enumerate_conditions
from interleavings import enumerate_runs, program


class InterleavingTests(unittest.TestCase):
    def test_split_paths_against_independent_combinations(self):
        expected = Counter()
        for positions in itertools.combinations(range(6), 3):
            order = [0 if i in positions else 1 for i in range(6)]
            shared, local, steps = 0, [0, 0], [0, 0]
            for thread in order:
                phase = steps[thread]
                if phase == 0:
                    local[thread] = shared
                elif phase == 1:
                    local[thread] += 1
                else:
                    shared = local[thread]
                steps[thread] += 1
            expected[shared] += 1
        actual = enumerate_runs('split')
        self.assertEqual(len(actual), 20)
        self.assertEqual(Counter(r['final'] for r in actual), expected)
        self.assertEqual(expected, {1: 18, 2: 2})

    def test_whole_critical_section_and_fetch_add(self):
        for mode in ('whole_lock', 'fetch_add'):
            runs = enumerate_runs(mode)
            self.assertEqual(len(runs), 2)
            self.assertEqual({run['final'] for run in runs}, {2})

    def test_store_only_lock_has_counterexample(self):
        runs = enumerate_runs('store_lock')
        self.assertIn(1, {run['final'] for run in runs})
        for run in runs:
            owners = []
            for event in run['trace']:
                if event['operation'] == 'lock': owners.append(event['thread'])
                if event['operation'] == 'unlock': self.assertEqual(owners.pop(), event['thread'])
                self.assertLessEqual(len(owners), 1)

    def test_program_order_and_transition_invariants(self):
        for mode in ('split', 'whole_lock', 'store_lock', 'fetch_add'):
            instructions = program(mode)
            for run in enumerate_runs(mode):
                for thread in (0, 1):
                    self.assertEqual(tuple(e['operation'] for e in run['trace'] if e['thread'] == thread), instructions)
                self.assertEqual(run['trace'][0]['shared_before'], 0)
                for first, second in zip(run['trace'], run['trace'][1:]):
                    self.assertEqual(first['shared_after'], second['shared_before'])
        with self.assertRaises(ValueError): enumerate_runs('unknown')

    def test_predicate_while_remains_safe_after_spurious_wake(self):
        for budget in (0, 1):
            runs = enumerate_conditions('while', budget)
            self.assertTrue(runs)
            self.assertEqual({r['outcome'] for r in runs}, {'complete'})
            self.assertEqual({r['consumed'] for r in runs}, {1})

    def test_if_and_split_wait_have_different_counterexamples(self):
        unsafe = enumerate_conditions('if', 1)
        self.assertTrue(any(r['outcome'] == 'safety_failure' for r in unsafe))
        blocked = enumerate_conditions('split_wait', 0)
        witness = next(r for r in blocked if r['outcome'] == 'blocked')
        self.assertTrue(witness['full'])
        self.assertTrue(any(e['operation'] == 'notify_no_waiter' for e in witness['trace']))
        self.assertTrue(any(e['operation'] == 'register_too_late' for e in witness['trace']))
        # Independently derived bad orders; these are not copied result counts.
        lost_wake = ['acquire', 'check_predicate', 'release_without_register',
                     'acquire', 'put_item', 'notify_no_waiter', 'release',
                     'register_too_late']
        self.assertTrue(any([e['operation'] for e in r['trace']] == lost_wake
                            for r in blocked if r['outcome'] == 'blocked'))
        empty_wake = ['acquire', 'check_predicate', 'atomic_release_and_register',
                      'spurious_wake', 'acquire', 'consume_empty']
        self.assertTrue(any([e['operation'] for e in r['trace']] == empty_wake
                            for r in unsafe if r['outcome'] == 'safety_failure'))
        with self.assertRaises(ValueError): enumerate_conditions('unknown')
        with self.assertRaises(ValueError): enumerate_conditions('while', True)

    def test_actual_c_defined_interleaving_and_repairs(self):
        report = observe()
        programs = [json.loads(r['stdout']) for r in report['actual_c_commands']
                    if r['command'][0].endswith(('threads-0', 'threads-1', 'threads-2'))]
        self.assertEqual(len(programs), 3)
        for program_result in programs:
            self.assertEqual([row['last_observed_value'] for row in program_result['cases']], [1, 2, 2])
            self.assertEqual(program_result['cases'][0]['last_loaded_values'], [0, 0])
        buffers = [json.loads(r['stdout']) for r in report['actual_c_commands']
                   if r['command'][0].endswith(('condition-0', 'condition-1', 'condition-2'))]
        self.assertEqual(len(buffers), 3)
        for buffer in buffers:
            self.assertEqual(buffer['sum'], 5050)
            self.assertEqual(buffer['items'], 100)
            self.assertTrue(buffer['empty_after_join'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
