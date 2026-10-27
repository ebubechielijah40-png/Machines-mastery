"""Actual bounded traces, independent of host-language source evaluation."""
import hashlib,json,platform,sys
from pathlib import Path
from binding_lab import *


def program_late():
    return (Let('tag', Literal('registry')), Block((
        Function('inspect', (), (Print(Name('tag')),)),
        Expression(Call(Name('inspect'))), Let('tag', Literal('block')),
        Expression(Call(Name('inspect'))))))


def program_counter():
    return (Function('factory', (), (Let('count', Literal(0)),
        Function('increment', (), (Expression(Assign('count', Add(Name('count'), Literal(1)))),
                                     Return(Name('count')))), Return(Name('increment')))),
        Let('left', Call(Name('factory'))), Let('right', Call(Name('factory'))),
        Print(Call(Name('left'))), Print(Call(Name('right'))), Print(Call(Name('left'))))


if __name__=='__main__':
    here=Path(__file__).resolve().parent
    observations=[]
    for label,builder in [('late declaration',program_late),('independent closure factories',program_counter)]:
        program=compile_program(builder())
        for mode in ('resolved','mutable-chain'):
            observations.append({'experiment':label,**program.run(lookup=mode)})
    static=[]
    for label,body in [('unreachable own initializer',(If(Literal(False),Block((Let('x',Name('x')),)),Block(())),)),
                       ('top-level return',(Return(Literal(0)),))]:
        try:compile_program(body);static.append({'case':label,'rejected':False})
        except BindingError as exc:static.append({'case':label,'rejected':True,'message':str(exc)})
    print(json.dumps({'kind':'actual original AST-language execution; not original Lox benchmarking',
        'environment':{'python':sys.version,'platform':platform.platform()},
        'code_sha256':hashlib.sha256((here/'binding_lab.py').read_bytes()).hexdigest(),
        'observations':observations,'static_checks':static},indent=2))
