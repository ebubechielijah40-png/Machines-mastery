"""Independent API boundary probes; retained before/after observations only."""
import argparse,hashlib,importlib.util,json,platform,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]

def load(name,path):
    spec=importlib.util.spec_from_file_location(name,ROOT/path)
    module=importlib.util.module_from_spec(spec);sys.modules[name]=module
    spec.loader.exec_module(module)
    return module

def run():
    specifications=[('noise','20-quantum-computing/noise-correction/noise.py',[
        ('unnormalized_large_state',lambda m:m.pure(1e308,0)),
        ('unrepresentable_integer',lambda m:m.scalar(10**1000)),
        ('unnormalized_large_vector',lambda m:m.vector([1e308]+[0]*7))]),
       ('phylogeny','18-computational-biology/population-phylogeny/phylogeny.py',[
        ('invalid_transposed_entry',lambda m:m.upgma(['A','B'],[[0,1],[None,0]]))]),
       ('privacy','13-privacy/count-release/count_release.py',[
        ('finite_inputs_overflow_output',lambda m:m.laplace_quantile(.01,1e308))])]
    results=[];hashes={}
    for name,path,calls in specifications:
        module=load('review_'+name,path)
        hashes[path]=hashlib.sha256((ROOT/path).read_bytes()).hexdigest()
        for label,call in calls:
            try:results.append(dict(probe=label,returned=repr(call(module)),controlled_rejection=False))
            except Exception as exc:results.append(dict(probe=label,exception=type(exc).__name__,message=str(exc),controlled_rejection=isinstance(exc,ValueError)))
    return dict(reviewer='root integration; independent of these module authors',python=sys.version,platform=platform.platform(),code_sha256=hashes,results=results,limits='Selected input-boundary probes, not a universal scientific or numerical correctness proof.')

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path);parser.add_argument('--require-repaired',action='store_true')
    args=parser.parse_args();result=run();data=json.dumps(result,indent=2)+'\n'
    if args.output:args.output.write_text(data)
    else:print(data,end='')
    if args.require_repaired and not all(r['controlled_rejection'] for r in result['results']):raise SystemExit(1)
