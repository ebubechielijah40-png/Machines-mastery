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

def global_alignment(a: str, b: str, match=1, mismatch=-1, gap=-1):
    """Compatibility tuple API; see alignment.py for the checked mechanism.

    Scoring uses integers and a nonpositive linear gap score. Inputs may include
    RNA/protein symbols; this function does not validate a biological alphabet.
    """
    from alignment import align_global
    result = align_global(a, b, match, mismatch, gap)
    return result.score, result.a_aligned, result.b_aligned
