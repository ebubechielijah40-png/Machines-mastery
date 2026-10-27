# Derivation: Count monotone routes around blocked cells

## State, construction and correctness

P[r,c] is number of routes ending at that cell. A nonstart unblocked cell receives disjoint route sets from above and left, so add their counts; blocked cells have0. Initialize the start contribution once, then propagate row-major. In the rolling array, ways[c] is the previous-row count and ways[c−1] is already the current-row count.

## Failed approach and counterexample

Failing to overwrite a blocked cell with0 lets paths pass through it. Allowing up/left moves introduces cycles and destroys this finite topological recurrence.

## Cost and boundary

O(RC) integer additions, O(C) cells. Counts can have many bits. Rectangular shape and actual bool flags are checked before recurrence evaluation.

The reference function is `grid_paths` in [the shared executable library](../../code/dp.py);
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
