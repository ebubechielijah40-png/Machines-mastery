import unittest,importlib.util,pathlib,itertools
P=pathlib.Path(__file__).parents[1]/"solution.py"; s=importlib.util.spec_from_file_location("sol",P); m=importlib.util.module_from_spec(s); s.loader.exec_module(m)
class T(unittest.TestCase):
 def test(self):
  for n in range(7):
   for a in itertools.product([0,1,2],repeat=n):
    e=[x for x in a if x!=0]+[0]*sum(x==0 for x in a); self.assertEqual(m.move_zeros(list(a)),e)
if __name__=="__main__": unittest.main()
