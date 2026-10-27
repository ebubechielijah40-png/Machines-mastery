# Bootstrap experiment and exact coverage counterexample

Question: does resampling an observed sample many times establish the intended
population uncertainty? Prediction: it estimates a distribution conditional on
the empirical sample, while a sample missing a rare outcome can give a severely
misleading percentile interval even with unlimited resampling.

Hold the statistic (mean), quantile convention (empirical CDF left inverse) and
nominal95% target fixed. First enumerate every ordered two-row resample of[0,1].
Then use10,000 pseudorandom resamples with seed7, retaining multiplicities of
each mean. Separately enumerate binomial counts under known synthetic p,n,
derive the corresponding ideal bootstrap percentile endpoints and sum true
sampling mass only when those endpoints include p. This separates Monte Carlo
error from a failure of the statistical procedure under its specified model.

Run from repository root with Python3.10+:

```bash
python3 -m unittest discover -s 10-data-science/code -v
python3 10-data-science/bootstrap-evidence/experiment.py
```

[The retained executed record](evidence/results.json) includes platform, Python,
UTC time, seeds and every finite count case. It observed resampled means0,.5,1
with counts2,487,5,049,2,464, compared with exact multiplicities1,2,1 out of4.
The all-zero five-row sample produced interval[0,0]. For true p=.1,n=5, the
ideal nominal95% percentile interval had enumerated coverage.40095. At n=20
and100 with p=.1 the recorded coverages were approximately.876037 and.966282.
They are conditional on the explicitly implemented quantile/inclusion rule,
not a universal ranking of bootstrap methods or an Efron paper reproduction.

The independent simple bound is especially useful: P(all five observations
are zero)=.9⁵=.59049. Every bootstrap resample from that event is zero and misses
true p=.1; hence any coverage for this procedure is at most.40951. Increasing
the resampling count cannot fix that missing empirical support.

Controls include sample size, generating distribution, statistic, interval rule,
repetition count and seed. Instrument observed sample values, resampled mean
frequencies, interval endpoints and inclusion decisions. An apparent discrepancy
can arise from finite simulation error, a different quantile convention or a
code defect. Shared subjects, time correlation, selection and nonresponse are
additional model failures not repaired by iid row resampling.

All observations are synthetic computations. No external population was sampled.
Follow up with dependent blocks or selection bias, changing one generating
mechanism at a time. State the appropriate independent sampling unit and retain
unfavorable results. [The lesson](README.md), [source map](SOURCES.md) and
separate [practice](EXERCISES.md) explain the derivation and interpretation.
