import json,platform,sys
from budget import choose_prefix

def observe():
    cases=[]
    for sizes,capacity in [([12,7,5],20),([12,11,9],20),([],0),([0,0,1],0),([2,3],5)]:
        accepted,used=choose_prefix(sizes,capacity)
        cases.append({'sizes':sizes,'capacity_bytes':capacity,'accepted':accepted,'used_bytes':used})
    return {'environment':{'python':sys.version,'platform':platform.platform()},'scope':'exact semantic cases, not timing or Python heap bytes','cases':cases}

if __name__=='__main__':print(json.dumps(observe(),indent=2))
