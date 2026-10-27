"""Bounded JSON driver around the original OS models, not a real kernel."""
import argparse,hashlib,json,pathlib,sys
ROOT=pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'05-operating-systems/code'))
from models import Job,schedule,AddressSpace,Fault

def execute(mode,payload):
 if mode not in {'schedule','translate'}:raise ValueError('unknown mode')
 if not isinstance(payload,dict):raise ValueError('JSON object required')
 if mode=='schedule':
  raw=payload.get('jobs',[])
  if not isinstance(raw,list) or len(raw)>32:raise ValueError('at most32 jobs')
  jobs=[Job(*row) for row in raw]
  if any(type(j.burst) is not int or not 1<=j.burst<=10000 or type(j.arrival) is not int or not 0<=j.arrival<=10000 for j in jobs) or sum(j.burst for j in jobs)>10000:raise ValueError('bounded time/service inputs required')
  return schedule(jobs,payload.get('policy','rr'),payload.get('quantum',2),payload.get('switch_cost',0))
 a=AddressSpace(payload.get('tlb_capacity',2));mappings=payload.get('mappings',[]);accesses=payload.get('accesses',[])
 if not isinstance(mappings,list) or len(mappings)>16 or not isinstance(accesses,list) or len(accesses)>100:raise ValueError('bounded mappings/accesses required')
 for row in mappings:a.map(*row)
 result=[]
 for row in accesses:
  try:result.append(a.translate(*row))
  except Fault as e:result.append({'fault':e.kind,'address':e.address})
 return result

def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('mode',choices=['schedule','translate']);args=parser.parse_args()
 try:
  raw=sys.stdin.buffer.read((1<<20)+1)
  if len(raw)>1<<20:raise ValueError('input exceeds1MiB')
  result=execute(args.mode,json.loads(raw))
 except (ValueError,TypeError,KeyError) as e:
  print(json.dumps({'error':str(e)}),file=sys.stderr)
  return 2
 print(json.dumps({'kind':'deterministic teaching model','input_sha256':hashlib.sha256(raw).hexdigest(),'result':result}));return 0
if __name__=='__main__':raise SystemExit(main())
