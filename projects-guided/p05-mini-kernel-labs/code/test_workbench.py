import json,pathlib,subprocess,sys,unittest
BASE=pathlib.Path(__file__).resolve().parent
class WorkbenchTests(unittest.TestCase):
 def run_case(self,mode,payload):
  return subprocess.run([sys.executable,str(BASE/'kernel_workbench.py'),mode],input=json.dumps(payload),text=True,capture_output=True,timeout=4)
 def test_schedule_complete_trace(self):
  p=self.run_case('schedule',{'jobs':[['A',0,5],['B',1,2],['C',2,1]],'quantum':2})
  self.assertEqual(p.returncode,0,p.stderr);r=json.loads(p.stdout)
  self.assertEqual(r['result']['metrics']['B']['finish'],4);self.assertEqual(len(r['input_sha256']),64)
 def test_translate_permissions_and_absence(self):
  p=self.run_case('translate',{'mappings':[[2,7,'r']],'accesses':[[45],[45,'w'],[64]]})
  self.assertEqual(p.returncode,0,p.stderr);r=json.loads(p.stdout)['result']
  self.assertEqual(r[0]['physical_address'],125);self.assertEqual(r[1]['fault'],'PROTECTION');self.assertEqual(r[2]['fault'],'NOT_PRESENT')
 def test_resource_and_invalid_boundaries(self):
  for payload in [{'jobs':[['A',0,10**20]]},{'jobs':[['A',0,1]],'quantum':0},[]]:
   p=self.run_case('schedule',payload);self.assertEqual(p.returncode,2);self.assertIn('error',json.loads(p.stderr))
if __name__=='__main__':unittest.main(verbosity=2)
