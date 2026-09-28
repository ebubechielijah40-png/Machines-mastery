import unittest,importlib.util,pathlib,itertools
P=pathlib.Path(__file__).parents[1]/"solution.py"; s=importlib.util.spec_from_file_location("sol",P); m=importlib.util.module_from_spec(s); s.loader.exec_module(m)
def oracle(a):
 n=len(a); return max(sum(a[(i+t)%n] for t in range(L)) for i in range(n) for L in range(1,n+1))
class T(unittest.TestCase):
 def test(self):
  for n in range(1,6):
   for a in itertools.product([-2,-1,0,1,2],repeat=n): self.assertEqual(m.max_circular_subarray_sum(list(a)),oracle(a))
if __name__=="__main__": unittest.main()
