import unittest,importlib.util,pathlib,itertools
P=pathlib.Path(__file__).parents[1]/"solution.py"; s=importlib.util.spec_from_file_location("sol",P); m=importlib.util.module_from_spec(s); s.loader.exec_module(m)
class T(unittest.TestCase):
 def test(self):
  for a in [[],[1],[1,3],[2,2]]:
   for b in [[],[0],[2],[2,4]]:
    aa=sorted(a)+[None]*len(b); e=sorted(a+b); self.assertEqual(m.merge_into_buffer(aa,len(a),sorted(b)),e)
if __name__=="__main__": unittest.main()
