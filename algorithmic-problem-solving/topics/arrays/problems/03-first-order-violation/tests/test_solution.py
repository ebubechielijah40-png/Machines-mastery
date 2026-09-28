import unittest,importlib.util,pathlib,itertools
P=pathlib.Path(__file__).parents[1]/"solution.py"; s=importlib.util.spec_from_file_location("sol",P); m=importlib.util.module_from_spec(s); s.loader.exec_module(m)
class T(unittest.TestCase):
 def test_exhaustive(self):
  for n in range(6):
   for a in itertools.product(range(3),repeat=n):
    e=next((i for i in range(n-1) if a[i]>a[i+1]),-1); self.assertEqual(m.first_descent(list(a)),e)
if __name__=="__main__": unittest.main()
