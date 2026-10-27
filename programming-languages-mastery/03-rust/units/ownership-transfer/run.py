"""Compile and run original Rust mechanisms; check deliberately rejected programs."""
import argparse,datetime,json,os,platform,shutil,subprocess,tempfile
from pathlib import Path
BASE=Path(__file__).resolve().parent

def run(compiler=None):
    compiler=compiler or os.environ.get('RUSTC') or shutil.which('rustc')
    if not compiler:return dict(status='BLOCKED',reason='rustc unavailable; set RUSTC to a trusted installed compiler',commands=[])
    records=[]
    def execute(command):
        p=subprocess.run(command,text=True,capture_output=True,timeout=60)
        records.append(dict(command=command,exit_code=p.returncode,stdout=p.stdout,stderr=p.stderr));return p
    version=execute([compiler,'--version','--verbose'])
    if version.returncode:raise AssertionError(records[-1])
    with tempfile.TemporaryDirectory(prefix='mm-rust-') as temporary:
        for label,flags in [('debug',[]),('optimized',['-O'])]:
            output=str(Path(temporary)/label)
            p=execute([compiler,'--edition=2021','--test','-C','overflow-checks=yes',*flags,str(BASE/'lab.rs'),'-o',output])
            if p.returncode:raise AssertionError(records[-1])
            p=execute([output,'--test-threads=1'])
            if p.returncode or '8 passed' not in p.stdout:raise AssertionError(records[-1])
        for name,code in [('moved','E0382'),('overlap','E0502'),('dangling','E0515')]:
            p=execute([compiler,'--edition=2021',str(BASE/'compile-fail'/f'{name}.rs'),'-o',str(Path(temporary)/name)])
            if not p.returncode or code not in p.stderr:raise AssertionError(records[-1])
        output=str(Path(temporary)/'experiment')
        p=execute([compiler,'--edition=2021',str(BASE/'lab.rs'),'-o',output])
        if p.returncode:raise AssertionError(records[-1])
        p=execute([output])
        if p.returncode or 'move_preserved_buffer=true;sum=528;length=33' not in p.stdout:raise AssertionError(records[-1])
    return dict(status='PASS',observed_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),platform=platform.platform(),commands=records,limits='Selected safe Rust2021 mechanisms, no complete Rust/unsafe/ABI or optimizer performance claim; recorded Vec capacity policy is implementation evidence.')

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--compiler');parser.add_argument('--output',type=Path);args=parser.parse_args();result=run(args.compiler);data=json.dumps(result,indent=2)+'\n'
    if args.output:args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(data)
    else:print(data,end='')
    raise SystemExit(0 if result['status']=='PASS' else 2)
