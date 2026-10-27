"""Bounded local command runner with original lexer and pipeline lifecycle.

Not POSIX shell syntax, not a sandbox. Execute only locally authorized programs.
No variable/glob/command expansion, job control, redirection or shell=True.
"""
from dataclasses import dataclass
from pathlib import Path
import subprocess,tempfile,time,math


def parse(line):
 if not isinstance(line,str) or len(line)>4096:raise ValueError('line must have at most 4096 characters')
 commands=[];argv=[];word=[];active=False;quote=None;escape=False
 def finish_word():
  nonlocal active,word
  if active:argv.append(''.join(word));word=[];active=False
 def finish_command():
  nonlocal argv
  finish_word()
  if not argv or not argv[0] or len(argv)>128:raise ValueError('empty command or too many arguments')
  commands.append(argv);argv=[]
  if len(commands)>8:raise ValueError('at most eight commands')
 for char in line:
  if escape:word.append(char);active=True;escape=False;continue
  if quote=="'":
   if char=="'":quote=None
   else:word.append(char)
   continue
  if char=='\\':escape=True;active=True;continue
  if quote=='"':
   if char=='"':quote=None
   else:word.append(char)
   continue
  if char in {'"',"'"}:quote=char;active=True
  elif char=='|':finish_command()
  elif char.isspace():finish_word()
  else:word.append(char);active=True
 if quote or escape:raise ValueError('unfinished quote or escape')
 finish_word()
 if argv:finish_command()
 elif commands:raise ValueError('pipeline ends with empty command')
 return commands

@dataclass(frozen=True)
class Result:
 stdout:bytes
 stderr:tuple[bytes,...]
 returncodes:tuple[int,...]


def run_pipeline(commands,*,cwd=None,input_bytes=b'',timeout=3,max_output=1<<20):
 if not isinstance(commands,list):raise ValueError('commands must be a list')
 if not commands:return Result(b'',(),())
 if len(commands)>8 or any(not isinstance(c,list) or not c or len(c)>128 or any(not isinstance(a,str) or '\0' in a for a in c) or not c[0] for c in commands):raise ValueError('invalid argv pipeline')
 if not isinstance(input_bytes,bytes) or len(input_bytes)>1<<20:raise ValueError('bounded byte input required')
 if isinstance(timeout,bool) or not isinstance(timeout,(int,float)) or not math.isfinite(timeout) or timeout<=0 or timeout>60:raise ValueError('timeout in (0,60]')
 if type(max_output) is not int or not 0<=max_output<=1<<20:raise ValueError('output memory cap in [0,1MiB]')
 processes=[];errors=[];files=[];deadline=time.monotonic()+timeout;previous=None
 try:
  inp=tempfile.TemporaryFile();files.append(inp);inp.write(input_bytes);inp.seek(0)
  output=tempfile.TemporaryFile();files.append(output)
  for i,argv in enumerate(commands):
   err=tempfile.TemporaryFile();files.append(err);errors.append(err)
   process=subprocess.Popen(argv,stdin=inp if previous is None else previous.stdout,stdout=output if i==len(commands)-1 else subprocess.PIPE,stderr=err,cwd=cwd,shell=False,close_fds=True)
   processes.append(process)
   if previous is not None:previous.stdout.close()
   previous=process
  for process in processes:process.wait(timeout=max(0.001,deadline-time.monotonic()))
  output.seek(0);data=output.read(max_output+1)
  if len(data)>max_output:raise ValueError('captured output exceeds memory cap')
  stderr=[]
  for err in errors:err.seek(0);stderr.append(err.read(65536))
  return Result(data,tuple(stderr),tuple(p.returncode for p in processes))
 finally:
  for process in processes:
   if process.poll() is None:process.kill()
  for process in processes:
   process.wait()
   if process.stdout is not None:process.stdout.close()
  for f in files:f.close()

class Shell:
 def __init__(self,cwd=None):self.cwd=Path(cwd or Path.cwd()).resolve()
 def execute(self,line,**kwargs):
  commands=parse(line)
  if any(c[0]=='cd' for c in commands):
   if len(commands)!=1 or len(commands[0])!=2:raise ValueError('cd needs one path and cannot appear in a pipeline')
   p=(self.cwd/commands[0][1]).resolve()
   if not p.is_dir():raise NotADirectoryError(str(p))
   self.cwd=p;return Result(b'',(),(0,))
  return run_pipeline(commands,cwd=self.cwd,**kwargs)


def main():
 """Run one bounded command line; use Shell for persistent logical cwd."""
 import argparse,sys
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('-c','--command',required=True)
 parser.add_argument('--input',default='',help='UTF-8 input for the first process')
 parser.add_argument('--cwd',default=None)
 parser.add_argument('--timeout',type=float,default=3)
 args=parser.parse_args()
 try:
  result=Shell(args.cwd).execute(args.command,input_bytes=args.input.encode(),timeout=args.timeout)
 except (ValueError,OSError,subprocess.TimeoutExpired) as error:
  print(f'minishell: {error}',file=sys.stderr);return 2
 sys.stdout.buffer.write(result.stdout)
 for data in result.stderr:sys.stderr.buffer.write(data)
 code=result.returncodes[-1] if result.returncodes else 0
 return 128-code if code<0 else code


if __name__=='__main__':raise SystemExit(main())
