"""Original count-based structure experiments, actually executed when invoked."""
from datetime import datetime,timezone
from pathlib import Path
import hashlib,json,platform,random,sys
from structures import ChainedMap,StableHeap,SearchTree,byte_hash


def main():
    rows=[]
    for n in (16,64,256,1024):
        row={'n':n}
        for name,hasher in [('rolling',byte_hash),('constant',lambda _:0)]:
            table=ChainedMap(hasher)
            for i in range(n):table[i.to_bytes(4,'little')]=i
            row['hash_'+name]={**table.inspect(),'key_comparisons':table.key_comparisons,'rehashed_entries':table.rehashed_entries}
            if name=='constant':assert table.key_comparisons==n*(n-1)//2
        items=[(n-i,i) for i in range(n)]
        heap=StableHeap(items);construction=heap.comparisons
        assert [heap.pop()[0] for _ in range(n)]==list(range(1,n+1))
        repeated=StableHeap()
        for priority,value in items:repeated.push(priority,value)
        row['heap']={'bottom_up_build_comparisons':construction,'repeated_push_comparisons':repeated.comparisons}
        for name,sequence in [('ascending',list(range(n))),('shuffled',random.Random(718).sample(range(n),n))]:
            tree=SearchTree()
            for i in sequence:tree[i]=i
            row['tree_'+name]={**tree.inspect(),'insertion_key_comparisons':tree.key_comparisons}
            assert tuple(k for k,v in tree.items())==tuple(range(n))
            if name=='ascending':assert tree.key_comparisons==n*(n-1)//2
        rows.append(row)
    return {'observed_at_utc':datetime.now(timezone.utc).isoformat(),'python':sys.version,'platform':platform.platform(),
            'source_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),Path(__file__).with_name('structures.py')]},
            'shuffle_seed':718,'rows':rows,
            'limits':'Logical comparisons and finite input families; no universal hashing guarantee, balance guarantee or wall-time ranking.'}


if __name__=='__main__':print(json.dumps(main(),indent=2))
