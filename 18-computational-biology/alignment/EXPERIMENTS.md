# Alignment mechanism experiments and actual observations

Scope: synthetic strings, agent-executed CPU computation on 2026-10-22. No biological specimen, external dataset, instrument, paper benchmark, or learner assessment is involved. The hypotheses below explain the mathematical expectation; this protocol was written after the first exploratory run and is **not a preregistration**.

## Reproduce

From repository root, Python 3.10+, standard library only:

```sh
python3 18-computational-biology/code/alignment_experiment.py
python3 -m unittest discover -s 18-computational-biology/code -p 'test_alignment.py' -v
python3 -m unittest discover -s projects-guided/p14-bioinformatics/tests -v
```

The [raw results](evidence/results.json) include actual Python/platform strings, all timing samples, deterministic outputs, and hashes of the executed aligner and experiment script. [Validation record](evidence/validation.json) stores exact commands, exit codes, and complete captured stdout/stderr. Re-running should reproduce discrete scores/alignments/counts; times and allocation peaks can vary. Do not replace historical timing evidence with invented expected values.

## A. Does a gap parameter change the optimum explanation?

- **Question:** For fixed strings, does increasing gap penalty alter alignment structure?
- **Hypothesis:** At low gap cost, extra matches can justify gaps. At sufficiently high gap cost, direct mismatches become cheaper.
- **Controlled:** `ACGT`/`AGCT`, match=2, mismatch=-3, same implementation and deterministic tie policy.
- **Independent variable:** gap score -1,-2,-4.
- **Measurements/instrumentation:** returned score, displayed strings; independent column rescoring and input reconstruction tested separately.
- **Procedure:** Optimize all three scoring settings. Record the entire alignment, not only score.

Actual output:

| Gap | Score | A alignment | B alignment |
| ---: | ---: | --- | --- |
| -1 | 4 | A-CGT | AGC-T |
| -2 | 2 | A-CGT | AGC-T |
| -4 | -2 | ACGT | AGCT |

The gapped option has three matches and two gaps, score 6+2g. The direct option has two matches and two mismatches, score 4-6=-2. They tie at g=-4; diagonal priority selects direct alignment. Thus the observed structural change includes tie policy, not a uniquely determined biological answer. A different tie policy may choose the other optimum at that boundary. **Follow-up:** add g=-5 to make the direct alignment strictly preferable, then enumerate tied optima at -4.

## B. Does changing the objective change the consumed interval?

Fix `TTACGTAA`/`GGACGTCC` and scores (2,-3,-2). Global returns full spans [0,8), score -4; local returns both spans [2,6), `ACGT`/`ACGT`, score 8. The expected difference follows from global's requirement to account for flanks. It does not show that local is a more accurate account of history. Repeated motifs or alternative scores can create equally good local segments. **Follow-up:** add a second identical motif and inspect endpoint ambiguity.

## C. What does a composition-preserving chance model actually test?

- **Question:** Under an explicitly finite null model, how often is an identity-level score reached?
- **Hypothesis:** Only the identical order will reach the maximum six-match score under these penalties.
- **Controlled:** fixed string `AACCGG`, scores (2,-3,-2), global objective. Null draws are equally weighted distinct permutations of exactly that symbol multiset.
- **Procedure:** Enumerate all 6!/(2!2!2!)=90 distinct permutations, align each to the fixed string, and count scores >= the observed self-alignment score.
- **Actual:** observed score 12; 1/90 permutations reach it; tail fraction 0.011111111111111112. Full histogram is in raw JSON.

This is an exact finite calculation under a toy null, not an estimated biological p-value. The observed pair was deliberately chosen identical; no blind discovery or hypothesis-test claim is made. Real sequence composition, dependence, repeat structure, score selection, multiple searches, and evolutionary processes can invalidate this null. An alternative null preserving adjacent-symbol frequencies asks a different question. **Follow-up:** compare two null models on the same preselected pair before inspecting outcomes.

## D. Does the implementation show quadratic growth?

- **Question:** As both input lengths double, how do cell count, time, and allocated peak change?
- **Hypothesis:** Interior cell evaluations increase exactly fourfold; elapsed time and traced allocation should roughly follow quadratic growth within overhead limits.
- **Controlled:** deterministic repeated strings, defaults (1,-1,-1), one process, one warmup per size, five timed runs per size. CPU contention and allocator/cache state are not fully controlled.
- **Procedure/instrumentation:** n=32,64,128,256; `time.perf_counter()` for five samples; one **separate** `tracemalloc` run for peak allocations so tracing overhead is excluded from timings.

Actual run, Python 3.12.14, Linux x86-64:

| n | Evaluated cells | Median seconds | Separate traced peak bytes |
| ---: | ---: | ---: | ---: |
| 32 | 1,024 | 0.000285276 | 42,242 |
| 64 | 4,096 | 0.001124390 | 168,594 |
| 128 | 16,384 | 0.004414748 | 667,834 |
| 256 | 65,536 | 0.017493255 | 2,649,618 |

Cell counts follow the recurrence exactly; timing observations are consistent with the operation-count argument. Four sizes on one machine do not establish production throughput or universal constants. `tracemalloc` measures traced Python allocations, not total process RSS or a physical instrument. Five samples are too few for reliable tail-latency estimates. **Follow-up:** compare score-only two-row memory under the same workloads; preserve correctness checks before claiming optimization.

## What was not reproduced

No original protein comparison, SW81 example matrix, source-paper reported numerical result, genomics pipeline, clinical finding, or physical biology experiment has been reproduced. All conclusions above concern bounded synthetic algorithm behavior only.
