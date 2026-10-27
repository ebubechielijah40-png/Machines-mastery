"""Finite original bag-join planner, explicitly not PostgreSQL/SQLite internals."""
from collections import Counter,defaultdict
from dataclasses import dataclass
MAX_ROWS=2000
MAX_OUTPUT=100000


def checked_rows(rows):
    out=[]
    for row in rows:
        if len(out)>=MAX_ROWS:raise ValueError('input row budget exceeded')
        if type(row) is not tuple or len(row)!=2 or type(row[0]) is not int or type(row[1]) is not str:
            raise ValueError('(integer key,text payload) tuples required')
        out.append(row)
    return out


@dataclass(frozen=True)
class Plan:
    algorithm:str
    build_side:str|None
    estimated_matches:int
    estimated_work:int
    memory_rows:int


def choose_plan(n,m,*,left_distinct,right_distinct,memory_rows):
    values=(n,m,left_distinct,right_distinct,memory_rows)
    if any(type(x) is not int or not 0<=x<=MAX_ROWS for x in values):raise ValueError('bounded integer statistics required')
    if (n==0)!=(left_distinct==0) or (m==0)!=(right_distinct==0) or left_distinct>n or right_distinct>m:
        raise ValueError('distinct and row counts disagree')
    estimate=0 if not n or not m else n*m//max(left_distinct,right_distinct)
    nested=n*m+estimate;hashed=n+m+2*estimate
    if min(n,m)<=memory_rows and hashed<nested:
        return Plan('hash','left' if n<=m else 'right',estimate,hashed,memory_rows)
    return Plan('nested',None,estimate,nested,0)


def exact_cardinality(left,right):
    a=Counter(row[0] for row in checked_rows(left));b=Counter(row[0] for row in checked_rows(right))
    return sum(n*b[k] for k,n in a.items())


def execute_join(left,right,plan):
    left=checked_rows(left);right=checked_rows(right)
    if type(plan) is not Plan or plan.algorithm not in ('nested','hash'):raise ValueError('declared plan required')
    if type(plan.memory_rows) is not int or not 0<=plan.memory_rows<=MAX_ROWS:raise ValueError('bounded row grant required')
    out=[];comparisons=build=probes=0
    def emit(a,b):
        if len(out)>=MAX_OUTPUT:raise ValueError('materialized output budget exhausted')
        out.append(a+b)
    if plan.algorithm=='nested':
        for a in left:
            for b in right:
                comparisons+=1
                if a[0]==b[0]:emit(a,b)
    else:
        if plan.build_side not in ('left','right'):raise ValueError('hash plan build side required')
        build_rows,probe_rows=(left,right) if plan.build_side=='left' else (right,left)
        if len(build_rows)>plan.memory_rows:raise ValueError('actual build exceeds grant: replan/spill')
        buckets=defaultdict(list)
        for row in build_rows:buckets[row[0]].append(row);build+=1
        for row in probe_rows:
            probes+=1
            for match in buckets.get(row[0],()):
                comparisons+=1
                emit(match,row) if plan.build_side=='left' else emit(row,match)
    return dict(rows=out,comparisons=comparisons,build_rows=build,probes=probes,actual_work=comparisons+build+probes+len(out))
