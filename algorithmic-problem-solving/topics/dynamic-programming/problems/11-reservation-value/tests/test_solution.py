from pathlib import Path
import importlib.util,unittest
p=Path(__file__).resolve().parents[1]/"solution.py"
spec=importlib.util.spec_from_file_location("reference",p);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
solve=module.solve
class ContractTests(unittest.TestCase):
    def test_fixed_contract(self):
        self.assertEqual(solve([(0,2,4),(2,4,5),(0,4,8)]),(9,(0,1))); self.assertEqual(solve([(0,1,-2)]),(0,())); self.assertEqual(solve([(0,4,100),(0,2,1),(2,4,1)])[0],100)
if __name__=="__main__":unittest.main(verbosity=2)
