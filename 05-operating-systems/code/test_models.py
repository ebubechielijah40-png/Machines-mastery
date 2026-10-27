import itertools,random,unittest
from models import Job,schedule,AddressSpace,Fault
class SchedulingTests(unittest.TestCase):
 def test_worked_traces_and_metrics(self):
  jobs=[Job('A',0,5),Job('B',1,2),Job('C',2,1)]
  f=schedule(jobs,'fcfs');r=schedule(jobs,'rr',2)
  self.assertEqual(f['timeline'],[('A',0,5),('B',5,7),('C',7,8)])
  self.assertEqual(r['timeline'],[('A',0,2),('B',2,4),('C',4,5),('A',5,7),('A',7,8)])
  self.assertEqual(r['metrics']['B'],dict(response=1,turnaround=3,waiting=1,finish=4))
 def test_switch_cost_is_accounted_and_arrivals_precede_requeue(self):
  r=schedule([Job('A',0,2),Job('B',1,1)],quantum=1,switch_cost=1)
  self.assertEqual(r['timeline'],[('A',0,1),('SWITCH',1,2),('B',2,3),('SWITCH',3,4),('A',4,5)])
  self.assertEqual(r['metrics']['A']['waiting'],3)
 def test_idle_empty_and_one_job_no_spurious_switch(self):
  self.assertEqual(schedule([])['elapsed'],0)
  r=schedule([Job('A',3,4)],quantum=1,switch_cost=100)
  self.assertEqual(r['elapsed'],7);self.assertEqual(r['metrics']['A']['waiting'],0)
 def test_random_work_conservation_and_time_accounting(self):
  rng=random.Random(910)
  for _ in range(100):
   jobs=[Job(str(i),rng.randrange(8),rng.randrange(1,6)) for i in range(rng.randrange(1,8))]
   for policy in ['rr','fcfs']:
    r=schedule(jobs,policy,rng.randrange(1,4),rng.randrange(3))
    self.assertEqual(sum(e-s for _,s,e in r['timeline']),r['elapsed'])
    for j in jobs:
     self.assertEqual(sum(e-s for n,s,e in r['timeline'] if n==j.name),j.burst)
     self.assertGreaterEqual(r['metrics'][j.name]['response'],0)
     self.assertGreaterEqual(r['metrics'][j.name]['waiting'],0)
 def test_invalid_workloads(self):
  for jobs in [[Job('A',0,0)],[Job('A',-1,1)],[Job('A',0,1),Job('A',1,1)],[Job('IDLE',0,1)]]:
   with self.assertRaises(ValueError):schedule(jobs)
  for kwargs in [dict(quantum=0),dict(quantum=True),dict(switch_cost=-1),dict(policy='unknown')]:
   with self.assertRaises(ValueError):schedule([],**kwargs)
class TranslationTests(unittest.TestCase):
 def test_worked_address_tlb_dirty_and_protection(self):
  a=AddressSpace();a.map(2,7,'r')
  self.assertEqual(a.translate(0x2d),dict(physical_address=125,vpn=2,offset=13,tlb_hit=False))
  self.assertTrue(a.translate(0x2d)['tlb_hit'])
  with self.assertRaises(Fault) as c:a.translate(0x2d,'w')
  self.assertEqual(c.exception.kind,'PROTECTION');self.assertFalse(a.entry(2).dirty)
 def test_remap_invalidates_stale_translation_and_unmap_prunes(self):
  a=AddressSpace();a.map(2,7);a.translate(0x2d);a.map(2,9)
  self.assertEqual(a.translate(0x2d)['physical_address'],157)
  self.assertTrue(a.entry(2).accessed);a.translate(0x2d,'w');self.assertTrue(a.entry(2).dirty)
  a.unmap(2);self.assertEqual(a.directory,{})
  with self.assertRaises(Fault):a.translate(0x2d)
 def test_all_addresses_against_direct_map_oracle(self):
  a=AddressSpace(2)
  mapping={vpn:(vpn*7)%32 for vpn in range(16)}
  for vpn,pfn in mapping.items():a.map(vpn,pfn)
  for addr in range(256):self.assertEqual(a.translate(addr)['physical_address'],mapping[addr//16]*16+addr%16)
 def test_lru_and_address_space_isolation(self):
  a=AddressSpace(2);b=AddressSpace(0)
  for v in range(3):a.map(v,v+3)
  b.map(0,20);a.translate(0);a.translate(16);a.translate(0);a.translate(32)
  self.assertEqual(list(a.tlb),[0,2]);self.assertFalse(a.translate(16)['tlb_hit'])
  self.assertEqual(b.translate(0)['physical_address'],320)
 def test_supervisor_and_invalid_contract(self):
  a=AddressSpace();a.map(0,1,'rx',user=False)
  with self.assertRaises(Fault):a.translate(0)
  self.assertEqual(a.translate(0,user=False)['physical_address'],16)
  for addr in [-1,256,True]:
   with self.assertRaises(ValueError):a.translate(addr)
  with self.assertRaises(ValueError):a.map(0,32)
  with self.assertRaises(ValueError):AddressSpace(-1)
if __name__=='__main__':unittest.main(verbosity=2)
