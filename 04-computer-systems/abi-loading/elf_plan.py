"""Strict bounded ELF64 little-endian x86-64 teaching load plan, never execution.

Accepts a conservative subset, not every valid ELF. No relocations/interpreter,
page-sharing resolution, TLS, constructors, execution or hostile-code sandbox.
"""
from dataclasses import dataclass
import struct

MAX_FILE=4*1024*1024
MAX_MEMORY=8*1024*1024
U64=1<<64
HEADER=struct.Struct('<16sHHIQQQIHHHHHH')
PHDR=struct.Struct('<IIQQQQQQ')


@dataclass(frozen=True)
class Segment:
    offset:int
    virtual:int
    file_size:int
    memory_size:int
    flags:int
    alignment:int


@dataclass(frozen=True)
class Plan:
    kind:int
    entry:int
    bias:int
    interpreter:str|None
    segments:tuple


def parse(raw,*,bias=0):
    if type(raw) is not bytes or not HEADER.size<=len(raw)<=MAX_FILE:
        raise ValueError('ELF bytes length must lie in64..4MiB')
    if type(bias) is not int or not 0<=bias<U64 or bias%4096:
        raise ValueError('page-aligned uint64 bias required')
    ident,kind,machine,version,entry,phoff,_,_,ehsize,phsize,phnum,_,_,_=HEADER.unpack_from(raw)
    if ident[:7]!=b'\x7fELF\x02\x01\x01' or machine!=62 or version!=1 or kind not in (2,3):
        raise ValueError('only ELF64 little-endian x86-64 EXEC/DYN version1')
    if ehsize!=HEADER.size or phsize!=PHDR.size or not 1<=phnum<=128:
        raise ValueError('unsupported header/table dimensions')
    if phoff<HEADER.size or phoff+phnum*phsize>len(raw):
        raise ValueError('program table outside file')
    if kind==2 and bias:raise ValueError('this EXEC subset requires zero bias')
    segments=[];interpreter=None;total=0
    for n in range(phnum):
        typ,flags,offset,virtual,_,file_size,memory_size,alignment=PHDR.unpack_from(raw,phoff+n*phsize)
        if typ==3:
            if interpreter is not None or segments or not 2<=file_size<=1024 or offset+file_size>len(raw):
                raise ValueError('invalid interpreter segment')
            path=raw[offset:offset+file_size]
            if not path.endswith(b'\0') or b'\0' in path[:-1]:raise ValueError('interpreter must have one terminal NUL')
            try:interpreter=path[:-1].decode('ascii')
            except UnicodeError:raise ValueError('ASCII interpreter subset only') from None
        if typ!=1:continue
        if flags&~7 or flags&3==3:raise ValueError('unknown permissions or writable-executable policy violation')
        if file_size>memory_size or offset+file_size>len(raw) or virtual+memory_size+bias>=U64:
            raise ValueError('segment size/file/address bound failed')
        if alignment not in (0,1) and (alignment&(alignment-1) or virtual%alignment!=offset%alignment):
            raise ValueError('segment alignment/congruence failed')
        if virtual%4096!=offset%4096:raise ValueError('4KiB page congruence required')
        if segments and virtual<segments[-1].virtual+segments[-1].memory_size:
            raise ValueError('unordered or byte-overlapping segments unsupported')
        total+=memory_size
        if total>MAX_MEMORY:raise ValueError('materialized memory budget exceeded')
        segments.append(Segment(offset,virtual,file_size,memory_size,flags,alignment))
    if not segments or not any(s.flags&1 and s.virtual<=entry<s.virtual+s.memory_size for s in segments):
        raise ValueError('entry must lie in an executable load segment')
    return Plan(kind,entry+bias,bias,interpreter,tuple(segments))


def materialize(raw,plan):
    # Reparse rather than trusting a hand-constructed Plan to bypass bounds.
    if type(plan) is not Plan or plan!=parse(raw,bias=plan.bias):raise ValueError('matching verified plan required')
    return tuple((s.virtual+plan.bias,raw[s.offset:s.offset+s.file_size]+bytes(s.memory_size-s.file_size),s.flags)
                 for s in plan.segments)


def read(image,address,count,permission='r'):
    if type(address) is not int or type(count) is not int or not 1<=count<=4096 or permission not in ('r','w','x'):
        raise ValueError('bounded address/count and permission required')
    mask={'r':4,'w':2,'x':1}[permission]
    for start,data,flags in image:
        if start<=address and address+count<=start+len(data):
            if not flags&mask:raise PermissionError('segment permission refused')
            return data[address-start:address-start+count]
    raise MemoryError('range not within one modeled segment')
