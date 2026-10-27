"""Original finite cache and two-stage translation models, no hardware emulator."""
from dataclasses import dataclass


def integer(x,minimum,maximum):
    if type(x) is not int or not minimum<=x<=maximum:raise ValueError('bounded integer required')


class SetCache:
    def __init__(self,*,sets=4,ways=1,line_bytes=16):
        integer(sets,1,64);integer(ways,1,8);integer(line_bytes,1,4096)
        if sets&(sets-1) or line_bytes&(line_bytes-1):raise ValueError('power-of-two geometry required')
        self.sets,self.ways,self.line_bytes=sets,ways,line_bytes
        self.lines=[[] for _ in range(sets)];self.hits=self.misses=0
    def access(self,address):
        integer(address,0,(1<<32)-1)
        if self.hits+self.misses>=10000:raise ValueError('finite cache trace exhausted')
        block=address//self.line_bytes;index=block%self.sets;tag=block//self.sets
        queue=self.lines[index];hit=tag in queue
        if hit:queue.remove(tag);self.hits+=1
        else:
            self.misses+=1
            if len(queue)==self.ways:queue.pop(0)
        queue.append(tag)
        return dict(hit=hit,set=index,tag=tag,block=block)


@dataclass(frozen=True)
class Mapping:
    frame:int
    permissions:frozenset
    def __post_init__(self):
        integer(self.frame,0,255)
        if type(self.permissions) is not frozenset or not self.permissions or not self.permissions<=frozenset('rwx'):
            raise ValueError('nonempty frozen permission subset required')


class TranslationFault(ValueError):
    pass


def nested_translate(address,guest,host,*,permission='r',page_bytes=256):
    integer(page_bytes,1,4096)
    if page_bytes&(page_bytes-1):raise ValueError('power-of-two page required')
    integer(address,0,page_bytes*256-1)
    if permission not in ('r','w','x'):raise ValueError('unknown access type')
    for table in (guest,host):
        if type(table) is not dict or len(table)>256 or any(type(k) is not int or not 0<=k<=255 or type(v) is not Mapping for k,v in table.items()):
            raise ValueError('bounded page map required')
    page,offset=divmod(address,page_bytes)
    if page not in guest:raise TranslationFault('guest page absent')
    first=guest[page]
    if permission not in first.permissions:raise TranslationFault('guest permission refused')
    if first.frame not in host:raise TranslationFault('host mapping absent')
    second=host[first.frame]
    if permission not in second.permissions:raise TranslationFault('host permission refused')
    return dict(guest_physical=first.frame*page_bytes+offset,
                host_physical=second.frame*page_bytes+offset,
                permissions=''.join(sorted(first.permissions&second.permissions)))
