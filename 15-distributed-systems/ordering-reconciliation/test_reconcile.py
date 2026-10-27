import itertools
import unittest
from reconcile import Envelope, LogicalClock, MAX_COUNTER, Record, Replica, join_states


class ReconciliationTests(unittest.TestCase):
    def test_clock_send_receive_and_nonconverse(self):
        a, b = LogicalClock(), LogicalClock()
        send = a.event()
        self.assertEqual(send, 1)
        self.assertEqual(b.receive(send), 2)
        self.assertGreater(b.event(), send)
        independent = LogicalClock()
        self.assertEqual(independent.event(), 1)
        # independent's next local event has stamp2 without any message from a.
        self.assertEqual(independent.event(), 2)
        # Clock inequality alone is no evidence of a message/causal edge.

    def test_envelope_preserves_send_clock_even_for_unchanged_state(self):
        a,b=Replica('A'),Replica('B')
        a.put('x','old')
        for _ in range(20):a.clock.event()
        message=a.send()
        self.assertGreater(message.counter,message.records[0].counter)
        b.receive(message)
        self.assertGreater(b.clock.value,message.counter)
        self.assertEqual(b.visible(),{'x':'old'})
        before,clock=b.snapshot(),b.clock.value
        with self.assertRaises(ValueError):b.receive(Envelope(0,message.records))
        self.assertEqual(b.snapshot(),before);self.assertEqual(b.clock.value,clock)

    def test_concurrent_conflicts_converge_with_total_tie_rule(self):
        a, b = Replica('A'), Replica('B')
        a.put('x', 'A-first'); b.put('x', 'B-first')
        a0, b0 = a.snapshot(), b.snapshot()
        a.merge(b0); b.merge(a0)
        self.assertEqual(a.visible(), {'x': 'B-first'})
        self.assertEqual(a.snapshot(), b.snapshot())
        self.assertFalse(a.merge(b0))
        a.put('x', 'A-after-seeing-B')
        b.merge(a.snapshot())
        self.assertEqual(b.visible(), {'x': 'A-after-seeing-B'})

    def test_all_delivery_permutations_and_duplicates_preserve_winner(self):
        events = [Record('x', 'a', 1, 'A'), Record('x', 'b', 1, 'B'),
                  Record('y', 'old', 2, 'A'), Record('y', 'new', 3, 'B')]
        expected = (events[1], events[3])
        for order in itertools.permutations(events):
            replica = Replica('C')
            for event in order + order[:2]:
                replica.merge((event,))
            self.assertEqual(replica.snapshot(), expected)

    def test_merge_algebra_on_maps_not_receive_clock(self):
        x = (Record('x', 'a', 1, 'A'),)
        y = (Record('x', 'b', 1, 'B'), Record('y', 'c', 2, 'B'))
        z = (Record('y', None, 3, 'C'),)
        self.assertEqual(join_states(x, x), x)
        self.assertEqual(join_states(x, y), join_states(y, x))
        self.assertEqual(join_states(join_states(x, y), z), join_states(x, join_states(y, z)))

    def test_tombstone_prevents_resurrection_and_naive_gc_breaks_it(self):
        a, b = Replica('A'), Replica('B')
        a.put('x', 'old'); b.merge(a.snapshot())
        stale = b.snapshot()
        a.delete('x'); a.merge(stale)
        self.assertEqual(a.visible(), {})
        self.assertEqual(len(a.snapshot()), 1)  # Deletion is retained in state.
        naive_gc = tuple(r for r in a.snapshot() if r.value is not None)
        resurrected = join_states(naive_gc, stale)
        self.assertEqual(resurrected[0].value, 'old')

    def test_invalid_or_conflicting_merge_is_atomic(self):
        a = Replica('A'); a.put('x', 'good')
        before, clock = a.snapshot(), a.clock.value
        for incoming in [(Record('x', 'evil', 1, 'A'),),
                         (Record('x', 'new', 2, 'B'), Record('', 'bad', 3, 'B')),
                         (Record('x', 'bad', True, 'B'),), ({'key': 'x'},)]:
            with self.assertRaises(ValueError): a.merge(incoming)
            self.assertEqual(a.snapshot(), before)
            self.assertEqual(a.clock.value, clock)
        with self.assertRaises(ValueError): a.put('', 'bad')
        self.assertEqual(a.snapshot(), before)
        self.assertEqual(a.clock.value, clock)

    def test_bounds_immutable_snapshot_and_clock_overflow(self):
        a = Replica('A'); a.put('x', 'good')
        self.assertIsInstance(a.snapshot(), tuple)
        with self.assertRaises(Exception): a.snapshot()[0].value = 'bad'
        clock = LogicalClock(MAX_COUNTER-1)
        with self.assertRaises(ValueError): clock.event()
        self.assertEqual(clock.value, MAX_COUNTER-1)
        with self.assertRaises(ValueError): Replica('')


if __name__ == '__main__': unittest.main(verbosity=2)
