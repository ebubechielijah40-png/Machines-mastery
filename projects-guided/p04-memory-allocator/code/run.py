import json,pathlib,platform,shutil,subprocess,tempfile
BASE=pathlib.Path(__file__).resolve().parent

def run():
 cc=shutil.which('cc')
 if not cc:raise RuntimeError('BLOCKED: C compiler unavailable')
 records=[]
 with tempfile.TemporaryDirectory(prefix='mm-arena-') as td:
  for i,flags in enumerate([['-O0'],['-O2'],['-O1','-fsanitize=undefined','-fno-sanitize-recover=all']]):
   exe=str(pathlib.Path(td)/str(i))
   for cmd in [[cc,'-std=c11','-Wall','-Wextra','-Werror',*flags,str(BASE/'arena.c'),str(BASE/'test_arena.c'),'-o',exe],[exe]]:
    p=subprocess.run(cmd,text=True,capture_output=True,timeout=15);records.append(dict(command=cmd,exit_code=p.returncode,stdout=p.stdout,stderr=p.stderr))
    if p.returncode:raise RuntimeError(records[-1])
 return dict(kind='actual C arena tests; no replacement of process malloc',platform=platform.platform(),records=records)
if __name__=='__main__':print(json.dumps(run(),indent=2))
