from pathlib import Path
import importlib.util,unittest
p=Path(__file__).resolve().parents[1]/"solution.py"
spec=importlib.util.spec_from_file_location("reference",p);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
solve=module.solve
class ContractTests(unittest.TestCase):
    def test_fixed_contract(self):
        self.assertEqual(solve(1,10),10); self.assertEqual(solve(2,10),4); self.assertEqual(solve(2,100),14); self.assertEqual(solve(5,0),0)
if __name__=="__main__":unittest.main(verbosity=2)
