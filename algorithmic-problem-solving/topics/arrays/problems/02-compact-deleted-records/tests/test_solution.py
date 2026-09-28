import unittest,importlib.util,pathlib,random
P=pathlib.Path(__file__).parents[1]/"solution.py"; s=importlib.util.spec_from_file_location("sol",P); m=importlib.util.module_from_spec(s); s.loader.exec_module(m)
class T(unittest.TestCase):
 def test_cases(self):
  for a in [[],[None,None],[3,None,4,None,5],[0,None,"",2]]:
   orig=a[:]; live=[x for x in orig if x is not None]; k=m.compact_active(a); self.assertEqual(k,len(live)); self.assertEqual(a,live+[None]*(len(orig)-len(live)))
if __name__=="__main__": unittest.main()
