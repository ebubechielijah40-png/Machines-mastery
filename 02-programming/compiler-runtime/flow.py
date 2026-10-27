"""Original bounded compiler, control-flow verifier and step debugger.

The Flow language is defined in README.md. No eval/exec/host source compiler is
used. This is an inspectable teaching machine, not a hostile-code sandbox.
"""
from collections import deque
from dataclasses import dataclass
import re

MIN_INT=-(2**31)
MAX_INT=2**31-1
MAX_SOURCE=8192
MAX_TOKENS=2048
MAX_CODE=4096
MAX_LOCALS=64
MAX_STACK=64
MAX_DEPTH=32
KEYWORDS={'let','print','if','else','while'}


class SourceError(ValueError):
    def __init__(self,message,offset):
        self.offset=offset
        super().__init__(f'{message} at source character offset {offset}')


class VerificationError(ValueError):pass


class RuntimeFault(ValueError):
    def __init__(self,message,state,offset):
        self.state,self.offset=state,offset
        super().__init__(f'{message} at pc {state.pc}, source character offset {offset}')


@dataclass(frozen=True)
class Instruction:
    op:str
    arg:object=None
    offset:int=0


@dataclass(frozen=True)
class Program:
    code:tuple
    names:tuple
    source:str=''


@dataclass(frozen=True)
class Snapshot:
    pc:int
    stack:tuple
    locals:tuple
    output:tuple
    steps:int
    halted:bool


def _integer(value):return type(value) is int and MIN_INT<=value<=MAX_INT


def trunc_div(left,right):
    """Internal integer quotient toward zero without a float conversion."""
    if right==0:raise ZeroDivisionError('division by zero')
    magnitude=abs(left)//abs(right)
    return -magnitude if (left<0)!=(right<0) else magnitude


def _tokens(source):
    if type(source) is not str:raise TypeError('source must be text')
    if len(source)>MAX_SOURCE:raise SourceError('source exceeds8192 characters',MAX_SOURCE)
    pattern=re.compile(r'\s+|#[^\n]*|[0-9]+|[A-Za-z_][A-Za-z_0-9]*|==|[+*/<={}();-]')
    result=[];position=0
    while position<len(source):
        match=pattern.match(source,position)
        if match is None:raise SourceError('unrecognized character',position)
        text=match.group()
        if not text.isspace() and not text.startswith('#'):
            if len(result)>=MAX_TOKENS:raise SourceError('source exceeds2048 tokens',position)
            if text[0].isdigit():
                if len(text)>10 or int(text)>MAX_INT:raise SourceError('literal outside nonnegative signed32 range',position)
            elif text[0].isalpha() or text[0]=='_':
                if len(text)>64:raise SourceError('identifier exceeds64 characters',position)
            result.append((text,position))
        position=match.end()
    result.append(('<eof>',len(source)));return result


