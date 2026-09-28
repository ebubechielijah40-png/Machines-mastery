import unittest,importlib.util,pathlib,random
P=pathlib.Path(__file__).parents[1]/"solution.py"; s=importlib.util.spec_from_file_location("sol",P); m=importlib.util.module_from_spec(s); s.loader.exec_module(m)
def oracle(n,ups):
 a=[0]*n
 for l,r,d in ups:
  for i in range(l,r+1):a[i]+=d
 return a
class T(unittest.TestCase):
 def test_random(self):
  rnd=random.Random(0)
  for n in range(1,20):
   for _ in range(30):
    ups=[]
    for __ in range(rnd.randrange(10)):
     l=rnd.randrange(n); r=rnd.randrange(l,n); d=rnd.randrange(-5,6); ups.append((l,r,d))
    self.assertEqual(m.apply_range_deltas(n,ups),oracle(n,ups))
if __name__=="__main__": unittest.main()
