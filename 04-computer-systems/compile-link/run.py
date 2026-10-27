"""Compile/run owned C, retain real symbols/relocations/disassembly as JSON."""
import json, pathlib, platform, shutil, subprocess, sys, tempfile
BASE=pathlib.Path(__file__).resolve().parent

def investigate():
    cc=shutil.which('cc')
    if not cc: raise RuntimeError('BLOCKED: C compiler unavailable')
    records=[]
    def command(args, expected=0):
        p=subprocess.run(args,text=True,capture_output=True,timeout=20)
        records.append({'command':args,'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr})
        if expected==0 and p.returncode: raise RuntimeError(records[-1])
        if expected=='failure' and not p.returncode: raise AssertionError('missing-symbol link unexpectedly succeeded')
        return p
    version=command([cc,'--version']).stdout
    with tempfile.TemporaryDirectory(prefix='mm-compile-') as td:
        d=pathlib.Path(td); source=BASE/'code'
        for opt in ['-O0','-O2']:
            prefix=d/opt[1:]; prefix.mkdir()
            common=[cc,'-std=c11','-Wall','-Wextra','-Werror',opt]
            command(common+['-c',str(source/'main.c'),'-o',str(prefix/'main.o')])
            command(common+['-c',str(source/'sum.c'),'-o',str(prefix/'sum.o')])
            for tool,args in [('nm',['-P']),('objdump',['-dr']),('readelf',['-Wr'])]:
                exe=shutil.which(tool)
                if exe:
                    command([exe,*args,str(prefix/'main.o')])
                    if tool=='objdump': command([exe,*args,str(prefix/'sum.o')])
            command(common+[str(prefix/'main.o'),'-o',str(prefix/'missing')],expected='failure')
            command(common+[str(prefix/'main.o'),str(prefix/'sum.o'),'-o',str(prefix/'program')])
            output=command([str(prefix/'program')]).stdout
            assert output=='sum=15 calls=1 affine=17\n',output
            command(common+[str(source/'test_sum.c'),str(source/'sum.c'),'-o',str(prefix/'test')])
            command([str(prefix/'test')])
        command([cc,'-std=c11','-Wall','-Wextra','-Werror','-O1','-fsanitize=undefined','-fno-sanitize-recover=all',str(source/'test_sum.c'),str(source/'sum.c'),'-o',str(d/'sanitized')])
        command([str(d/'sanitized')])
    return {'kind':'actual local compiler/process investigation','python':sys.version,'platform':platform.platform(),'compiler':version,'records':records,'limits':'Only owned safe code executed; no ABI specification access or universal instruction/address claims.'}

if __name__=='__main__':print(json.dumps(investigate(),indent=2))
