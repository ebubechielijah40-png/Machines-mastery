"""Execute with: python3 -m unittest discover -s 16-machine-learning/labs -v"""
import math
import unittest
from attention import causal_attention, identity, matvec, softmax

class AttentionTests(unittest.TestCase):
    def setUp(self):
        self.tokens = [[1.,0.], [0.,1.], [1.,1.]]
        self.i = identity(2)

    def test_projection(self):
        self.assertEqual(matvec([2, 3], [[1,2],[4,5]]), [14,19])

    def test_causal_mask(self):
        outputs, rows = causal_attention(self.tokens,self.i,self.i,self.i)
        self.assertEqual(len(outputs),3)
        for t, row in enumerate(rows):
            self.assertAlmostEqual(sum(row),1)
            self.assertEqual(row[t+1:],[0.]*(len(rows)-t-1))

    def test_first_position_only_self(self):
        outputs, rows = causal_attention(self.tokens,self.i,self.i,self.i)
        self.assertEqual(outputs[0],self.tokens[0]); self.assertEqual(rows[0],[1.,0.,0.])

    def test_no_lookahead_leakage(self):
        original,_ = causal_attention(self.tokens,self.i,self.i,self.i)
        mutated = [row[:] for row in self.tokens]; mutated[-1]=[999,-999]
        changed,_ = causal_attention(mutated,self.i,self.i,self.i)
        self.assertEqual(original[:-1],changed[:-1])

    def test_softmax_stable_large_scores(self):
        w=softmax([10000,10001]); self.assertTrue(all(math.isfinite(x) for x in w))
        self.assertAlmostEqual(sum(w),1)
        self.assertGreater(w[1],w[0])

    def test_scale_changes_concentration(self):
        x = [[1.,0.],[1.,1.]]
        _,scaled=causal_attention(x,self.i,self.i,self.i,scale=True)
        _,unscaled=causal_attention(x,self.i,self.i,self.i,scale=False)
        self.assertNotEqual(scaled[1],unscaled[1])

    def test_invalid_dimensions(self):
        with self.assertRaises(ValueError):
            causal_attention(self.tokens,[[1]],self.i,self.i)
        with self.assertRaises(ValueError):
            causal_attention([[1.], [1.,2.]],[[1.]],[[1.]],[[1.]])

    def test_bad_scores(self):
        with self.assertRaises(ValueError): softmax([float('inf'), 1.])

if __name__=='__main__': unittest.main()
