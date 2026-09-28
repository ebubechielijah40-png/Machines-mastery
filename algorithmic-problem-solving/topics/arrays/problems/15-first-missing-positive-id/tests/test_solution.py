import unittest,importlib.util,pathlib,itertools
P=pathlib.Path(__file__).parents[1]/"solution.py"; s=importlib.util.spec_from_file_location("sol",P); m=importlib.util.module_from_spec(s); s.loader.exec_module(m)
def oracle(a):
 s=set(a); x=1
 while x in s:x+=1
 return x
class T(unittest.TestCase):
 def test(self):
  vals=[-1,0,1,2,3]
  for n in range(6):
   for a in itertools.product(vals,repeat=n): self.assertEqual(m.first_missing_positive(list(a)),oracle(a))
if __name__=="__main__": unittest.main()
