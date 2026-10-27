"""Original bounded JC69 distance and UPGMA; exact assumptions in README.md."""
from dataclasses import dataclass
import itertools
import math


def mismatch(a,b):
    if not isinstance(a,str) or not isinstance(b,str) or len(a)==0 or len(a)!=len(b):
        raise ValueError('equal-length nonempty aligned sequences required')
    if set(a+b)-set('ACGT'):
        raise ValueError('aligned unambiguous uppercase DNA only; gaps need a declared policy')
    return sum(x!=y for x,y in zip(a,b))/len(a)


def jc_from_fraction(p):
    if isinstance(p,bool) or not isinstance(p,(int,float)) or not math.isfinite(p) or not 0 <= p < .75:
        raise ValueError('finite JC69 estimate requires 0 <= mismatch fraction < .75')
    return -.75*math.log1p(-4*p/3)


def jc_distance(a,b):return jc_from_fraction(mismatch(a,b))


@dataclass(frozen=True)
class Cluster:
    members:tuple
    height:float
    children:tuple=()

    def record(self):
        return {'members':self.members,'height':self.height,'children':[c.record() for c in self.children]}


def validate(labels,distances):
    if not isinstance(labels,(list,tuple)) or not 2 <= len(labels) <= 32 or any(not isinstance(x,str) or not x for x in labels) or len(set(labels))!=len(labels):
        raise ValueError('two through thirty-two distinct nonempty labels required')
    n=len(labels)
    if not isinstance(distances,(list,tuple)) or len(distances)!=n or any(not isinstance(row,(list,tuple)) or len(row)!=n for row in distances):
        raise ValueError('square distance matrix required')
    # Validate all entries before inspecting their transposed partners.
    for row in distances:
        for d in row:
            try:
                valid=not isinstance(d,bool) and isinstance(d,(int,float)) and d>=0 and math.isfinite(d)
            except OverflowError:
                valid=False
            if not valid:raise ValueError('finite nonnegative distances required')
    for i in range(n):
        for j in range(n):
            d=distances[i][j]
            if abs(d-distances[j][i])>1e-10:raise ValueError('distance matrix must be symmetric')
        if distances[i][i]!=0:raise ValueError('diagonal must be zero')


def upgma(labels,distances):
    validate(labels,distances)
    index={name:i for i,name in enumerate(labels)}
    active=[Cluster((name,),0) for name in sorted(labels)]
    merges=[]
    while len(active)>1:
        choices=[]
        for a,b in itertools.combinations(active,2):
            d=sum(distances[index[x]][index[y]] for x in a.members for y in b.members)/(len(a.members)*len(b.members))
            choices.append((d,a.members,b.members,a,b))
        d,_,_,a,b=min(choices,key=lambda x:x[:3])
        new=Cluster(tuple(sorted(a.members+b.members)),d/2,(a,b))
        merges.append({'left':a.members,'right':b.members,'distance':d,'height':d/2})
        active=[c for c in active if c is not a and c is not b]+[new]
        active.sort(key=lambda c:c.members)
    return active[0],merges


def clades(root):
    return [root.members]+[members for child in root.children for members in clades(child)]


def cophenetic(root):
    result={}
    def visit(node):
        if not node.children:return
        a,b=node.children
        for x in a.members:
            for y in b.members:result[tuple(sorted((x,y)))]=2*node.height
        visit(a);visit(b)
    visit(root)
    return result


def ultrametric_violation(labels,distances):
    validate(labels,distances)
    worst=0
    for i,j,k in itertools.combinations(range(len(labels)),3):
        a,b,c=sorted([distances[i][j],distances[i][k],distances[j][k]])
        worst=max(worst,c-b)
    return worst
