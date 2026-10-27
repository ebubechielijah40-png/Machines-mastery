# Build and investigate a bounded count release

Read [the original lesson](LESSON.md) for sensitivity, the ideal Laplace proof,
inverse sampling, composition and exact budget accounting. Begin with the
internal [probability unit](../../foundations/statistics/probability-inference/README.md)
and [calculus bridge](../../foundations/mathematics/core/04_CALCULUS_OPTIMIZATION.md).

Python3.10+, standard library only, synthetic locally controlled data:

```bash
python3 -m unittest discover -s 13-privacy/count-release -v
python3 13-privacy/count-release/experiment.py
```

Work through [exercises](EXERCISES.md) before opening [hints](HINTS.md) or
[solutions](SOLUTIONS.md). The lesson retains the full experiment design,
[executed observations](evidence/observed.json) and [inspected source scopes](SOURCES.md).
Reconstruct the likelihood-ratio argument and demonstrate the seed-reuse
failure before extending the mechanism.

The continuous mathematical proof is distinct from this finite-float sampler.
The sampler and in-memory accountant are teaching mechanisms, with no claim
to certify a private-data service. Contribution enforcement, finite-precision
analysis, durable/concurrent accounting and reviewed deployment remain missing.
