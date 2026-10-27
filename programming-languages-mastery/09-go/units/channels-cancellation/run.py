"""Compile/test original finite Go concurrency mechanism; no third-party modules."""
import argparse,datetime,json,os,platform,shutil,subprocess,tempfile
from pathlib import Path
BASE=Path(__file__).resolve().parent

def run(compiler=None):
    compiler=compiler or os.environ.get('GO') or shutil.which('go')
    if not compiler:return dict(status='BLOCKED',reason='Go compiler unavailable; set GO to a trusted installed go executable',commands=[])
    records=[]
    env=dict(os.environ,GOTOOLCHAIN='local',GOWORK='off',GOENV='off',GOMAXPROCS='2',CGO_ENABLED='1')
    with tempfile.TemporaryDirectory(prefix='mm-go-') as temporary:
        for name in ['go.mod','pipeline.go','pipeline_test.go']:shutil.copyfile(BASE/name,Path(temporary)/name)
        for suffix in [['version'],['test','-count=1','-v','./...'],['test','-race','-count=1','-v','./...'],['vet','./...']]:
            command=[compiler,*suffix]
            p=subprocess.run(command,cwd=temporary,env=env,capture_output=True,text=True,timeout=150)
            records.append(dict(command=command,exit_code=p.returncode,stdout=p.stdout,stderr=p.stderr))
            if p.returncode or ('test' in suffix and 'TestObservation' not in p.stdout):raise AssertionError(records[-1])
    return dict(status='PASS',observed_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),platform=platform.platform(),controlled_environment={k:env[k] for k in ['GOTOOLCHAIN','GOWORK','GOENV','GOMAXPROCS','CGO_ENABLED']},commands=records,limits='Finite Go channel/join/aliasing contracts and local race-detector run; not universal scheduler fairness, leak freedom, network cancellation or production reliability proof.')

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--compiler');parser.add_argument('--output',type=Path);args=parser.parse_args();result=run(args.compiler);data=json.dumps(result,indent=2)+'\n'
    if args.output:args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(data)
    else:print(data,end='')
    raise SystemExit(0 if result['status']=='PASS' else 2)
