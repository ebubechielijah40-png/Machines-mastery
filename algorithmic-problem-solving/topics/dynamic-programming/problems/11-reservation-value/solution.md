# Derivation: Choose compatible weighted reservations

## State, construction and correctness

With jobs sorted by end, let J[i] be best value among first i. Skip job i−1 for J[i−1], or include it for value+J[p], where p counts preceding jobs with end≤start. Binary search finds p. In any feasible solution including that job, the other jobs lie in this compatible prefix; the converse combination is feasible. Backtrack skip/take decisions to original indices.

## Failed approach and counterexample

Earliest finish time maximizes cardinality for unweighted scheduling, not weight. A job spanning(0,4) with value100 beats two short jobs worth1 each. Using end<start wrongly forbids back-to-back jobs.

## Cost and boundary

O(n log n) sort/predecessor time, O(n) table/parent/index storage. Inputs are single-resource reservations, not multicore or uncertain-duration scheduling.

The reference function is `weighted_intervals` in [the shared executable library](../../code/dp.py);
[solution.py](solution.py) exposes that implementation as `solve` without a second
copy. [The independent suite](../../code/test_dp.py) compares complete small
search spaces or alternative formulations, in addition to the local fixed-contract
test. None of these finite checks replaces the displayed general argument.

## Reconstruction and transfer

Close the implementation, derive the state/base/order again, rebuild it and write
a fresh witness/negative test. Then change the constraint named above and explain
whether the state still contains everything needed for the next decision.

These are original teaching statements for established methods; the selected
[primary-source map](../../SOURCES.md) distinguishes direct source scopes from
independently derived extensions.
