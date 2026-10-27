# Repeated search and incorrect-update experiments

Question: how much repeated work does memoizing the same amount remove, and can
an innocent-looking loop rewrite change the problem being solved? The hypothesis
is that memoization evaluates one state per reachable amount while repeated
search revisits amounts through different package orders. Control denominations
at1,3,4, targets4/8/12/16/20 and the same final-count objective. Count function
body executions; separately retain elapsed time. Before running, derive the
states for target4 and predict the three wrong-loop cases.

Execute `python3 algorithmic-problem-solving/topics/dynamic-programming/experiment.py`
from the root after the21-suite release tests. [observed.json](evidence/observed.json)
contains the actual2026-10-23 execution with Python/platform/source hashes.
Both searches agree with the reference's legal minimum-count witness.

| Target | Uncached calls | Memoized body evaluations | Optimal count |
| --- | --- | --- | --- |
|4|9|5|1|
|8|64|9|2|
|12|441|13|3|
|16|3025|17|4|
|20|20736|21|5|

Memoized counts include the amount0 base. Cache lookups still have a cost; a
body-evaluation count is not the total CPU instruction count. Only five small
cases were timed once. Those times cannot establish a universal speed ratio or
a production scalability boundary. Larger targets also encounter Python recursion
limits in the recursive variants, while the bottom-up reference has another
memory/cost tradeoff. A caller must choose a finite resource budget explicitly.

Actual counterexamples: amount-first counting returned3 ordered strings for
sizes1,2,target3; the declared unordered contract returned2. Ascending capacity
on one weight2,value3 item at capacity4 returned6, whereas0/1 selection returned3.
In-place edge relaxation reached vertex2 at cost−3 in a single pass over0→1→2;
the one-hop reference correctly returned unreachable. These are intentionally
incorrect variants, not failed reference tests. Their disagreement shows that
iteration order can encode resource-use constraints.

For follow-up, repeat operation counts with another denomination set and a
large numeric target, measuring memory and integer bit length separately. Try
an unreachable amount and explain its representation before comparing timings.
Retain independent witness checks, not only equal objective numbers. Nothing in
this run establishes complete algorithms coverage or a learner's unaided skill.