class _Compiler:
    def __init__(self,source):
        self.source,self.tokens=source,_tokens(source)
        self.index=0;self.code=[];self.names=[];self.slots={}
    def peek(self):return self.tokens[self.index][0]
    def take(self,expected=None):
        token=self.tokens[self.index]
        if expected is not None and token[0]!=expected:raise SourceError('expected '+repr(expected),token[1])
        if token[0]=='<eof>':raise SourceError('unexpected end of source',token[1])
        self.index+=1;return token
    def identifier(self):
        name,offset=self.take()
        if re.fullmatch(r'[A-Za-z_][A-Za-z_0-9]*',name) is None or name in KEYWORDS:
            raise SourceError('expected non-keyword identifier',offset)
        return name,offset
    def emit(self,op,arg=None,offset=0):
        if len(self.code)>=MAX_CODE:raise SourceError('code exceeds4096 instructions',offset)
        self.code.append(Instruction(op,arg,offset));return len(self.code)-1
    def patch(self,pc,target):
        old=self.code[pc];self.code[pc]=Instruction(old.op,target,old.offset)
    def slot(self,name,offset):
        if name not in self.slots:raise SourceError('name used before declaration: '+name,offset)
        return self.slots[name]
    def expression(self,depth=0,minimum=0):
        if depth>MAX_DEPTH:raise SourceError('expression nesting exceeds32',self.tokens[self.index][1])
        token,offset=self.take()
        if token=='-':self.expression(depth+1,4);self.emit('NEG',offset=offset)
        elif token=='(':
            self.expression(depth+1);self.take(')')
        elif token[0].isdigit():self.emit('CONST',int(token),offset)
        elif re.fullmatch(r'[A-Za-z_][A-Za-z_0-9]*',token) and token not in KEYWORDS:
            self.emit('LOAD',self.slot(token,offset),offset)
        else:raise SourceError('expected expression',offset)
        precedence={'==':1,'<':1,'+':2,'-':2,'*':3,'/':3}
        operators={'==':'EQ','<':'LT','+':'ADD','-':'SUB','*':'MUL','/':'DIV'}
        while self.peek() in precedence and precedence[self.peek()]>=minimum:
            op,where=self.take();self.expression(depth+1,precedence[op]+1)
            self.emit(operators[op],offset=where)
    def block(self,depth):
        if depth>MAX_DEPTH:raise SourceError('block nesting exceeds32',self.tokens[self.index][1])
        self.take('{')
        while self.peek()!='}':
            if self.peek()=='<eof>':raise SourceError('unclosed block',self.tokens[self.index][1])
            self.statement(depth)
        self.take('}')
    def statement(self,depth=0):
        token,where=self.tokens[self.index]
        if token=='let':
            self.take()
            if depth:raise SourceError('declarations are top-level only',where)
            name,offset=self.identifier()
            if name in self.slots:raise SourceError('duplicate declaration',offset)
            if len(self.names)>=MAX_LOCALS:raise SourceError('at most64 locals',offset)
            self.take('=');self.expression();self.take(';')
            slot=len(self.names);self.slots[name]=slot;self.names.append(name);self.emit('STORE',slot,where)
        elif token=='print':
            self.take();self.expression();self.take(';');self.emit('PRINT',offset=where)
        elif token=='while':
            self.take();start=len(self.code);self.take('(');self.expression();self.take(')')
            branch=self.emit('JZ',0,where);self.block(depth+1);self.emit('JUMP',start,where);self.patch(branch,len(self.code))
        elif token=='if':
            self.take();self.take('(');self.expression();self.take(')')
            branch=self.emit('JZ',0,where);self.block(depth+1)
            if self.peek()=='else':
                self.take();end=self.emit('JUMP',0,where);self.patch(branch,len(self.code));self.block(depth+1);self.patch(end,len(self.code))
            else:self.patch(branch,len(self.code))
        else:
            name,offset=self.identifier();slot=self.slot(name,offset)
            self.take('=');self.expression();self.take(';');self.emit('STORE',slot,where)


def compile_source(source):
    compiler=_Compiler(source)
    try:
        while compiler.peek()!='<eof>':compiler.statement()
        compiler.emit('HALT',offset=len(source))
    except RecursionError as error:raise SourceError('host parser stack exhausted',compiler.tokens[compiler.index][1]) from error
    result=Program(tuple(compiler.code),tuple(compiler.names),source);verify(result);return result


def verify(program):
    """Conservative control-flow dataflow; all values are signed32 integers.

    Branches propagate both successors. Joins require equal operand depths and
    intersect definitely-initialized slots. Unreachable code gets shape checks.
    This is not a termination, arithmetic or source/bytecode equivalence proof.
    """
    if type(program) is not Program or type(program.code) is not tuple:raise VerificationError('exact immutable Program/code tuple required')
    code,names=program.code,program.names
    if not 1<=len(code)<=MAX_CODE:raise VerificationError('code length must be1..4096')
    if type(names) is not tuple or len(names)>MAX_LOCALS:raise VerificationError('at most64 named slots')
    if any(type(n) is not str or re.fullmatch(r'[A-Za-z_][A-Za-z_0-9]{0,63}',n) is None or n in KEYWORDS for n in names):
        raise VerificationError('invalid slot name')
    if len(set(names))!=len(names):raise VerificationError('duplicate slot name')
    if type(program.source) is not str or len(program.source)>MAX_SOURCE:raise VerificationError('bounded source-map text required')
    noarg={'NEG','ADD','SUB','MUL','DIV','LT','EQ','PRINT','HALT'}
    ops=noarg|{'CONST','LOAD','STORE','JZ','JUMP'}
    for pc,instruction in enumerate(code):
        if type(instruction) is not Instruction or type(instruction.op) is not str or instruction.op not in ops:
            raise VerificationError(f'invalid instruction at{pc}')
        op,arg=instruction.op,instruction.arg
        if type(instruction.offset) is not int or not 0<=instruction.offset<=len(program.source):raise VerificationError('source offset outside map')
        if op in noarg and arg is not None:raise VerificationError('unexpected operand')
        if op=='CONST' and not _integer(arg):raise VerificationError('constant must be signed32 integer')
        if op in ('LOAD','STORE') and (type(arg) is not int or not 0<=arg<len(names)):raise VerificationError('slot outside frame')
        if op in ('JZ','JUMP') and (type(arg) is not int or not 0<=arg<len(code)):raise VerificationError('branch outside code')
    if code[-1].op!='HALT':raise VerificationError('last instruction must be HALT')
    states={0:(0,frozenset())};pending=deque([0]);maximum=0
    while pending:
        pc=pending.popleft();height,initialized=states[pc];op,arg=code[pc].op,code[pc].arg
        pops=2 if op in {'ADD','SUB','MUL','DIV','LT','EQ'} else int(op in {'NEG','STORE','PRINT','JZ'})
        pushes=int(op in {'CONST','LOAD','NEG','ADD','SUB','MUL','DIV','LT','EQ'})
        if height<pops:raise VerificationError(f'stack underflow at{pc}')
        next_height=height-pops+pushes;maximum=max(maximum,next_height)
        if maximum>MAX_STACK:raise VerificationError('operand stack exceeds64 entries')
        if op=='LOAD' and arg not in initialized:raise VerificationError(f'possibly uninitialized slot at{pc}')
        if op=='STORE':initialized=initialized|{arg}
        if op=='HALT':
            if height:raise VerificationError('HALT requires empty stack')
            continue
        successors=[arg] if op=='JUMP' else ([arg,pc+1] if op=='JZ' else [pc+1])
        for successor in successors:
            if not 0<=successor<len(code):raise VerificationError('reachable execution falls off code')
            if successor not in states:
                states[successor]=(next_height,frozenset(initialized));pending.append(successor)
            else:
                old_height,old_initialized=states[successor]
                if old_height!=next_height:raise VerificationError(f'incompatible stack depths at join{successor}')
                common=old_initialized&initialized
                if common!=old_initialized:states[successor]=(old_height,frozenset(common));pending.append(successor)
    return dict(incoming_heights={pc:state[0] for pc,state in sorted(states.items())},max_stack=maximum,reachable_instructions=len(states))


