import unittest,importlib.util,pathlib,itertools
P=pathlib.Path(__file__).parents[1]/"solution.py"; s=importlib.util.spec_from_file_location("sol",P); m=importlib.util.module_from_spec(s); s.loader.exec_module(m)
class T(unittest.TestCase):
 def test_unique(self):
  for n in range(1,7):
   perms=list(itertools.permutations(range(n)))
   for idx,p in enumerate(perms):
    a=list(p); got=m.next_permutation(a); e=list(perms[(idx+1)%len(perms)]); self.assertEqual(a,e); self.assertEqual(got,idx<len(perms)-1)
 def test_duplicates(self):
  a=[1,1,2]; self.assertTrue(m.next_permutation(a)); self.assertEqual(a,[1,2,1])
if __name__=="__main__": unittest.main()
