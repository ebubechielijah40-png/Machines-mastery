import unittest,importlib.util,pathlib,itertools,math
P=pathlib.Path(__file__).parents[1]/"solution.py"; s=importlib.util.spec_from_file_location("sol",P); m=importlib.util.module_from_spec(s); s.loader.exec_module(m)
def oracle(a): return max(math.prod(a[i:j]) for i in range(len(a)) for j in range(i+1,len(a)+1))
class T(unittest.TestCase):
 def test_no_input_slicing_and_empty_rejection(self):
  class IndexOnly(list):
   def __getitem__(self,key):
    if isinstance(key,slice): raise AssertionError('would allocate an input-sized slice')
    return super().__getitem__(key)
  self.assertEqual(m.max_product_subarray(IndexOnly([-2,3,-4])),24)
  with self.assertRaises(ValueError): m.max_product_subarray([])
 def test(self):
  for n in range(1,7):
   for a in itertools.product([-2,-1,0,1,2],repeat=n): self.assertEqual(m.max_product_subarray(list(a)),oracle(a))
if __name__=="__main__": unittest.main()
