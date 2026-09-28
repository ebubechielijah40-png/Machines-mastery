from __future__ import annotations
from dataclasses import dataclass

DNA=set("ACGTN")
COMP=str.maketrans("ACGTNacgtn","TGCANtgcan")

def parse_fasta(text: str):
    records=[]; name=None; buf=[]
    for raw in text.splitlines():
        line=raw.strip()
        if not line: continue
        if line.startswith('>'):
            if name is not None: records.append((name,''.join(buf).upper()))
            name=line[1:].strip()
            if not name: raise ValueError('empty FASTA header')
            buf=[]
        else:
            if name is None: raise ValueError('sequence before header')
            seq=line.upper()
            bad=set(seq)-DNA
            if bad: raise ValueError(f'invalid DNA symbols: {sorted(bad)}')
            buf.append(seq)
    if name is not None: records.append((name,''.join(buf).upper()))
    return records

def reverse_complement(seq: str)->str:
    s=seq.upper()
    if set(s)-DNA: raise ValueError('invalid DNA')
    return s.translate(COMP)[::-1]

def gc_fraction(seq: str)->float:
    s=seq.upper(); known=[c for c in s if c in 'ACGT']
    if not known: return float('nan')
    return sum(c in 'GC' for c in known)/len(known)

def kmer_counts(seq: str,k:int):
    if k<=0: raise ValueError('k must be positive')
    s=seq.upper(); out={}
    for i in range(len(s)-k+1):
        kmer=s[i:i+k]; out[kmer]=out.get(kmer,0)+1
    return out

def global_alignment(a:str,b:str,match=1,mismatch=-1,gap=-1):
    n,m=len(a),len(b)
    f=[[0]*(m+1) for _ in range(n+1)]
    for i in range(1,n+1): f[i][0]=i*gap
    for j in range(1,m+1): f[0][j]=j*gap
    for i in range(1,n+1):
        for j in range(1,m+1):
            diag=f[i-1][j-1]+(match if a[i-1]==b[j-1] else mismatch)
            f[i][j]=max(diag,f[i-1][j]+gap,f[i][j-1]+gap)
    i,j=n,m; aa=[]; bb=[]
    while i or j:
        if i and j and f[i][j]==f[i-1][j-1]+(match if a[i-1]==b[j-1] else mismatch):
            aa.append(a[i-1]);bb.append(b[j-1]);i-=1;j-=1
        elif i and f[i][j]==f[i-1][j]+gap:
            aa.append(a[i-1]);bb.append('-');i-=1
        else:
            aa.append('-');bb.append(b[j-1]);j-=1
    return f[n][m], ''.join(reversed(aa)), ''.join(reversed(bb))
