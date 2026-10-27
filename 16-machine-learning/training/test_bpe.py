import unittest
from bpe import BytePairTokenizer


class BPETests(unittest.TestCase):
    def test_roundtrip_unseen_unicode_and_deterministic_ties(self):
        a=BytePairTokenizer('abababab',4);b=BytePairTokenizer('abababab',4)
        self.assertEqual(a.merges,b.merges)
        for text in ['abababab','new β 你好','', 'a\x00b']:
            self.assertEqual(a.decode(a.encode(text)),text)
            self.assertEqual(a.decode(iter(a.encode(text))),text)
        self.assertLess(len(a.encode('abababab')),8)

    def test_nonoverlap_merge_and_invalid_ids(self):
        self.assertEqual(BytePairTokenizer.replace([1,1,1],(1,1),256),[256,1])
        with self.assertRaises(ValueError):BytePairTokenizer('x',-1)
        with self.assertRaises(ValueError):BytePairTokenizer('x').decode([True])


if __name__=='__main__':unittest.main()
