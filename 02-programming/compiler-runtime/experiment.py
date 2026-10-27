"""Controlled actual compiler/runtime observations; stdout or create-only file."""
import argparse
from dataclasses import asdict
import dis
import hashlib
import json
from pathlib import Path
import platform
import sys
from flow import (Instruction as I,Program,Machine,RuntimeFault,VerificationError,
                  compile_source,verify,disassemble)


def host_sum(n):
    total=0
    i=0
    while i<n:
        total=total+i
        i=i+1
    return total


def run():
    curves=[]
    for n in (0,1,2,5,10,30):
        program=compile_source(f'let i=0;let s=0;while(i<{n}){{s=s+i;i=i+1;}}print s;')
        state=Machine(program).run()
        assert state.output==(n*(n-1)//2,) and state.steps==13*n+11
        curves.append(dict(n=n,output=list(state.output),executed_instructions=state.steps,
                           static_instructions=len(program.code),maximum_stack=verify(program)['max_stack']))
    worked_source='let x=2+3*4;if(x<15){print x;}else{print 0;}'
    worked_program=compile_source(worked_source)
    worked_machine=Machine(worked_program);trace=[asdict(worked_machine.state)]
    while not worked_machine.state.halted:trace.append(asdict(worked_machine.step()))
    logic=compile_source('let i=0;let s=0;while(i<5){s=s+i;i=i+2;}print s;')
    incorrect=Machine(logic).run()
    assert incorrect.output==(6,) and incorrect.output!=(10,)
    mutant=Program((I('CONST',1),I('JZ',4),I('CONST',9),I('JUMP',4),I('HALT')),())
    try:verify(mutant)
    except VerificationError as error:join_rejection=str(error)
    else:raise AssertionError('join mutant accepted')
    failure_source='let x=8;print x;x=x/(x-8);'
    failed=Machine(compile_source(failure_source))
    try:failed.run()
    except RuntimeFault as error:failure=dict(message=str(error),offset=error.offset,state=asdict(error.state))
    else:raise AssertionError('division failure not observed')
    infinite=Machine(compile_source('while(1){}'),budget=17)
    try:infinite.run()
    except RuntimeFault as error:fuel=dict(message=str(error),state=asdict(error.state))
    else:raise AssertionError('fuel bound not enforced')
    here=Path(__file__).resolve().parent
    return dict(environment=dict(python=sys.version,implementation=sys.implementation.name,platform=platform.platform()),
                source_sha256={name:hashlib.sha256((here/name).read_bytes()).hexdigest() for name in ('flow.py','experiment.py')},
                counted_loop=curves,worked_source=worked_source,worked_disassembly=disassemble(worked_program),
                worked_trace=trace,accepted_wrong_algorithm=dict(result=list(incorrect.output),proof=verify(logic)),
                malformed_join_rejected=join_rejection,division_fault=failure,infinite_loop_budget=fuel,
                host_comparison=dict(result_at5=host_sum(5),opnames=[i.opname for i in dis.get_instructions(host_sum)]),
                limitations='Deterministic finite educational workloads. Instruction counts are not host timing, CPU instructions or a universal compiler proof. No hostile-code sandbox or learner mastery.')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path)
    args=parser.parse_args();text=json.dumps(run(),indent=2)+'\n'
    if args.output:
        with args.output.open('x') as stream:stream.write(text)
    else:print(text,end='')
