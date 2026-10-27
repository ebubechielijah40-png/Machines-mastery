"""Actual computation on explicitly synthetic observations and Gaussian trials."""
import json,platform,random,statistics,sys
from pathlib import Path
from measurement_pipeline import read_bounded,summarize


def main():
    raw=read_bounded(Path(__file__).resolve().parents[1]/'data/synthetic.csv')
    result=summarize(raw,offset_milli_c=-10,calibration_u_milli_c=5)
    rng=random.Random(493);trials=10000;observed=[]
    for n in [1,4,25,100]:
        shared=[];independent=[]
        for _ in range(trials):
            common=rng.gauss(0,5)
            repeated=[rng.gauss(0,2) for _ in range(n)]
            shared.append(common+statistics.mean(repeated))
            independent.append(statistics.mean(rng.gauss(0,5)+x for x in repeated))
        observed.append({'n':n,'trials':trials,'shared_calibration_predicted_variance':25+4/n,
              'shared_calibration_observed_variance':statistics.pvariance(shared),
              'independent_calibration_predicted_variance':29/n,
              'independent_calibration_observed_variance':statistics.pvariance(independent)})
    print(json.dumps({'kind':'synthetic computation, not physical measurements',
      'environment':{'python':sys.version,'platform':platform.platform()},'fixed_seed':493,
      'example':result,'correlation_experiment_variance_units':'milli-celsius squared',
      'correlation_experiment':observed},indent=2))

if __name__=='__main__':main()
