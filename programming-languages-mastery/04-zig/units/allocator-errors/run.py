"""Pinned Zig0.13 native allocator/error and negative-control tests."""
import argparse,datetime,json,os,platform,shutil,subprocess,tempfile
from pathlib import Path
BASE=Path(__file__).resolve().parent

def run(compiler=None):
    compiler=compiler or os.environ.get('ZIG') or shutil.which('zig')
    if not compiler:return dict(status='BLOCKED',reason='Zig0.13 unavailable; set ZIG to a trusted installed compiler',commands=[])
    records=[]
    with tempfile.TemporaryDirectory(prefix='mm-zig-') as temporary:
        def execute(suffix):
            command=[compiler,*suffix]
            p=subprocess.run(command,text=True,capture_output=True,cwd=temporary,timeout=120)
            records.append(dict(command=command,exit_code=p.returncode,stdout=p.stdout,stderr=p.stderr));return p
        p=execute(['version'])
        if p.returncode or p.stdout.strip()!='0.13.0':return dict(status='BLOCKED',reason='unit is pinned to Zig0.13.0; other standard-library APIs not validated',commands=records)
        for mode in ['Debug','ReleaseSafe']:
            p=execute(['test',str(BASE/'packet.zig'),'-O',mode,'--cache-dir',str(Path(temporary)/'cache')])
            if p.returncode or 'All 6 tests passed' not in p.stdout+p.stderr:raise AssertionError(records[-1])
        p=execute(['test',str(BASE/'broken.zig'),'--cache-dir',str(Path(temporary)/'cache')])
        if not p.returncode or 'MemoryLeakDetected' not in p.stderr:raise AssertionError(records[-1])
        binary=Path(temporary)/'experiment'
        p=execute(['build-exe',str(BASE/'packet.zig'),'-O','ReleaseSafe','-femit-bin='+str(binary),'--cache-dir',str(Path(temporary)/'cache')])
        if p.returncode:raise AssertionError(records[-1])
        p=subprocess.run([str(binary)],text=True,capture_output=True,timeout=10)
        records.append(dict(command=[str(binary)],exit_code=p.returncode,stdout=p.stdout,stderr=p.stderr))
        if p.returncode or 'budget=4;status=OutOfMemory;after_cleanup=0' not in p.stderr:raise AssertionError(records[-1])
    return dict(status='PASS',observed_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),platform=platform.platform(),commands=records,limits='Zig0.13 byte allocations and scoped error paths, not a borrow checker, all allocator behavior or safe arbitrary copied ownership.')

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--compiler');parser.add_argument('--output',type=Path);args=parser.parse_args();result=run(args.compiler);data=json.dumps(result,indent=2)+'\n'
    if args.output:args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(data)
    else:print(data,end='')
    raise SystemExit(0 if result['status']=='PASS' else 2)
