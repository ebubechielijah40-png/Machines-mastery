import unittest,importlib.util,pathlib,itertools
P=pathlib.Path(__file__).parents[1]/"solution.py"; s=importlib.util.spec_from_file_location("sol",P); m=importlib.util.module_from_spec(s); s.loader.exec_module(m)
def oracle(h):
 return sum(max(0,min(max(h[:i+1]),max(h[i:]))-h[i]) for i in range(len(h))) if h else 0
class T(unittest.TestCase):
 def test(self):
  for n in range(7):
   for h in itertools.product(range(3),repeat=n): self.assertEqual(m.trapped_water(list(h)),oracle(list(h)))
if __name__=="__main__": unittest.main()
