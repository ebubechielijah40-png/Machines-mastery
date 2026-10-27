import json,math,platform,random,statistics,sys
from count_release import Budget,laplace_noise,log_density_ratio


def main():
    trials=20000;observations=[]
    for epsilon in [.1,.5,1,2]:
        rng=random.Random(710+int(epsilon*100));errors=[laplace_noise(1/epsilon,rng) for _ in range(trials)]
        observations.append({'epsilon':epsilon,'trials':trials,'predicted_mae':1/epsilon,
           'measured_mae':statistics.mean(abs(x) for x in errors),'predicted_variance':2/epsilon**2,
           'measured_variance':statistics.pvariance(errors),'measured_mean_error':statistics.mean(errors)})
    rng=random.Random(901);averages=[statistics.mean(laplace_noise(2,rng) for _ in range(100)) for _ in range(2000)]
    b=Budget(1_000_000);outputs=[b.release([1]*20+[0]*30,100_000,rng=random.Random(i+91)) for i in range(10)]
    try:b.release([1],1);denied=False
    except ValueError:denied=True
    print(json.dumps({'kind':'synthetic pedagogical finite-float simulation; no production DP certificate',
      'environment':{'python':sys.version,'platform':platform.platform()},'seed_policy':'fixed independent seeds explicitly for reproducibility',
      'noise_utility':observations,
      'density_grid':{'neighbor_counts':[10,11],'epsilon':.5,'max_absolute_log_ratio':max(abs(log_density_ratio(z,10,11,2)) for z in range(-100,101))},
      'repeated_release_average':{'releases_per_average':100,'epsilon_each':.5,'conservative_total_epsilon':50,
        'predicted_average_noise_variance':8/100,'observed_average_noise_variance':statistics.pvariance(averages)},
      'accountant':{'outputs':outputs,'spent_micros':b.spent,'remaining_micros':b.remaining,'eleventh_query_denied':denied}},indent=2))

if __name__=='__main__':main()
