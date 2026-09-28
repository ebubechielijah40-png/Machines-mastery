import unittest,importlib.util,pathlib,itertools
P=pathlib.Path(__file__).parents[1]/"solution.py"; s=importlib.util.spec_from_file_location("sol",P); m=importlib.util.module_from_spec(s); s.loader.exec_module(m)
class T(unittest.TestCase):
 def test(self):
  cases=[([],[]),([1],[]),([],[2]),([1,4,7],[2,2,9]),([-2,3],[-3,8])]
  for a,b in cases:self.assertEqual(m.merge_sorted(a,b),sorted(a+b))
if __name__=="__main__": unittest.main()
