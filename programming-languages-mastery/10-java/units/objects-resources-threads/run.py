"""Actual Java compile/execute/disassemble, using JDK modules when launchers are absent."""
import argparse,datetime,json,platform,shutil,subprocess,tempfile
from pathlib import Path
BASE=Path(__file__).resolve().parent

def run():
    java=shutil.which('java')
    if not java:return dict(status='BLOCKED',reason='java unavailable',commands=[])
    commands=[]
    def execute(command):
        result=subprocess.run(command,text=True,capture_output=True,timeout=30)
        record=dict(command=command,exit_code=result.returncode,stdout=result.stdout,stderr=result.stderr)
        commands.append(record)
        return result
    version=execute([java,'--version'])
    probe=execute([java,'com.sun.tools.javac.Main','-version'])
    if probe.returncode:return dict(status='BLOCKED',reason='JDK compiler module unavailable',commands=commands)
    with tempfile.TemporaryDirectory(prefix='mm-java-') as temporary:
        build=execute([java,'com.sun.tools.javac.Main','--release','17','-Xlint:all','-d',temporary,str(BASE/'LifetimeLab.java')])
        if build.returncode:raise AssertionError(commands[-1])
        for flags in ([],['-Xint']):
            result=execute([java,*flags,'-cp',temporary,'LifetimeLab'])
            if result.returncode or 'checks=15' not in result.stdout:raise AssertionError(commands[-1])
        bytecode=execute([java,'-m','jdk.jdeps/com.sun.tools.javap.Main','-c','-p','-classpath',temporary,'LifetimeLab$Packet'])
        if bytecode.returncode or 'arraylength' not in bytecode.stdout or 'clone' not in bytecode.stdout:raise AssertionError(commands[-1])
    return dict(status='PASS',observed_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),platform=platform.platform(),commands=commands,limits='Java17 selected contracts only; no GC timing, native assembly, throughput or all-memory-model outcomes claim.')

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path);args=parser.parse_args();result=run();data=json.dumps(result,indent=2)+'\n'
    if args.output:args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(data)
    else:print(data,end='')
    raise SystemExit(0 if result['status']=='PASS' else 2)
