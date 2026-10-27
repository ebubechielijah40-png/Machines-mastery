"""Reference-free short-input oracle plus boundary and reconstruction checks."""
import itertools
import unittest

from alignment import align_global, align_local, score_alignment


def path_scores(a, b, match, mismatch, gap):
    """Enumerate every column path directly; deliberately no DP or memoization."""
    if not a and not b:
        yield 0
    if a and b:
        for score in path_scores(a[1:], b[1:], match, mismatch, gap):
            yield score + (match if a[0] == b[0] else mismatch)
    if a:
        for score in path_scores(a[1:], b, match, mismatch, gap):
            yield score + gap
    if b:
        for score in path_scores(a, b[1:], match, mismatch, gap):
            yield score + gap


def brute_global(a, b, *scores):
    return max(path_scores(a, b, *scores))


def brute_local(a, b, *scores):
    # Independent definition: every pair of contiguous intervals, every path.
    return max([0] + [brute_global(a[i:j], b[k:l], *scores)
                      for i in range(len(a) + 1) for j in range(i, len(a) + 1)
                      for k in range(len(b) + 1) for l in range(k, len(b) + 1)])


def words(max_length):
    return [''.join(p) for n in range(max_length + 1)
            for p in itertools.product('AC', repeat=n)]


class AlignmentTests(unittest.TestCase):
    def assert_reconstructs(self, a, b, result, scores):
        self.assertEqual(result.a_aligned.replace('-', ''), a[slice(*result.a_span)])
        self.assertEqual(result.b_aligned.replace('-', ''), b[slice(*result.b_span)])
        self.assertEqual(score_alignment(result.a_aligned, result.b_aligned, *scores), result.score)
        self.assertEqual(len(result.a_aligned), len(result.b_aligned))
        self.assertEqual(result.cells_evaluated, len(a) * len(b))

    def test_global_exhaustive_independent_oracle(self):
        # 15*15*3 = 675 sequence/scoring cases, all column paths up to length 6.
        for scores in [(1, -1, -1), (2, -3, -1), (1, 0, 0)]:
            for a, b in itertools.product(words(3), repeat=2):
                with self.subTest(a=a, b=b, scores=scores):
                    r = align_global(a, b, *scores)
                    self.assertEqual(r.score, brute_global(a, b, *scores))
                    self.assertEqual(r.a_span, (0, len(a)))
                    self.assertEqual(r.b_span, (0, len(b)))
                    self.assert_reconstructs(a, b, r, scores)

    def test_local_exhaustive_independent_oracle(self):
        # 7*7*3 = 147 cases; small size limits exponential oracle cost.
        for scores in [(1, -1, -1), (2, -3, -1), (1, 0, 0)]:
            for a, b in itertools.product(words(2), repeat=2):
                with self.subTest(a=a, b=b, scores=scores):
                    r = align_local(a, b, *scores)
                    self.assertEqual(r.score, brute_local(a, b, *scores))
                    self.assert_reconstructs(a, b, r, scores)

    def test_worked_matrix_and_traceback(self):
        r = align_global('AG', 'ACG', 2, -1, -2)
        self.assertEqual(r.table, ((0, -2, -4, -6), (-2, 2, 0, -2), (-4, 0, 1, 2)))
        self.assertEqual((r.score, r.a_aligned, r.b_aligned), (2, 'A-G', 'ACG'))

    def test_local_flanks_and_coordinates(self):
        r = align_local('TTACGTAA', 'GGACGTCC', 2, -3, -2)
        self.assertEqual((r.score, r.a_span, r.b_span), (8, (2, 6), (2, 6)))
        self.assert_reconstructs('TTACGTAA', 'GGACGTCC', r, (2, -3, -2))

    def test_ties_have_documented_selection(self):
        r = align_global('AA', 'A')
        self.assertEqual((r.a_aligned, r.b_aligned), ('AA', '-A'))
        r = align_local('A', 'AA')
        self.assertEqual(r.b_span, (0, 1))

    def test_empty_and_no_positive_local_alignment(self):
        self.assertEqual(align_global('', 'AC').score, -2)
        self.assertEqual(align_local('', 'AC').score, 0)
        r = align_local('AAA', 'CCC')
        self.assertEqual((r.score, r.a_aligned, r.b_aligned, r.a_span), (0, '', '', (0, 0)))

    def test_symmetry_scores_not_necessarily_tracebacks(self):
        for a, b in [('AGT', 'AT'), ('AA', 'A'), ('', 'AA')]:
            for method in (align_global, align_local):
                self.assertEqual(method(a, b).score, method(b, a).score)

    def test_gap_model_can_prefer_two_gaps_over_mismatch(self):
        r = align_global('A', 'C', 2, -5, -1)
        self.assertEqual(r.score, -2)
        self.assertEqual(score_alignment(r.a_aligned, r.b_aligned, 2, -5, -1), -2)

    def test_input_and_resource_contracts(self):
        for method in (align_global, align_local):
            for kwargs in [dict(gap=1), dict(match=1.0), dict(gap=True), dict(max_cells=0),
                           dict(max_cells=3), dict(max_cells=True)]:
                with self.subTest(method=method.__name__, kwargs=kwargs), self.assertRaises(ValueError):
                    method('A', 'A', **kwargs)
            with self.assertRaises(ValueError): method('A-', 'A')
            with self.assertRaises(ValueError): method(None, 'A')
        with self.assertRaises(ValueError): score_alignment('A', '')
        with self.assertRaises(ValueError): score_alignment('-', '-')


if __name__ == '__main__':
    unittest.main(verbosity=2)
