# Exercises

1. Compute the sample mean/variance of[1,2,3] and explain the denominator.
2. Enumerate the four ordered resamples of[0,1]. Why does[0,1] appear as a mean
   twice but not as one sample occurrence twice?
3. Derive conditional bootstrap variance `(n-1)*s²/n²` for the mean.
4. Compute q(.25),q(.5),q(.75) under the declared inverse-CDF rule for[0,.5,.5,1].
5. Implement exact enumeration and a seeded random approximation independently.
   Explain why without-replacement shuffling cannot do the same job.
6. Derive P(all zero) for Bernoulli p=.1,n=5 and an upper bound on percentile
   coverage. Does increasing B change that bound?
7. Reconstruct the full exact-coverage finite sum over k. Distinguish original
   sampling randomness from conditional resampling randomness.
8. For data transformed by a positive scale a and offset b, derive how the
   percentile endpoints change when the same random indices are reused.
9. Give a sampling process in which100 repeated rows contain the information
   of only one independent observation. Identify the missing covariance terms.
10. Debug a bootstrap that fits preprocessing or chooses its interval after seeing
    the held result. Which reported evidence becomes conditional on that choice?
11. Experiment: hold one sample fixed, vary B and seeds, and compare conditional
    simulated probabilities with exact enumeration. Report approximation error,
    not a supposed increase in population evidence.
12. Transfer: compare two services using matched requests to the same workload.
    State a target parameter, identify pairing/dependence, and design a resampling
    unit. Implement a tiny exact paired mean-difference distribution. Explain
    which production workloads the synthetic model cannot represent.
