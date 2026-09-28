import unittest,importlib.util,pathlib,itertools
P=pathlib.Path(__file__).parents[1]/"solution.py"; s=importlib.util.spec_from_file_location("sol",P); m=importlib.util.module_from_spec(s); s.loader.exec_module(m)
class T(unittest.TestCase):
 def test(self):
  for n in range(7):
   for a in itertools.product([-1,0,1],repeat=n):
    e=[i for i in range(n) if sum(a[:i])==sum(a[i+1:])]; self.assertEqual(m.equilibrium_indices(list(a)),e)
if __name__=="__main__": unittest.main()
