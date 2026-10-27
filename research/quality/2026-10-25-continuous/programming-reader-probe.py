"""Reader-selected matrix/gcd programs, Unicode fault map and late CFG join.

No eval/exec or compiler implementation is used to produce the output oracles.
The independent cases are chosen by a reviewer other than the Flow author.
"""
from dataclasses import asdict
import hashlib
import json
import math
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[3]
UNIT=ROOT/'02-programming/compiler-runtime'
sys.path.insert(0,str(UNIT))
import flow


def product(a,b):
    return tuple(tuple(sum(a[i][k]*b[k][j] for k in range(2)) for j in range(2)) for i in range(2))


def fib_matrix(n):
    result=((1,0),(0,1));base=((1,1),(1,0))
    while n:
        if n%2:result=product(result,base)
        base=product(base,base);n//=2
    return result[0][1]


def main():
    fibonacci=[]
    for n in range(24):
        source=f'let a=0;let b=1;let next=0;let i=0;while(i<{n}){{next=a+b;a=b;b=next;i=i+1;}}print a;'
        final=flow.Machine(flow.compile_source(source)).run()
        assert final.output==(fib_matrix(n),)
        fibonacci.append(final.output[0])
    gcd_cases=0
    for a in (-144,-31,-7,0,2,60,97):
        for b in (-99,-15,-1,1,8,42):
            source=f'let a={a};let b={b};let r=0;if(a<0){{a=-a;}}if(b<0){{b=-b;}}while(b){{r=a-(a/b)*b;a=b;b=r;}}print a;'
            final=flow.Machine(flow.compile_source(source)).run()
            assert final.output==(math.gcd(a,b),)
            gcd_cases+=1
    source='# λ\nlet x=2147483647;print x;x=x+1;'
    machine=flow.Machine(flow.compile_source(source))
    try:machine.run()
    except flow.RuntimeFault as error:
        fault=machine.state;offset=error.offset
        assert offset==source.index('+')
        byte_offset=len(source[:offset].encode('utf-8'));assert byte_offset==offset+1
        assert fault.locals==(2147483647,) and fault.output==(2147483647,) and fault.stack==(2147483647,1)
        try:machine.step()
        except flow.RuntimeFault:pass
        else:raise AssertionError('repeated overflow step succeeded')
        assert machine.state==fault
    else:raise AssertionError('overflow not raised')
    I=flow.Instruction
    # Long bypass reaches the earlier merge only after its initialized path can
    # have propagated. Removing init at this backward join must revisit LOAD0.
    code=(I('CONST',1),I('JZ',8),I('CONST',9),I('STORE',0),I('JUMP',6),
          I('HALT'),I('LOAD',0),I('PRINT'),I('JUMP',9),I('JUMP',10),
          I('JUMP',11),I('JUMP',12),I('JUMP',6),I('HALT'))
    try:flow.verify(flow.Program(code,('x',)))
    except flow.VerificationError as error:
        join_error=str(error);assert 'uninitialized' in join_error
    else:raise AssertionError('late uninitialized bypass accepted')
    # Worklist termination is independent of concrete program termination.
    infinite=flow.Program((I('JUMP',0),I('HALT')),())
    proof=flow.verify(infinite);bounded=flow.Machine(infinite,budget=7)
    try:bounded.run()
    except flow.RuntimeFault:assert bounded.state.steps==7 and not bounded.state.halted
    else:raise AssertionError('nontermination escaped fuel')
    print(json.dumps(dict(runtime=sys.version,source_sha256=hashlib.sha256((UNIT/'flow.py').read_bytes()).hexdigest(),
                         fibonacci_matrix_oracle=dict(cases=24,observed=fibonacci),
                         signed_euclidean_oracle=dict(cases=gcd_cases,all_agree_with_math_gcd=True),
                         atomic_overflow=dict(state=asdict(fault),character_offset=offset,utf8_byte_offset=byte_offset,repeated_step_unchanged=True),
                         late_backward_join_rejected=join_error,
                         verifier_terminates_on_loop=proof,actual_loop_fuel=bounded.state.steps,
                         limitations='Finite source/CFG/state probes. No general source equivalence, termination, native ABI, heap runtime or hostile-code isolation proof.'),indent=2))


if __name__=='__main__':main()
