"""Compile only supplied C/assembly; compare native observations and GNU tools."""
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess
import sys
import tempfile
from elf_plan import parse,materialize,read

HERE=Path(__file__).resolve().parent


def investigate():
    required=('cc','readelf','objdump','nm')
    missing=[name for name in required if shutil.which(name) is None]
    if platform.system()!='Linux' or platform.machine() not in ('x86_64','amd64') or missing:
        return dict(status='BLOCKED',reason='Linux x86-64 and cc/readelf/objdump/nm required',missing=missing)
    records=[];builds=[]
    with tempfile.TemporaryDirectory() as directory:
        destination=Path(directory)
        def execute(command,*,expected=0):
            result=subprocess.run(command,text=True,capture_output=True,timeout=30)
            records.append(dict(command=command,exit_code=result.returncode,stdout=result.stdout,stderr=result.stderr))
            if result.returncode!=expected:raise AssertionError(records[-1])
            return result.stdout
        compiler=execute(['cc','--version']).splitlines()[0]
        tools={name:execute([name,'--version']).splitlines()[0] for name in ('readelf','objdump','nm')}
        for name,flags in [('o0-exec',['-O0','-fno-pie','-no-pie']),('o2-exec',['-O2','-fno-pie','-no-pie']),('o2-pie',['-O2','-fPIE','-pie'])]:
            target=destination/name
            execute(['cc','-std=c11','-Wall','-Wextra','-Werror',*flags,str(HERE/'code/main.c'),str(HERE/'code/boundary.S'),'-o',str(target)])
            observed=json.loads(execute([str(target)]))
            assert observed==dict(weighted_cases=100,weighted_1_to_8=204,entry_alignment=0,good_preserves=1,mutant_preserves=0,pid_equal=1,raw_write=-9,libc_write=-1,libc_errno=9,bss_zero_sum=0,row_size=24,row_align=8,value_offset=8,code_offset=16)
            raw=target.read_bytes();bias=0x10000000 if name.endswith('pie') else 0
            plan=parse(raw,bias=bias);image=materialize(raw,plan)
            program_headers=execute(['readelf','-W','-l',str(target)])
            tool_segments=[]
            for line in program_headers.splitlines():
                cells=line.split()
                if cells and cells[0]=='LOAD':
                    flags_text=''.join(cells[6:-1]);flags=sum({'R':4,'W':2,'E':1}[x] for x in flags_text)
                    tool_segments.append((int(cells[1],16),int(cells[2],16),int(cells[4],16),int(cells[5],16),flags,int(cells[-1],16)))
            assert tool_segments==[(s.offset,s.virtual,s.file_size,s.memory_size,s.flags,s.alignment) for s in plan.segments]
            symbols=execute(['nm','-S',str(target)])
            symbol=next(line.split() for line in symbols.splitlines() if line.endswith(' zero_area'))
            zero_address,zero_size=int(symbol[0],16)+bias,int(symbol[1],16)
            assert zero_size==8192
            assert read(image,zero_address,4096)==bytes(4096)
            assert read(image,zero_address+4096,4096)==bytes(4096)
            disassembly=execute(['objdump','-d','--no-show-raw-insn',str(target)])
            assert '<weighted8>:' in disassembly and '<raw_write>:' in disassembly and 'syscall' in disassembly
            # Remove only section-table coordinates in a binary built above.
            # Program headers and segment contents remain unchanged.
            stripped=bytearray(raw)
            stripped[40:48]=bytes(8);stripped[58:64]=bytes(6)
            assert parse(bytes(stripped),bias=bias)==plan
            without_sections=destination/(name+'-no-sections');without_sections.write_bytes(stripped);without_sections.chmod(0o700)
            assert json.loads(execute([str(without_sections)]))==observed
            builds.append(dict(name=name,native=observed,elf_kind=plan.kind,entry_model=plan.entry,
                               bias=bias,interpreter=plan.interpreter,load_segments=[vars(s) for s in plan.segments],
                               zero_fill_bytes=sum(s.memory_size-s.file_size for s in plan.segments),
                               bss_symbol=dict(address=zero_address,size=zero_size),readelf_agreed=True,
                               section_table_removed_binary_still_ran=True))
        kvm=dict(path_present=Path('/dev/kvm').exists(),guest_executed=False,
                 meaning='Path presence is not accessibility/capability evidence; no KVM ioctl or guest was run.')
    return dict(status='PASS',environment=dict(python=sys.version,platform=platform.platform(),compiler=compiler,tools=tools),
                source_sha256={name:hashlib.sha256((HERE/name).read_bytes()).hexdigest() for name in ('code/main.c','code/boundary.S','elf_plan.py','memory_models.py','run_native.py')},
                builds=builds,records=records,kvm=kvm,
                limitations='Selected Linux SysV integer ABI and educational ELF subset. No all-ABI proof, dynamic linker, hardware cache measurement or virtual machine execution.')


if __name__=='__main__':
    report=investigate();print(json.dumps(report,indent=2));raise SystemExit(2 if report['status']=='BLOCKED' else 0)
