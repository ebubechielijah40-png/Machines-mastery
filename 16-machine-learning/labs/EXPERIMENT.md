# Experiment: causality, derivatives, scaling, and state reuse

## Question and falsifiable predictions

Does this isolated mechanism preserve causal information flow and reproduce
its own full-prefix output when decoding incrementally? Are derived gradients
consistent with independent perturbations? Does square-root scaling prevent
concentration for deliberately correlated vectors?

Before running predict: (a) earlier outputs do not change after mutating only
the final token; (b) incremental and full outputs agree within `1e-12` absolute
error; (c) query central-difference error is below `1e-8` for the supplied
moderate-valued case; (d) even scaled weights concentrate for all-ones vectors
as width grows. The fourth case intentionally violates the random-coordinate
assumptions; it is not a test of initialization distributions.

## Controls, procedure, instrumentation

Use Python 3.10+ standard library. No GPU, dataset, API, account or network is
needed. Keep sequence length 32, seed 2718, head width 4, identity projections
and binary64 arithmetic fixed for the causality/cache comparison. Mutate only
the last token. For the gradient comparison perturb one query scalar at a
time by `±1e-6`. For concentration keep q/key construction fixed and vary only
width through 1, 4, 16 and 64. Values `[1]` and `[0]` expose routing directly.
`perf_counter` records one illustrative full-call time; it is not a benchmark.
`platform`/`sys.version` record the execution environment. Counts are derived
from loop structure, not measured CPU/GPU hardware counters.

Run from repository root:

```sh
python3 -m unittest discover -s 16-machine-learning/labs -v
python3 16-machine-learning/labs/experiment_attention.py
```

Save stdout unchanged to a new result file; retain the interpreter version,
command, and any failures. Do not overwrite committed historical evidence.

## Actual reference observation, 2026-10-22

Executed raw output: [JSON](evidence/2026-10-22-attention.json).
Actual test output: [18 tests](evidence/2026-10-22-tests.txt).
The reference run observed zero maximum absolute difference for both cache
versus full computation and earlier-prefix outputs after future mutation.
Query-gradient central-difference error was `3.069764407948039e-11`. Wrong
post-normalization masking yielded a row sum `4.122307227883699e-09`.
For width 64, the scaled first weight was `0.9996646498695336`; unscaled rounded
to `1.0`. The observed single-call time is in the JSON and should not be used
to claim an optimization speedup.

At n=32 the **derived** counts are 528 score pairs for cached generation and
5984 for recomputing all prefix outputs. Projection vector counts are 96 and
1584 respectively. A better uncached baseline could calculate only the newest
query while recomputing old K/V; these counts do not compare against that
baseline. The cache is not asymptotically faster than one full causal call.

## Interpretation, alternatives, and limits

These observations support the small-input local invariants and the derived
VJP in this implementation. Identical code paths could share a bug, which is
why tests also compare against Decimal arithmetic, hand edge cases and
independent central differences. Floating-point cancellation and an unsuitable
step size can mislead finite differences; repeat at several step sizes and
avoid saturated or nonsmooth objectives when diagnosing derivatives.

Exact zero on these inputs is not a proof for all real numbers, lengths, model
stacks, data preprocessing or deployed systems. This layer has no training,
position features, dropout, batching, padding, security isolation or learned
language behavior. Caching does not establish truth, provenance or privacy.
No machine-translation result from the research paper has been reproduced.

## Follow-up experiments

1. Repeat gradient checks for steps `1e-3`, `1e-5`, `1e-7`, `1e-9`; identify the
   region where truncation error gives way to cancellation.
2. Sample independent zero-mean unit-variance q/K coordinates at each width,
   then estimate score variance over many draws. This investigates the stated
   variance model, unlike the deterministic counterexample above.
3. Benchmark warmed-up repeated cached generation against both full-prefix
   recomputation and a newest-query-only uncached baseline. Report median,
   spread, validation costs, n, widths, trials and Python allocation limits.
4. Deliberately reuse one cache across two synthetic users; observe state
   contamination, then enforce ownership/reset and add a regression test.
