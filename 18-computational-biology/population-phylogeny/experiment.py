import json
import math
import platform
import statistics
import sys
from population import evolve,log_likelihood,simulate,summary
from phylogeny import clades,cophenetic,jc_distance,ultrametric_violation,upgma


def main():
    m,start,t,reps=20,10,30,2000
    exact=evolve(m,start,t)
    outcomes=[simulate(m,start,t,seed=i)[-1]/m for i in range(reps)]
    observed=simulate(40,10,12,seed=0,selection=0)
    labels=['A','B','C','D']
    models={'clock_matrix':[[0,2,6,6],[2,0,6,6],[6,6,0,4],[6,6,4,0]],
            'nonclock_additive_matrix':[[0,6,4,4],[6,0,8,8],[4,8,0,2],[4,8,2,0]]}
    trees={}
    for name,d in models.items():
        root,trace=upgma(labels,d)
        trees[name]={'input':d,'merges':trace,'tree':root.record(),'clades':clades(root),
                     'ultrametric_violation':ultrametric_violation(labels,d),
                     'cophenetic':{','.join(pair):v for pair,v in cophenetic(root).items()}}
    print(json.dumps({'kind':'synthetic finite-population and tree calculations; no organism/clinical data',
        'environment':{'python':sys.version,'platform':platform.platform()},
        'controls':{'copies':m,'initial':start,'generations':t,'selection':0,'replicates':reps,'seeds':'integers0..1999'},
        'exact_summaries':[{'generation':i,**summary(dist)} for i,dist in enumerate(exact)],
        'exact_final_distribution':exact[-1],
        'simulated':{'mean_frequency':statistics.mean(outcomes),'variance_population_estimator':statistics.pvariance(outcomes),
                     'loss_fraction':outcomes.count(0)/reps,'fixation_fraction':outcomes.count(1)/reps,
                     'final_counts':[round(x*m) for x in outcomes],
                     'first_five_trajectories':[simulate(m,start,t,seed=i) for i in range(5)]},
        'single_neutral_path':{'copies':40,'seed':0,'counts':observed,
            'selection_log_likelihood_grid':[{'s':s,'log_likelihood':log_likelihood(40,observed,s)} for s in [-.2,-.1,0,.1,.2,.4]]},
        'sequence_example':{'a':'AAAAAAAA','b':'AAAAAATT','mismatch_fraction':.25,'jc_distance':jc_distance('AAAAAAAA','AAAAAATT')},
        'trees':trees},indent=2))

if __name__=='__main__':main()
