"""Tests for algorithmic growth demonstrations and complexity models."""
import sys
import unittest
from pathlib import Path

GROWTH_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(GROWTH_DIR))

from benchmark import naive_duplicate, set_duplicate, tree_nodes, run


class GrowthTests(unittest.TestCase):
    def test_naive_duplicate_counts(self):
        values = list(range(10))
        has_dup, comps = naive_duplicate(values)
        self.assertFalse(has_dup)
        self.assertEqual(comps, 10 * 9 // 2)

        has_dup, comps = naive_duplicate([42, 42])
        self.assertTrue(has_dup)
        self.assertEqual(comps, 1)

    def test_set_duplicate_counts(self):
        values = list(range(10))
        has_dup, visits = set_duplicate(values)
        self.assertFalse(has_dup)
        self.assertEqual(visits, 10)

        has_dup, visits = set_duplicate([5, 5])
        self.assertTrue(has_dup)
        self.assertEqual(visits, 2)

    def test_tree_nodes_recursion(self):
        for d in (0, 1, 2, 4):
            self.assertEqual(tree_nodes(d), 2 ** (d + 1) - 1)

    def test_run_generates_valid_cases(self):
        data = run()
        self.assertEqual(data['kind'], 'agent bounded algorithm measurement; no learner evidence')
        self.assertTrue(len(data['cases']) > 0)
        case_names = {c['name'] for c in data['cases']}
        self.assertIn('constant_index', case_names)
        self.assertIn('binary_search', case_names)
        self.assertIn('quadratic_unique_check', case_names)
        self.assertIn('exponential_recursion', case_names)


if __name__ == '__main__':
    unittest.main()
