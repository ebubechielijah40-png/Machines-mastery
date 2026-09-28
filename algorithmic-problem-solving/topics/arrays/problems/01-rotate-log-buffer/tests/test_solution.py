import unittest,importlib.util,pathlib,random
P=pathlib.Path(__file__).parents[1]/"solution.py"; s=importlib.util.spec_from_file_location("sol",P); m=importlib.util.module_from_spec(s); s.loader.exec_module(m)
class T(unittest.TestCase):
 def test_examples(self):
  for a,k,e in [([],3,[]),([1],100,[1]),([1,2,3,4,5],2,[4,5,1,2,3]),([1,2,3],-1,[2,3,1])]: self.assertEqual(m.rotate_right(a,k),e)
 def test_oracle(self):
  for n in range(8):
   for k in range(-10,11):
    a=list(range(n)); e=a[-(k%n):]+a[:-(k%n)] if n and k%n else a[:]; self.assertEqual(m.rotate_right(a[:],k),e)
if __name__=="__main__": unittest.main()
