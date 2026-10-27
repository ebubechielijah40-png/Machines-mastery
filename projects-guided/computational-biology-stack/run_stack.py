"""Connect bounded synthetic sequence, population and tree mechanisms locally."""
import hashlib
import json
import platform
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[2]
for relative in ['18-computational-biology/code','18-computational-biology/population-phylogeny']:
    sys.path.insert(0,str(ROOT/relative))
import alignment
import population
import phylogeny
import sequence_lab

FIXTURE='>synthetic-A\nAAAAAAAA\n>synthetic-B\nAAAAAATT\n'


def build_report():
    records=sequence_lab.parse_fasta(FIXTURE)
    result=alignment.align_global(records[0][1],records[1][1],2,-1,-2,max_cells=100)
    distance=phylogeny.jc_distance(result.a_aligned,result.b_aligned)
    labels=['A','B','C','D']
    matrix=[[0,2,6,6],[2,0,6,6],[6,6,0,4],[6,6,4,0]]
    root,merges=phylogeny.upgma(labels,matrix)
    files=[Path(__file__),Path(alignment.__file__),Path(population.__file__),Path(phylogeny.__file__),Path(sequence_lab.__file__)]
    return {'scope':'three original synthetic demonstrations; no inferred population/tree from two strings',
            'environment':{'python':sys.version,'platform':platform.platform()},
            'fixture_sha256':hashlib.sha256(FIXTURE.encode()).hexdigest(),
            'implementation_sha256':{str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in files},
            'alignment':{'score':result.score,'a':result.a_aligned,'b':result.b_aligned,'cells':result.cells_evaluated},
            'distance':{'model':'JC69, unambiguous gapless aligned sites','substitutions_per_site':distance},
            'population':{'copies':4,'initial':2,'generations':3,'model':'neutral fixed-size copy sampling',
                          'distribution':population.evolve(4,2,3)[-1],
                          'summary':population.summary(population.evolve(4,2,3)[-1])},
            'tree':{'labels':labels,'source':'separate original exact clock distance matrix','input':matrix,'merges':merges,'root':root.record()}}

if __name__=='__main__':print(json.dumps(build_report(),indent=2))
