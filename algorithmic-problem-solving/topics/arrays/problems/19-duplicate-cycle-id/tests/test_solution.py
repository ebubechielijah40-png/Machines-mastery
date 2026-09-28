import unittest,importlib.util,pathlib,itertools
P=pathlib.Path(__file__).parents[1]/"solution.py"; s=importlib.util.spec_from_file_location("sol",P); m=importlib.util.module_from_spec(s); s.loader.exec_module(m)
class T(unittest.TestCase):
 def test_generated(self):
  for n in range(2,8):
   base=list(range(1,n+1))
   for dup in range(1,n+1):
    a=base+[dup]; got=m.find_duplicate(a); self.assertIn(got,{x for x in a if a.count(x)>1})
 def test_examples(self): self.assertEqual(m.find_duplicate([1,3,4,2,2]),2)
if __name__=="__main__": unittest.main()
