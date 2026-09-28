import unittest,importlib.util,pathlib,itertools
P=pathlib.Path(__file__).parents[1]/"solution.py"; s=importlib.util.spec_from_file_location("sol",P); m=importlib.util.module_from_spec(s); s.loader.exec_module(m)
class T(unittest.TestCase):
 def test(self):
  for n in range(8):
   for a in itertools.product([0,1,2],repeat=n): self.assertEqual(m.dutch_flag(list(a)),sorted(a))
 def test_bad(self):
  with self.assertRaises(ValueError):m.dutch_flag([0,3])
if __name__=="__main__": unittest.main()
