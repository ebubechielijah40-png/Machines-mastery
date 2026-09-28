import unittest,importlib.util,pathlib,itertools,math
P=pathlib.Path(__file__).parents[1]/"solution.py"; s=importlib.util.spec_from_file_location("sol",P); m=importlib.util.module_from_spec(s); s.loader.exec_module(m)
class T(unittest.TestCase):
 def test_exhaustive(self):
  for n in range(2,6):
   for a in itertools.product([-2,-1,0,1,2],repeat=n):
    e=[math.prod(a[:i]+a[i+1:]) for i in range(n)]; self.assertEqual(m.product_except_self(list(a)),e)
if __name__=="__main__": unittest.main()
