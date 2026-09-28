# Growth is not an exact runtime

Runnable original demonstration; learner NOT STARTED. Python 3.10+ standard library. From repository root:

```sh
python3 algorithmic-problem-solving/experiments/growth/benchmark.py --output /tmp/my-growth-run.json
```

Use a new output path. The bounded run compares constant indexing, logarithmic binary search, linear sum, sorting, quadratic duplicate detection, expected-linear hashing and exponential recursion. Sorting's general O(n log n) comparison bound is not an assertion that this particular partially ordered input takes that many comparisons; Python's adaptive implementation may exploit order. Hashing has expected, not universal worst-case, constant membership cost. Integer/key costs and runtime implementation are part of the cost model.

For distinct values, the naive checker compares every pair: 0+1+…+(n−1)=n(n−1)/2. The improved method visits n values and retains a set, trading space for expected time. Both exit early on an immediate duplicate, demonstrating distribution dependence. The full recursion tree satisfies T(d)=1+2T(d−1), T(0)=1, hence 2^(d+1)−1 calls. These counts are checked independently of elapsed time.

Timing uses five runs per case; traced Python allocation is measured in a separate run because instrumentation changes costs. It is not total resident memory. Built-in loops versus Python loops have different constants; tiny inputs and noisy timings do not establish asymptotic dominance. Cache effects require additional instrumentation before attribution. Plot samples or tabulate median/min/max versus n, preserve outliers, and state the input distribution. The production ledger supplies a separate realistic indexing/cache application. This demonstration does not count toward a topic's 20-problem quota.
