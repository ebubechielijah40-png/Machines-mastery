from sequence_lab import *

def run():
    assert parse_fasta('>x\nACG\nTT\n>y\nNN')==[('x','ACGTT'),('y','NN')]
    assert reverse_complement('ACGT')=='ACGT'
    assert reverse_complement(reverse_complement('AAGTC'))=='AAGTC'
    assert abs(gc_fraction('AAGC')-.5)<1e-12
    assert kmer_counts('AAAA',2)=={'AA':3}
    score,a,b=global_alignment('GATTACA','GCATGCU')
    assert len(a)==len(b) and score<=len(a)
    print('sequence_lab: PASS')
if __name__=='__main__': run()
