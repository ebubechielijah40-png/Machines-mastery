"""Independent deque vectors, actual VHDL/SystemVerilog, two semantic mutants."""
from collections import deque
from datetime import datetime,timezone
import argparse,hashlib,itertools,json,os,platform,random,shutil,subprocess,tempfile
from pathlib import Path
BASE=Path(__file__).resolve().parent


def vectors():
    queue=deque();rows=[]
    def apply(reset,push,pop,data):
        if reset:queue.clear()
        else:
            consumed=bool(pop and queue)
            if consumed:queue.popleft()
            if push and len(queue)<3:queue.append(data)
        rows.append((reset,push,pop,data,len(queue),queue[0] if queue else 0))
    # Reset plus every short binary-valued queue/input contract, not every RTL state.
    for length in range(4):
        for contents in itertools.product(range(2),repeat=length):
            for push,pop,data in itertools.product(range(2),repeat=3):
                apply(1,0,0,0)
                for value in contents:apply(0,1,0,value)
                apply(0,push,pop,data)
                for _ in range(4):apply(0,0,1,0)
    rng=random.Random(6221)
    for _ in range(2000):apply(int(rng.randrange(31)==0),rng.randrange(2),rng.randrange(2),rng.randrange(16))
    return rows


def run(language='all'):
    needed={'sv':['iverilog','vvp'],'vhdl':['ghdl']}
    selected=('sv','vhdl') if language=='all' else (language,)
    missing=[x for name in selected for x in needed[name] if not shutil.which(x)]
    if missing:raise RuntimeError('BLOCKED: missing tools '+','.join(missing))
    rows=vectors();records=[]
    def command(args,cwd,expect_success=True,marker=None):
        p=subprocess.run(args,cwd=cwd,text=True,capture_output=True,timeout=40)
        record=dict(command=args,exit_code=p.returncode,stdout=p.stdout,stderr=p.stderr,expected_success=expect_success)
        records.append(record)
        if (expect_success and p.returncode) or (not expect_success and p.returncode==0):raise RuntimeError(record)
        if marker and marker not in p.stdout+p.stderr:raise RuntimeError('intended assertion/marker not observed')
    for name in selected:
        command([shutil.which('iverilog' if name=='sv' else 'ghdl'),'-V' if name=='sv' else '--version'],BASE)
        for mutant in ('reference','no-full-replacement','wrong-count'):
            with tempfile.TemporaryDirectory(prefix='mm-fifo-') as directory:
                tmp=Path(directory);(tmp/'vectors.txt').write_text(''.join(' '.join(map(str,row))+'\n' for row in rows))
                source=(BASE/('fifo.sv' if name=='sv' else 'fifo.vhd')).read_text()
                if mutant=='no-full-replacement':source=source.replace(' || pop_fire','').replace(' or take_pop','')
                if mutant=='wrong-count':
                    source=source.replace('default: count<=count;','default: if (push_fire && pop_fire) count<=count-1;')
                    source=source.replace('elsif take_pop and not take_push then count<=count-1;', 'elsif take_pop then count<=count-1;')
                src=tmp/('fifo.sv' if name=='sv' else 'fifo.vhd');src.write_text(source)
                correct=mutant=='reference'
                if name=='sv':
                    command([shutil.which('iverilog'),'-g2012','-s','tb','-o','sim',str(src),str(BASE/'tb.sv')],tmp)
                    command([shutil.which('vvp'),'sim'],tmp,correct,'PASS:' if correct else 'queue transition mismatch')
                else:
                    command([shutil.which('ghdl'),'-a','--std=08',str(src),str(BASE/'tb.vhd')],tmp)
                    command([shutil.which('ghdl'),'-e','--std=08','tb'],tmp)
                    command([shutil.which('ghdl'),'-r','--std=08','tb','--assert-level=error'],tmp,correct,'PASS:' if correct else 'queue transition mismatch')
    return dict(executed_at_utc=datetime.now(timezone.utc).isoformat(),python=platform.python_version(),platform=platform.platform(),
                vector_count=len(rows),vector_sha256=hashlib.sha256(repr(rows).encode()).hexdigest(),
                code_sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in BASE.iterdir() if p.suffix in ('.py','.sv','.vhd')},records=records,
                scope='Actual logical simulation and intended negative controls; no physical timing, synthesis, CDC or all-state formal proof.')

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--language',choices=('all','sv','vhdl'),default='all');args=parser.parse_args()
    print(json.dumps(run(args.language),indent=2))
