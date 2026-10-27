#!/usr/bin/env python3
"""Replay the current reference/test contracts and save exact command evidence.

Core failures fail the command. Missing optional compilers are BLOCKED, not PASS.
Educational incompleteness remains separately visible in quality_audit.py.
"""
import argparse
import datetime
import json
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report-dir', type=Path, default=Path('research/quality/latest-verification'))
    args = parser.parse_args()
    destination = (ROOT/args.report_dir).resolve()
    if not destination.is_relative_to(ROOT):
        parser.error('report directory must remain inside the repository')
    destination.mkdir(parents=True, exist_ok=True)
    py = sys.executable
    commands = [
        ('structure',[py,'tools/validate.py'],None),
        ('publication',[py,'tools/check_publication.py'],None),
        ('infrastructure',[py,'-m','unittest','discover','-s','tools/tests','-v'],None),
        ('render-drift',[py,'tools/render.py','--check'],None),
        ('strong-dashboard',[py,'tools/strong_dashboard.py','--check'],None),
        ('expansion',[py,'tools/validate_expansion.py'],None),
        ('reference-groups',[py,'tools/run_reference_tests.py'],None),
        ('independent-boundaries',[py,'research/quality/2026-10-23/review_boundaries.py','--require-repaired'],None),
        ('programming-reader',[py,'research/quality/2026-10-25-continuous/programming-reader-probe.py'],None),
        ('protected-history',[py,'security-cryptography-mastery/provenance/run_protected.py'],None),
        ('native-systems',[py,'04-computer-systems/abi-loading/run_native.py'],'cc'),
        ('c-parser',[py,'programming-languages-mastery/01-c/units/01-byte-parser/tests/run.py'],'cc'),
        ('compile-link',[py,'-m','unittest','discover','-s','04-computer-systems/compile-link','-v'],'cc'),
        ('c-arena',[py,'projects-guided/p04-memory-allocator/code/run.py'],'cc'),
        ('c-synchronization',[py,'05-operating-systems/synchronization/code/experiment.py'],'cc'),
        ('cpp-lifetime',[py,'programming-languages-mastery/02-cpp/units/resource-lifetime/run.py'],'g++'),
        ('riscv-assembler',[py,'programming-languages-mastery/07-riscv-assembly/units/01-addi/tests/run.py'],'riscv64-linux-gnu-as'),
        ('riscv-model',[py,'programming-languages-mastery/07-riscv-assembly/units/01-addi/tests/run.py',
            'AddiTests.test_fixed_words_and_trace','AddiTests.test_all_immediates_arithmetic','AddiTests.test_negative_contract'],None),
        ('hidden-state',[py,'-m','unittest','discover','-s','reverse-engineering-systems/exercises/01-hidden-state/tests','-v'],None),
        ('git-whitespace',['git','diff','--check'],None),
        ('git-index-whitespace',['git','diff','--cached','--check'],None),
    ]
    # The registry identifies exact exemplar paths; do not invent tool locations.
    catalog = json.loads((ROOT/'registries/catalog.json').read_text())
    lessons = {x['id']:x['path'] for x in catalog['lessons']}
    if 'U-SVEX' in lessons:
        commands.append(('systemverilog',[py,lessons['U-SVEX']+'/tests/run.py'],'iverilog'))
    if 'U-PROD' in lessons:
        commands.append(('production-ledger',[py,'-m','unittest','discover','-s',lessons['U-PROD']+'/tests','-v'],None))
    for label, path in [('production-cluster','production-systems-engineering/labs/distributed-cluster'),
                         ('production-serving','production-systems-engineering/labs/model-serving')]:
        commands.append((label,[py,'-m','unittest','discover','-s',path+'/tests','-v'],None))
    commands.extend([
        ('binary-records',[py,'-m','unittest','discover','-s','reverse-engineering-systems/exercises/02-binary-records','-v'],'cc'),
        ('rust-ownership',[py,'programming-languages-mastery/03-rust/units/ownership-transfer/run.py'],'rustc'),
        ('zig-allocators',[py,'programming-languages-mastery/04-zig/units/allocator-errors/run.py'],'zig'),
        ('go-cancellation',[py,'programming-languages-mastery/09-go/units/channels-cancellation/run.py'],'go'),
        ('java-lifetimes',[py,'programming-languages-mastery/10-java/units/objects-resources-threads/run.py'],'java'),
        ('fifo-systemverilog',[py,'hardware-description-languages/fifo-contract/run.py','--language','sv'],'iverilog'),
        ('fifo-vhdl',[py,'hardware-description-languages/fifo-contract/run.py','--language','vhdl'],'ghdl'),
    ])
    records=[]
    for name, command, tool in commands:
        started = datetime.datetime.now(datetime.timezone.utc).isoformat()
        record={'name':name,'command':command,'cwd':str(ROOT),'started_at_utc':started}
        if name in {'git-whitespace','git-index-whitespace','publication'} and not (ROOT/'.git').exists():
            record.update(status='BLOCKED',exit_code=None,reason='source archive has no Git metadata; use bundle checkout for this check')
        elif tool and not shutil.which(tool):
            record.update(status='BLOCKED',exit_code=None,reason=f'optional toolchain unavailable: {tool}')
        else:
            begin=time.monotonic()
            try:
                p=subprocess.run(command,cwd=ROOT,text=True,capture_output=True,timeout=180)
                log=p.stdout+p.stderr
                # Version-pinned native runners can discover an incompatible or
                # incomplete toolchain after PATH lookup. Preserve that boundary.
                try:
                    runner_result=json.loads(p.stdout)
                except (ValueError, TypeError):
                    runner_result={}
                blocked=p.returncode==2 and runner_result.get('status')=='BLOCKED'
                no_tests='Ran 0 tests' in log or 'NO TESTS RAN' in log
                record.update(status='BLOCKED' if blocked else ('PASS' if p.returncode==0 and not no_tests else 'FAIL'),
                              exit_code=p.returncode,duration_seconds=round(time.monotonic()-begin,3))
                if no_tests: record['reason']='test discovery executed zero tests'
                if blocked: record['reason']=runner_result.get('reason','native runner reports unavailable toolchain')
            except subprocess.TimeoutExpired as exc:
                log=str(exc);record.update(status='FAIL',exit_code=124,reason='180 second timeout')
            log_path=destination/(name+'.txt')
            log_path.write_text(log)
            record['log']=str(log_path.relative_to(ROOT))
        records.append(record)
        print(json.dumps(record),flush=True)
    report={'schema_version':1,'python':sys.version,'platform':platform.platform(),
            'results':records,'limitations':'PASS covers specified test contracts, not educational completeness or learner mastery.'}
    (destination/'results.json').write_text(json.dumps(report,indent=2)+'\n')
    return int(any(x['status']=='FAIL' for x in records))


if __name__=='__main__': raise SystemExit(main())
