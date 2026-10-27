"""Synthetic policy/MMU models plus actual owned file/pipe/subprocess observations."""
import json,os,pathlib,platform,subprocess,sys,tempfile
from models import Job,schedule,AddressSpace,Fault

def investigate():
 jobs=[Job('A',0,5),Job('B',1,2),Job('C',2,1)]
 policies={p:schedule(jobs,p,2) for p in ['fcfs','rr']}
 sweep=[{'quantum':q,'switch_cost':1,'result':schedule([Job('A',0,8),Job('B',0,8),Job('C',0,8)],quantum=q,switch_cost=1)} for q in [1,2,4,8]]
 vm=AddressSpace();vm.map(2,7,'r');vmobs=[vm.translate(0x2d),vm.translate(0x2e)]
 try:vm.translate(0x2d,'w')
 except Fault as e:vmobs.append({'fault':e.kind})
 vm.map(2,9);vmobs.append(vm.translate(0x2d))
 with tempfile.TemporaryDirectory(prefix='mm-fd-') as td:
  p=pathlib.Path(td)/'owned.txt';p.write_bytes(b'abcdef')
  fd=os.open(p,os.O_RDONLY);dup=os.dup(fd);independent=os.open(p,os.O_RDONLY)
  try:offset={'original_read':os.read(fd,2).decode(),'duplicate_read':os.read(dup,2).decode(),'separate_open_read':os.read(independent,2).decode(),'shared_offset':os.lseek(fd,0,os.SEEK_CUR)}
  finally:
   for f in [fd,dup,independent]:os.close(f)
  r,w=os.pipe();extra=os.dup(w);os.close(w);os.set_blocking(r,False)
  try:
   try:os.read(r,1);held='unexpected read'
   except BlockingIOError:held='would block: another writer descriptor remains open'
   os.close(extra);extra=None;eof=os.read(r,1)==b''
  finally:
   os.close(r)
   if extra is not None:os.close(extra)
  before=os.getcwd()
  child=subprocess.run([sys.executable,'-c','import os,sys; print(os.getcwd()); sys.exit(7)'],cwd=td,capture_output=True,text=True,timeout=5)
  process={'child_pid_is_separate':'API-spawned child; PID not used as correctness oracle','requested_child_cwd':td,'child_stdout':child.stdout,'child_returncode':child.returncode,'parent_cwd_unchanged':os.getcwd()==before}
 return {'kind':'model outputs and separately labeled actual local OS observations','environment':{'python':sys.version,'platform':platform.platform()},'scheduling_model':policies,'quantum_overhead_model':sweep,'translation_model':vmobs,'actual_duplicate_descriptor':offset,'actual_pipe':{'while_duplicate_writer_open':held,'eof_after_last_writer_closed':eof},'actual_subprocess':process}
if __name__=='__main__':print(json.dumps(investigate(),indent=2))
