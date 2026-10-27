from collections import Counter
from itertools import permutations
import random
import unittest

from task_publication import Publication, word_counts


class PublicationTests(unittest.TestCase):
    def test_all_completion_orders_match_sequential_oracle(self):
        shards = {'s0': ['red red', 'blue'], 's1': ['blue green', '']}
        oracle = dict(Counter('red red blue blue green'.split()))
        attempts = [('s0', 'a'), ('s0', 'b'), ('s1', 'c'), ('s1', 'd')]
        for order in permutations(attempts):
            job = Publication(shards)
            accepted = [job.publish(task, attempt, word_counts(shards[task]))
                        for task, attempt in order]
            self.assertEqual(sum(accepted), 2)
            self.assertEqual(job.reduce(), oracle)

    def test_seeded_shards_and_attempt_retries(self):
        rng = random.Random(2004)
        for _ in range(50):
            shards = {str(i): [' '.join(rng.choices(['x', 'y', 'z'], k=rng.randrange(12)))]
                      for i in range(rng.randrange(1, 8))}
            oracle = Counter()
            for records in shards.values():
                oracle.update(' '.join(records).split())
            attempts = [(t, f'{t}/{i}') for t in shards for i in range(3)]
            rng.shuffle(attempts)
            job = Publication(shards)
            for task, attempt in attempts:
                job.publish(task, attempt, word_counts(shards[task]))
            self.assertEqual(job.reduce(), dict(oracle))

    def test_crash_before_publication_and_snapshot_isolation(self):
        job = Publication(['s0', 's1'])
        with self.assertRaises(RuntimeError):
            job.reduce()
        # The first s0 execution crashes and never invokes publish.
        output = {'x': 2}
        self.assertTrue(job.publish('s0', 'retry', output))
        output['x'] = 999
        snapshot = job.accepted
        snapshot['s0']['x'] = 500
        job.publish('s1', 'other', {})
        self.assertEqual(job.reduce(), {'x': 2})

    def test_replay_contract_and_non_deterministic_counterexample(self):
        job = Publication(['s0'])
        self.assertTrue(job.publish('s0', 'a', {'x': 1}))
        self.assertFalse(job.publish('s0', 'a', {'x': 1}))
        with self.assertRaises(ValueError):
            job.publish('s0', 'a', {'x': 2})
        self.assertFalse(job.publish('s0', 'b', {'x': 2}))
        other = Publication(['s0'])
        other.publish('s0', 'b', {'x': 2})
        self.assertNotEqual(job.reduce(), other.reduce())

    def test_invalid_inputs(self):
        for tasks in [[], ['s', 's'], [''], [True]]:
            with self.assertRaises(ValueError):
                Publication(tasks)
        for output in [{'x': -1}, {'x': True}, {'x': 1.5}, {'a b': 2}, {'': 1}, []]:
            with self.assertRaises(ValueError):
                Publication(['s']).publish('s', 'a', output)
        with self.assertRaises(ValueError):
            Publication(['s']).publish('other', 'a', {})
        with self.assertRaises(ValueError):
            word_counts(['valid', 5])
        self.assertEqual(word_counts(['', ' a\tb a\n']), {'a': 2, 'b': 1})


if __name__ == '__main__':
    unittest.main()
