import unittest,importlib.util,pathlib,itertools
P=pathlib.Path(__file__).parents[1]/"solution.py"; s=importlib.util.spec_from_file_location("sol",P); m=importlib.util.module_from_spec(s); s.loader.exec_module(m)
def oracle(a):
 if a==sorted(a): return (-1,-1)
 target=sorted(a); d=[i for i,(x,y) in enumerate(zip(a,target)) if x!=y]; return (d[0],d[-1])
class T(unittest.TestCase):
 def test(self):
  for n in range(7):
   for a in itertools.product(range(3),repeat=n): self.assertEqual(m.minimal_sort_window(list(a)),oracle(list(a)))
if __name__=="__main__": unittest.main()
