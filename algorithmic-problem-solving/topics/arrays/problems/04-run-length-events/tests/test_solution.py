import unittest,importlib.util,pathlib,itertools
P=pathlib.Path(__file__).parents[1]/"solution.py"; s=importlib.util.spec_from_file_location("sol",P); m=importlib.util.module_from_spec(s); s.loader.exec_module(m)
class T(unittest.TestCase):
 def decode(self,r): return [x for x,c in r for _ in range(c)]
 def test(self):
  for n in range(7):
   for a in itertools.product([0,1],repeat=n):
    r=m.run_length_encode(list(a)); self.assertEqual(self.decode(r),list(a)); self.assertTrue(all(c>0 for _,c in r)); self.assertTrue(all(r[i][0]!=r[i+1][0] for i in range(len(r)-1)))
if __name__=="__main__": unittest.main()