class Machine:
    """Verified mutable interpreter with immutable debugger snapshots.

    A successful instruction commits one new snapshot. A fault preserves its
    incoming state; earlier instructions' assignments/output stay committed.
    Host Python can mutate this object: it is not an isolation/security boundary.
    """
    def __init__(self,program,*,budget=10000,output_limit=1000):
        self.verification=verify(program)
        if type(budget) is not int or not 1<=budget<=100000:raise ValueError('budget must be integer1..100000')
        if type(output_limit) is not int or not 0<=output_limit<=1000:raise ValueError('output limit must be integer0..1000')
        self.program,self.budget,self.output_limit=program,budget,output_limit
        self._state=Snapshot(0,(),(None,)*len(program.names),(),0,False)
    @property
    def state(self):return self._state
    def step(self):
        before=self._state
        if before.halted:return before
        instruction=self.program.code[before.pc];op,arg=instruction.op,instruction.arg
        def fail(message):raise RuntimeFault(message,before,instruction.offset)
        if before.steps>=self.budget:fail('instruction budget exhausted')
        stack,frame,output=list(before.stack),list(before.locals),list(before.output)
        pc,halted=before.pc+1,False
        if op=='CONST':stack.append(arg)
        elif op=='LOAD':stack.append(frame[arg])
        elif op=='STORE':frame[arg]=stack.pop()
        elif op=='NEG':
            result=-stack[-1]
            if not _integer(result):fail('signed32 overflow')
            stack[-1]=result
        elif op in {'ADD','SUB','MUL','DIV','LT','EQ'}:
            left,right=stack[-2:]
            if op=='ADD':result=left+right
            elif op=='SUB':result=left-right
            elif op=='MUL':result=left*right
            elif op=='DIV':
                if right==0:fail('division by zero')
                result=trunc_div(left,right)
            elif op=='LT':result=int(left<right)
            else:result=int(left==right)
            if not _integer(result):fail('signed32 overflow')
            stack[-2:]=[result]
        elif op=='PRINT':
            if len(output)>=self.output_limit:fail('output budget exhausted')
            output.append(stack.pop())
        elif op=='JZ':
            if stack.pop()==0:pc=arg
        elif op=='JUMP':pc=arg
        elif op=='HALT':pc,halted=before.pc,True
        self._state=Snapshot(pc,tuple(stack),tuple(frame),tuple(output),before.steps+1,halted);return self._state
    def run(self):
        while not self.state.halted:self.step()
        return self.state
    def until(self,*,breakpoints=(),steps=100):
        """Pause before valid instruction indices; step() crosses a breakpoint."""
        if type(breakpoints) is not tuple or any(type(p) is not int or not 0<=p<len(self.program.code) for p in breakpoints):raise ValueError('tuple of valid instruction indices required')
        if type(steps) is not int or not 0<=steps<=100000:raise ValueError('debugger steps must be0..100000')
        for _ in range(steps):
            if self.state.halted or self.state.pc in breakpoints:break
            self.step()
        return self.state


def disassemble(program):
    proof=verify(program);lines=[]
    for pc,instruction in enumerate(program.code):
        height=proof['incoming_heights'].get(pc,'-');arg='' if instruction.arg is None else str(instruction.arg)
        lines.append(f'{pc:04d} h={height!s:>2} {instruction.op:<5} {arg:<5} @ {instruction.offset}')
    return '\n'.join(lines)
