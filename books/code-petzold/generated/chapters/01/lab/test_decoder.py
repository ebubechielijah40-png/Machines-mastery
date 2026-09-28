"""Contract, independent duration formula, exhaustive small-domain checks."""
import itertools
import unittest
from decoder import decode, encode


class DecoderTests(unittest.TestCase):
    def test_hand_derived_traces(self):
        self.assertEqual(encode('AN', 2), [(1, 2), (0, 2), (1, 6), (0, 6),
                                          (1, 6), (0, 2), (1, 2)])
        self.assertEqual(decode([(1, 6), (0, 2), (1, 2), (0, 12), (1, 2)], 2), 'N E')
        self.assertEqual(sum(d for _, d in encode('E A')), 12)
        self.assertEqual(sum(d for _, d in encode('EA')), 9)

    def test_gap_corruption_is_valid_but_wrong(self):
        self.assertEqual(decode([(1, 1), (0, 1), (1, 3)]), 'A')
        self.assertEqual(decode([(1, 1), (0, 3), (1, 3)]), 'ET')
        self.assertEqual(decode([(1, 3), (0, 1), (1, 1)]), 'N')
        self.assertEqual(decode([(1, 3), (0, 3), (1, 1)]), 'TE')

    def test_empty_and_single(self):
        self.assertEqual(encode(''), [])
        self.assertEqual(decode([]), '')
        self.assertEqual(decode([(1, 1)]), 'E')
        self.assertEqual(decode([(1, 3)]), 'T')

    def test_small_domain_and_independent_cost(self):
        # 4^k letter sequences * 2^(k-1) choices of word boundaries.
        dots = {'E': 1, 'T': 0, 'A': 1, 'N': 1}
        dashes = {'E': 0, 'T': 1, 'A': 1, 'N': 1}
        for k in range(1, 5):
            for letters in itertools.product('ETAN', repeat=k):
                for gaps in itertools.product(('', ' '), repeat=k-1):
                    text = letters[0] + ''.join(g + c for g, c in zip(gaps, letters[1:]))
                    for tau in (1, 2, 7):
                        events = encode(text, tau)
                        self.assertEqual(decode(events, tau), text)
                        d = sum(dots[c] for c in letters)
                        h = sum(dashes[c] for c in letters)
                        w = 1 + text.count(' ')
                        self.assertEqual(sum(t for _, t in events),
                                         (2*d + 4*h + 2*k + 3*w - 6)*tau)

    def test_invalid_text(self):
        for text in ('a', 'E  T', ' E', 'E ', 'SOS', '\n', 42):
            with self.subTest(text=text), self.assertRaises(ValueError):
                encode(text)

    def test_invalid_events(self):
        invalid = [[(0, 1)], [(1, 1), (1, 3)], [(1, 2)],
                   [(1, 1), (0, 2), (1, 1)], [(1, 1), (0, 1)],
                   [(1, 1), (0, 1), (1, 1)], [(1, 0)], [(1, -1)],
                   [(1, 1.0)], [(True, 1)], [(1, True)], [(1,)],
                   [(2, 1)], ['bad']]
        for events in invalid:
            with self.subTest(events=events), self.assertRaises(ValueError):
                decode(events)
        with self.assertRaises(ValueError):
            decode([(1, 3)], 2)

    def test_tau_contract(self):
        for tau in (0, -1, True, 1.5, '1'):
            with self.subTest(tau=tau), self.assertRaises(ValueError):
                encode('E', tau)
            with self.subTest(tau=tau), self.assertRaises(ValueError):
                decode([], tau)

    def test_scale_ambiguity(self):
        self.assertEqual(decode([(1, 3)], 1), 'T')
        self.assertEqual(decode([(1, 3)], 3), 'E')


if __name__ == '__main__':
    unittest.main()
