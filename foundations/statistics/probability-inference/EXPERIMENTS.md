# Enumerating coverage and breaking the iid assumption

## Questions and hypotheses

E1 asks whether two nominal95% binomial interval procedures actually include
the true parameter95% of the time for each declared finite model. Prediction:
Wald's zero-count degeneracy is particularly poor near a boundary; Wilson
handles it better, but discreteness and the score approximation prevent a
universal95% equality or guarantee.

E2 asks whether identical marginal probabilities suffice for iid interval
inference. Prediction: copying one random bit20 times retains each marginal
p=.2 but destroys the independence needed to use20 as an iid sample size.

## Controlled procedure and instrumentation

Python3.10+, standard library only. From repository root:

```bash
python3 -m unittest discover -s foundations/statistics/probability-inference -v
python3 foundations/statistics/probability-inference/experiment.py --output foundations/statistics/probability-inference/evidence/your-run.json
```

For E1 hold the nominal normal quantile and inclusion rule fixed. Enumerate
every K under Binomial(n,p), with n in{5,20,100}, p in{.02,.2,.5}. Vary only
n,p and the interval method. Record rational coverage masses, their decimal
presentations and expected interval width. The mass sum is exact conditional
on floating endpoint decisions, not a Monte Carlo estimate or a proof of the
sampling model. Save n,p and the procedure identity with each observation.

For E2 hold n=20, marginal p=.2, Wilson procedure, replication count4,000
and RNG seed7241 fixed. Generate a fresh iid bit record and a separate copied
bit record per replication. Record how many intervals cover.2. Compare the
iid result with exact enumerated iid coverage, and compare the copied result
with its exact possible counts0 or20. One seeded simulation is not the theorem;
the two-count argument explains the copied process independently.

The script also retains the exact fault-model posterior, the zero-count
intervals and the six-assignment permutation test as cross-checks. No external
dataset, physical instrument, subject or real factory observation is involved.

## Actually executed observations

The [retained run](evidence/observed-2026-10-23.json) records UTC time,
Python/platform, parameters and outputs. Selected observations are:

| Controlled case | Observed result | Scope of interpretation |
| --- | --- | --- |
| n=5,p=.02 | Wald coverage.096001584; Wilson.9039207968 | This boundary case refutes uniform nominal95% coverage for both procedures |
| n=20,p=.2 | Exact Wilson coverage≈.956328122 | A different parameter pair has different coverage |
| iid20-bit records | 3,828/4,000 intervals covered.2, empirical.957 | Compatible with the declared exact iid coverage; one finite simulation |
| One bit copied20 times | 0/4,000 covered.2; exact model coverage0 | Marginal probabilities alone did not validate the iid standard error |

At n=5,p=.02 the Wilson width is substantially larger than the degenerate
Wald intervals on the most common outcome. Narrower intervals are not an
unqualified improvement when they fail to cover their target. Conversely,
high coverage achieved by always returning[0,1] would give little precision;
retain width and coverage together.

## Alternative explanations and limits

A simulation/analytic discrepancy could come from finite sampling fluctuation,
a mismatched tail/endpoint convention, RNG/code defects or a different sampling
process. Tests compare binomial masses to enumerated binary paths and Wilson
roots to the original score equation, including exact deterministic parameters.
They cannot prove the iid model describes a real stream of failures.

Do not repeatedly change the seed until an attractive result appears. Do not
describe the seed as a secure randomness source. Fraction masses can grow
expensive; n≤1000 is deliberately bounded. Near an approximate interval
endpoint, finite precision can change inclusion. Identically distributed
observations can also be dependent in ways different from complete copying.

Follow up by adding block correlation, unequal per-trial probabilities,
selection of only successful records, and a predeclared multi-test procedure.
For each, write the data-generating process first and establish an independent
finite oracle before treating simulation output as evidence.
