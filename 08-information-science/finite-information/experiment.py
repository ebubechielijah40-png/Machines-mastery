import json,platform,sys
from information import joint_information


def main():
    results=[]
    for flip in [0,.01,.1,.25,.5,.75,.9,1]:
        table=[[(1-flip)/2,flip/2],[flip/2,(1-flip)/2]]
        results.append({'flip_probability':flip,'joint_table':table,**joint_information(table)})
    print(json.dumps({'kind':'finite distribution calculation, not sampled physical channel data',
      'environment':{'python':sys.version,'platform':platform.platform()},
      'input_distribution':'uniform binary X; Y=X XOR independent Bernoulli(flip)',
      'results':results},indent=2))

if __name__=='__main__':main()
