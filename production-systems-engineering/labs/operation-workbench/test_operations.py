from concurrent.futures import ThreadPoolExecutor
from fractions import Fraction
from pathlib import Path
import sqlite3
import tempfile
import threading
import time
import unittest
from operations import BoundedService, Conflict, Observation, OperationStore, UnknownOutcome, evaluate, nearest_rank


class OperationsTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.path = Path(self.temp.name) / 'operations.db'
        self.store = OperationStore(self.path)

    def tearDown(self):
        self.temp.cleanup()

    def test_atomic_idempotency_conflict_and_retained_reply(self):
        self.assertEqual(self.store.apply('A', 5), (5, False))
        self.assertEqual(self.store.apply('B', 7), (12, False))
        self.assertEqual(self.store.apply('A', 5), (5, True))
        with self.assertRaises(Conflict):
            self.store.apply('A', 6)
        self.assertEqual(self.store.snapshot()['counter'], 12)
        self.assertEqual(len(self.store.snapshot()['operations']), 2)

    def test_precommit_failure_has_no_partial_effect(self):
        self.store.apply('old', 2)
        with self.assertRaises(RuntimeError):
            self.store.apply('new', 7, fault='before_commit')
        self.assertEqual(self.store.snapshot(), {'counter': 2, 'operations': [('old', 2, 2)]})
        self.assertEqual(self.store.apply('new', 7), (9, False))

    def test_postcommit_unknown_and_restart_reconciliation(self):
        with self.assertRaises(UnknownOutcome):
            self.store.apply('lost-reply', 9, fault='after_commit')
        fresh = OperationStore(self.path)
        self.assertEqual(fresh.apply('lost-reply', 9), (9, True))
        self.assertEqual(fresh.snapshot()['counter'], 9)

    def test_concurrent_duplicate_has_one_effect(self):
        def call(_):
            for attempt in range(10):
                try:
                    return self.store.apply('same', 4)
                except sqlite3.OperationalError:
                    time.sleep(.001)
            raise AssertionError('bounded controlled retries exhausted')
        with ThreadPoolExecutor(max_workers=8) as pool:
            replies = list(pool.map(call, range(24)))
        self.assertEqual(sum(not duplicate for _, duplicate in replies), 1)
        self.assertEqual({value for value, _ in replies}, {4})
        self.assertEqual(self.store.snapshot()['counter'], 4)

    def test_validation_and_counter_bound_rollback(self):
        for identity, delta in [('', 1), ('x'*65, 1), ('x\n', 1), ('x', True), ('x', 1001), (None, 1)]:
            with self.assertRaises(ValueError):
                self.store.apply(identity, delta)
        db = self.store.connect()
        try:
            db.execute('UPDATE counter SET value=? WHERE id=1', (10**12,))
        finally:
            db.close()
        with self.assertRaises(ValueError):
            self.store.apply('overflow', 1)
        self.assertEqual(self.store.snapshot()['operations'], [])

    def test_bounded_admission_and_exhaustion(self):
        entered, release = threading.Event(), threading.Event()
        class Gate:
            def apply(self, request_id, delta, fault='none'):
                entered.set()
                if not release.wait(2):
                    raise AssertionError('test release missing')
                return 1, False
        service = BoundedService(Gate(), workers=1, capacity=1, deadline_ms=1000, max_observations=2)
        try:
            first = service.submit('one', 1)
            self.assertTrue(entered.wait(1))
            second = service.submit('two', 1)
            self.assertEqual(second.result().status, 'overload')
            with self.assertRaises(ValueError):
                service.submit('three', 1)
            release.set()
            self.assertEqual(first.result(timeout=2).status, 'ok')
        finally:
            release.set()
            service.close()
        self.assertEqual(len(service.records), 2)
        with self.assertRaises(RuntimeError):
            service.submit('closed', 1)

    def test_expired_queued_request_does_not_apply(self):
        entered, release = threading.Event(), threading.Event()
        called = []
        class Gate:
            def apply(self, request_id, delta, fault='none'):
                called.append(request_id)
                entered.set()
                if not release.wait(2):
                    raise AssertionError('test release missing')
                return 1, False
        with BoundedService(Gate(), workers=1, capacity=2, deadline_ms=5) as service:
            first = service.submit('one', 1)
            self.assertTrue(entered.wait(1))
            second = service.submit('two', 1)
            time.sleep(.02)
            release.set()
            self.assertEqual(first.result(timeout=2).status, 'ok')
            self.assertEqual(second.result(timeout=2).status, 'deadline')
        self.assertEqual(called, ['one'])

    def test_service_outcome_accounting_under_controlled_faults(self):
        with BoundedService(self.store, deadline_ms=1000) as service:
            one = service.submit('pre', 1, fault='before_commit').result()
            two = service.submit('post', 2, fault='after_commit').result()
            three = service.submit('post', 2).result()
            self.assertEqual([one.status, two.status, three.status], ['injected_failure', 'unknown', 'duplicate'])
        self.assertEqual(self.store.snapshot()['counter'], 2)
        self.assertEqual(evaluate(service.records, 1_000_000_000)['eligible'], 3)

    def test_exact_slo_budget_and_percentile_denominator(self):
        records = [Observation(str(i), 0, 0, 0, 1 if i < 90 else 100, 'ok' if i < 90 else 'overload', 0 if i < 90 else None) for i in range(100)]
        result = evaluate(records, 50, Fraction(95, 100))
        self.assertEqual((result['good'], result['bad'], result['permitted_bad_exact'], result['remaining_bad_exact']), (90, 10, '5', '-5'))
        self.assertEqual(result['burn_rate'], 2)
        self.assertFalse(result['slo_met'])
        self.assertEqual(nearest_rank([1, 2, 9, 100], .95), 100)
        empty = evaluate([], 1)
        self.assertIsNone(empty['slo_met'])
        self.assertIsNone(empty['good_ratio'])

    def test_metric_validation_and_clock_order(self):
        for record in [Observation('x', 2, 1, 3, 4, 'ok', 0), Observation('x', False, 1, 2, 3, 'ok', 0)]:
            with self.assertRaises(ValueError):
                evaluate([record], 1)
        for q in [0, 1.1, float('nan'), True]:
            with self.assertRaises(ValueError):
                nearest_rank([1], q)
        with self.assertRaises(ValueError):
            nearest_rank([float('inf')], .5)


if __name__ == '__main__':
    unittest.main(verbosity=2)
