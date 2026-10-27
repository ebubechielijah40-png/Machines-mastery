"""Deterministic teaching models, not a kernel or an MMU emulator."""
from collections import deque, OrderedDict
from dataclasses import dataclass

@dataclass(frozen=True)
class Job:
    name:str
    arrival:int
    burst:int


def schedule(jobs, policy='rr', quantum=1, switch_cost=0):
    """Single CPU, integer ticks, no I/O, fixed bursts, work-conserving queue.

    Arrival order ties follow input order. Arrivals at the end of a slice join
    before that unfinished job is requeued. A switch cost is charged only
    between different jobs with no intervening idle time, never initial dispatch.
    """
    jobs=list(jobs)
    if policy not in {'rr','fcfs'}:raise ValueError('policy must be rr or fcfs')
    for v in [quantum,switch_cost]:
        if type(v) is not int:raise ValueError('times must be integers, not bool')
    if quantum<=0 or switch_cost<0:raise ValueError('positive quantum, nonnegative switch cost required')
    if any(not isinstance(j,Job) or not isinstance(j.name,str) or not j.name or j.name in {'IDLE','SWITCH'} or type(j.arrival) is not int or j.arrival<0 or type(j.burst) is not int or j.burst<=0 for j in jobs):raise ValueError('invalid job')
    if len({j.name for j in jobs})!=len(jobs):raise ValueError('duplicate names')
    waiting=sorted(enumerate(jobs),key=lambda p:(p[1].arrival,p[0]))
    remaining={j.name:j.burst for j in jobs}; first={}; finish={}; ready=deque(); timeline=[]
    now=0; cursor=0; previous=None
    def arrivals():
        nonlocal cursor
        while cursor<len(waiting) and waiting[cursor][1].arrival<=now:
            ready.append(waiting[cursor][1]);cursor+=1
    while ready or cursor<len(waiting):
        arrivals()
        if not ready:
            arrival=waiting[cursor][1].arrival
            timeline.append(('IDLE',now,arrival));now=arrival;previous=None;arrivals()
        job=ready.popleft()
        if previous is not None and previous!=job.name and switch_cost:
            timeline.append(('SWITCH',now,now+switch_cost));now+=switch_cost;arrivals()
        first.setdefault(job.name,now)
        duration=remaining[job.name] if policy=='fcfs' else min(quantum,remaining[job.name])
        timeline.append((job.name,now,now+duration));now+=duration;remaining[job.name]-=duration
        arrivals()
        if remaining[job.name]:ready.append(job)
        else:finish[job.name]=now
        previous=job.name
    metrics={j.name:{'response':first[j.name]-j.arrival,'turnaround':finish[j.name]-j.arrival,'waiting':finish[j.name]-j.arrival-j.burst,'finish':finish[j.name]} for j in jobs}
    return {'timeline':timeline,'metrics':metrics,'elapsed':now,'useful_ticks':sum(j.burst for j in jobs)}


class Fault(Exception):
    def __init__(self,kind,address):self.kind=kind;self.address=address;super().__init__(f'{kind}: {address:#x}')

@dataclass
class Entry:
    frame:int
    permissions:frozenset
    user:bool
    accessed:bool=False
    dirty:bool=False

class AddressSpace:
    """8-bit VA, 16-byte pages, 2+2-bit two-level table, 32 physical frames.

    Per-object fully associative LRU TLB; mapping changes invalidate their VPN.
    Permissions are checked on every access, including a TLB hit. No contents,
    actual CPU privilege, replacement/swap or shared TLB/ASIDs are modeled.
    """
    def __init__(self,tlb_capacity=2):
        if type(tlb_capacity) is not int or tlb_capacity<0:raise ValueError('nonnegative TLB capacity')
        self.directory={};self.tlb=OrderedDict();self.capacity=tlb_capacity
    @staticmethod
    def _vpn(vpn):
        if type(vpn) is not int or not 0<=vpn<16:raise ValueError('VPN in [0,15]')
    def map(self,vpn,frame,permissions='rw',user=True):
        self._vpn(vpn)
        if type(frame) is not int or not 0<=frame<32:raise ValueError('frame in [0,31]')
        if not isinstance(permissions,str) or not set(permissions)<=set('rwx') or not permissions or type(user) is not bool:raise ValueError('invalid permission set')
        self.directory.setdefault(vpn>>2,{})[vpn&3]=Entry(frame,frozenset(permissions),user)
        self.tlb.pop(vpn,None)
    def unmap(self,vpn):
        self._vpn(vpn);table=self.directory.get(vpn>>2,{})
        if vpn&3 not in table:raise KeyError(vpn)
        del table[vpn&3]
        if not table:del self.directory[vpn>>2]
        self.tlb.pop(vpn,None)
    def entry(self,vpn):
        self._vpn(vpn)
        return self.directory[vpn>>2][vpn&3]
    def translate(self,address,access='r',user=True):
        if type(address) is not int or not 0<=address<256:raise ValueError('8-bit virtual address required')
        if access not in {'r','w','x'} or type(user) is not bool:raise ValueError('invalid access')
        vpn,offset=divmod(address,16);hit=vpn in self.tlb
        if hit:entry=self.tlb[vpn]
        else:
            try:entry=self.entry(vpn)
            except KeyError:raise Fault('NOT_PRESENT',address) from None
        if access not in entry.permissions or (user and not entry.user):raise Fault('PROTECTION',address)
        if self.capacity:
            self.tlb[vpn]=entry;self.tlb.move_to_end(vpn)
            if len(self.tlb)>self.capacity:self.tlb.popitem(last=False)
        entry.accessed=True
        if access=='w':entry.dirty=True
        return {'physical_address':entry.frame*16+offset,'vpn':vpn,'offset':offset,'tlb_hit':hit}
