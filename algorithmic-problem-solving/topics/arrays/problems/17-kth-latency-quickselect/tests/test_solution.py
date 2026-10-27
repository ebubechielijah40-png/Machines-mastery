import unittest,importlib.util,pathlib,itertools
P=pathlib.Path(__file__).parents[1]/"solution.py"; s=importlib.util.spec_from_file_location("sol",P); m=importlib.util.module_from_spec(s); s.loader.exec_module(m)
class T(unittest.TestCase):
 def test_adversarial_comparison_count(self):
  class Counted:
   comparisons=0
   def __init__(self,value): self.value=value
   def __le__(self,other):
    Counted.comparisons+=1
    return self.value<=other.value
  for n in [8,16,32]:
   for values in [list(range(n)), [1]*n]:
    Counted.comparisons=0
    result=m.kth_smallest([Counted(x) for x in values],0)
    self.assertEqual(result.value,min(values))
    self.assertEqual(Counted.comparisons,n*(n-1)//2)
 def test(self):
  for n in range(1,7):
   for a in itertools.product(range(3),repeat=n):
    for k in range(n): self.assertEqual(m.kth_smallest(list(a),k),sorted(a)[k])
 def test_bad(self):
  with self.assertRaises(IndexError):m.kth_smallest([1],1)
if __name__=="__main__": unittest.main()
