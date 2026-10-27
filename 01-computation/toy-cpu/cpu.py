"""Original 8-bit/16-address accumulator ISA with explicitly bounded execution.

This is neither Hack nor RISC-V. A cycle is an abstract atomic transition; no
transistor delays, caches, interrupts, concurrency or hardware safety modeled.
"""
from dataclasses import dataclass,field


class DecodeError(ValueError):pass


def byte(x):
    if type(x) is not int or not 0<=x<256:raise ValueError('an unsigned byte is required')
    return x


def full_adder(a,b,carry):
    if any(type(x) is not int or x not in (0,1) for x in [a,b,carry]):raise ValueError('bits must be integers0/1')
    return (a^b^carry),(a&b)|(carry&(a^b))


def add8(a,b):
    byte(a);byte(b);result=carry=0
    for bit in range(8):
        s,carry=full_adder((a>>bit)&1,(b>>bit)&1,carry)
        result|=s<<bit
    return result,bool(carry)


def instruction(name,operand=0):
    codes={'NOP':0,'LDI':1,'ADD':2,'LDA':3,'STA':4,'JMP':5,'JZ':6,'HLT':15}
    if name not in codes:raise DecodeError('unknown mnemonic')
    if type(operand) is not int or not 0<=operand<16:raise ValueError('operand must fit four bits')
    if name in ('NOP','HLT') and operand:raise DecodeError('reserved low nibble must be zero')
    return codes[name]*16+operand


@dataclass
class CPU:
    memory: list[int]
    accumulator:int=0
    pc:int=0
    carry:bool=False
    halted:bool=False
    cycles:int=0

    def __post_init__(self):
        self.memory=list(self.memory)
        self.validate()

    def validate(self):
        if len(self.memory)!=16:raise ValueError('memory has exactly sixteen bytes')
        for value in self.memory:byte(value)
        byte(self.accumulator)
        if type(self.pc) is not int or not 0<=self.pc<16:raise ValueError('pc must be a four-bit address')
        if type(self.carry) is not bool or type(self.halted) is not bool:raise ValueError('flags must be boolean')
        if type(self.cycles) is not int or self.cycles<0:raise ValueError('cycles must be nonnegative')

    def step(self):
        self.validate()
        if self.halted:raise RuntimeError('processor halted')
        address=self.pc;word=self.memory[address];op,operand=word>>4,word&15
        before=dict(pc=self.pc,accumulator=self.accumulator,carry=self.carry)
        pc=(self.pc+1)&15;acc=self.accumulator;carry=self.carry;halted=False;write=None
        if op==0:
            if operand:raise DecodeError('reserved NOP operand')
        elif op==1:acc=operand
        elif op==2:acc,carry=add8(acc,self.memory[operand])
        elif op==3:acc=self.memory[operand]
        elif op==4:write=(operand,acc)
        elif op==5:pc=operand
        elif op==6:
            if acc==0:pc=operand
        elif op==15:
            if operand:raise DecodeError('reserved HLT operand')
            halted=True
        else:raise DecodeError(f'unsupported opcode {op:x}')
        # Nothing architectural changes until decoding/arithmetic validates.
        if write:self.memory[write[0]]=write[1]
        self.pc,self.accumulator,self.carry,self.halted=pc,acc,carry,halted
        self.cycles+=1
        return dict(address=address,word=word,opcode=op,operand=operand,before=before,
                    after=dict(pc=pc,accumulator=acc,carry=carry,halted=halted),write=write)

    def run(self,budget=1000):
        if type(budget) is not int or not 0<=budget<=1_000_000:raise ValueError('bounded integer cycle budget required')
        trace=[]
        while not self.halted and len(trace)<budget:trace.append(self.step())
        if not self.halted:raise TimeoutError('instruction budget exhausted; machine state retained for inspection')
        return trace


def multiplication_program(a=3,b=4):
    if type(a) is not int or not 0<=a<256 or type(b) is not int or not 1<=b<256:
        raise ValueError('a byte and positive byte multiplier required')
    return [instruction('LDI',0),instruction('STA',13),instruction('LDA',13),instruction('ADD',14),
            instruction('STA',13),instruction('LDA',15),instruction('ADD',12),instruction('STA',15),
            instruction('JZ',10),instruction('JMP',2),instruction('LDA',13),instruction('HLT'),255,0,a,b]
