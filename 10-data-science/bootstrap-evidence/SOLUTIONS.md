# Solutions

1. Mean2; squared deviations sum2; sample variance2/(3-1)=1. Dividing by3 gives
   the variance of the observed empirical distribution instead.
2. Means0,.5,.5,1, probability1/4 each ordered draw. Different ordered samples
   can give the same statistic; probabilities aggregate rather than disappear.
3. An empirical draw has variance Σ(xi-xbar)²/n=(n-1)s²/n. Averaging n independent
   resampled draws divides that variance by n, giving(n-1)s²/n².
4. The one-based index is ceil(p*4), giving0,.5,.5. At p=1 choose1.
5. Use a Cartesian product of observed occurrences for exact ordered samples;
   sample random indices independently for Monte Carlo. A permutation has exactly
   the original sum on every iteration and would estimate mean variation as0.
6. Probability.9^5=.59049, so coverage≤.40951 because every such[0,0] interval
   misses. More resamples leave that empirical distribution unchanged.
7. The README gives the finite sum; [stats_lab.py](../code/stats_lab.py) is the
   reference only after your derivation. The unknown original p weights observed
   k; the observed k/n defines the conditional bootstrap law. They are not equal
   by definition.
8. Each resampled mean becomes a*z+b. Positive a preserves order, so both
   endpoint quantiles transform by the same formula. Negative a reverses order
   and needs the endpoints exchanged with attention to the discrete convention.
9. If every row is the same latent Z, all pairwise covariances equal Var(Z).
   Var(mean)=Var(Z), not Var(Z)/100. A row bootstrap on an observed identical
   sample degenerates and does not recover latent variation.
10. Evaluation helped choose the procedure, so its apparent performance no longer
    independently assesses that selection. A fresh evaluation boundary or nested
    selection protocol is needed; this unit does not implement one.
11. Saved seeded counts differ from exact probabilities by conditional Monte Carlo
    error. Increasing B approximates the same empirical law; report the sample
    separately and do not count B as new population observations.
12. Use per-request differences di=latencyA_i-latencyB_i and resample whole pairs
    (equivalently the differences for this statistic). For two differences0,2,
    possible mean differences0,1,1,2 have masses1/4,1/2,1/4. This preserves pairing
    but does not handle time/burst dependence or prove representative production
    workload selection. Explain those assumptions before external inference.
