"""Causal graph oracle and adversarial traces; no distributed clock needed."""
import itertools
import random
import unittest

from logical_clocks import Event, graph, happened_before, stamp, total_order, violations


def delayed_trace():
    return [Event('a','A'),Event('b','A'),Event('s','A','send','m','B'),
            Event('r','B','receive','m','A'),Event('c','B'),Event('u','C')]


class ClockTests(unittest.TestCase):
    def test_worked_trace_and_nonconverse(self):
        events=delayed_trace()
        values=stamp(events)
        self.assertEqual(values,{'a':1,'b':2,'s':3,'r':4,'c':5,'u':1})
        self.assertFalse(violations(events,values))
        relation=happened_before(events)
        self.assertIn(('a','c'),relation)
        self.assertNotIn(('u','c'),relation)
        self.assertNotIn(('c','u'),relation)
        self.assertLess(values['u'],values['c'])  # smaller is not proof of causality

    def test_independent_transitive_closure_known_case(self):
        events=[Event('a','A','send','m','B'),Event('b','B','receive','m','A'),Event('c','B')]
        self.assertEqual(happened_before(events),frozenset({('a','b'),('b','c'),('a','c')}))

    def test_two_broken_receivers_fail_different_conditions(self):
        events=delayed_trace()
        for rule in ['ignore-message','non-strict']:
            values=stamp(events,rule)
            self.assertIn(('s','r'),violations(events,values))
        self.assertLess(stamp(events,'ignore-message')['r'],stamp(events,'ignore-message')['s'])
        self.assertEqual(stamp(events,'non-strict')['r'],stamp(events,'non-strict')['s'])

    def test_total_order_is_linear_extension_not_extra_causality(self):
        events=delayed_trace();values=stamp(events);order=total_order(events,values)
        positions={name:i for i,name in enumerate(order)}
        for a,b in happened_before(events):self.assertLess(positions[a],positions[b])
        self.assertIn('u',order)
        with self.assertRaises(ValueError):total_order(events,stamp(events,'ignore-message'))

    def test_all_small_schedule_interleavings(self):
        # All interleavings of two local chains with one matching message.
        a=[Event('a0','A'),Event('s','A','send','m','B'),Event('a2','A')]
        b=[Event('b0','B'),Event('r','B','receive','m','A'),Event('b2','B')]
        checked=0
        for positions in itertools.combinations(range(6),3):
            ia=ib=0;events=[]
            for index in range(6):
                if index in positions:events.append(a[ia]);ia+=1
                else:events.append(b[ib]);ib+=1
            if events.index(a[1])>events.index(b[1]):continue
            self.assertFalse(violations(events,stamp(events)))
            checked+=1
        self.assertGreater(checked,1)

    def test_random_traces_against_graph_reachability(self):
        rng=random.Random(71978)
        for trial in range(80):
            events=[];pending=[]
            for i in range(30):
                if pending and rng.random()<.45:
                    m,sender,recipient=pending.pop(rng.randrange(len(pending)))
                    events.append(Event(f'e{i}',recipient,'receive',m,sender))
                elif rng.random()<.5:
                    sender,recipient=rng.sample(['A','B','C'],2);m=f'm{trial}-{i}'
                    events.append(Event(f'e{i}',sender,'send',m,recipient))
                    pending.append((m,sender,recipient))
                else:events.append(Event(f'e{i}',rng.choice(['A','B','C'])))
            self.assertFalse(violations(events,stamp(events)))

    def test_invalid_traces_fail_before_timestamping(self):
        cases=[[Event('x','A'),Event('x','B')],
               [Event('x','A','receive','missing','B')],
               [Event('x','A','send','m','B'),Event('y','C','receive','m','A')],
               [Event('x','A','send','m','B'),Event('y','A','send','m','B')],
               [Event('x','A','local','m','B')],
               [Event('x','', 'local')],
               [Event('x','A','bad')]]
        for events in cases:
            with self.subTest(events=events),self.assertRaises(ValueError):stamp(events)

    def test_empty_undelivered_and_exact_timestamp_contracts(self):
        self.assertEqual(stamp([]),{})
        self.assertEqual(total_order([],{}),[])
        self.assertEqual(stamp([Event('x','A','send','m','B')]),{'x':1})
        with self.assertRaises(ValueError):violations([Event('x','A')],{})
        with self.assertRaises(ValueError):violations([Event('x','A')],{'x':True})


if __name__=='__main__':unittest.main(verbosity=2)
