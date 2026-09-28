import unittest,importlib.util,pathlib,itertools
P=pathlib.Path(__file__).parents[1]/"solution.py"; s=importlib.util.spec_from_file_location("sol",P); m=importlib.util.module_from_spec(s); s.loader.exec_module(m)
class T(unittest.TestCase):
 def test(self):
  for n in range(1,7):
   for a in itertools.product(range(3),repeat=n):
    for k in range(n): self.assertEqual(m.kth_smallest(list(a),k),sorted(a)[k])
 def test_bad(self):
  with self.assertRaises(IndexError):m.kth_smallest([1],1)
if __name__=="__main__": unittest.main()
