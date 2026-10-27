import unittest,importlib.util,pathlib,math
p=pathlib.Path(__file__).parents[1]/"solution.py"
spec=importlib.util.spec_from_file_location("reference",p);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
class ContractTest(unittest.TestCase):
 def test_worked_contract(self):
  got=module.solve([[0,3,2,0],[0,0,1,2],[0,0,0,3],[0,0,0,0]],0,3);expected=(5,{0})
  self.assertEqual(got[0],expected[0]);self.assertEqual(got[1],expected[1])
if __name__=="__main__":unittest.main()
