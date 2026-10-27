import unittest,importlib.util,pathlib,math
p=pathlib.Path(__file__).parents[1]/"solution.py"
spec=importlib.util.spec_from_file_location("reference",p);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
class ContractTest(unittest.TestCase):
 def test_worked_contract(self):
  got=module.solve([[1,2],[3],[3],[]],0,3);expected=[0,1,3]
  self.assertEqual(got,expected)
if __name__=="__main__":unittest.main()
