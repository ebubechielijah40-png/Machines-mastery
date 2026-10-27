# Derivation: Choose a minimum-cost monotone inspection route

## State, construction and correctness

C[r,c] is current cell cost plus the smaller reachable predecessor cost. Since right/down increase r+c, all predecessor optima are final before this state. Replacing any nonoptimal prefix would improve a candidate route, so the recurrence is both feasible and optimal. A parent coordinate stores the selected predecessor; backtracking stops at the start.

## Failed approach and counterexample

Always choosing the cheaper next cell is not globally valid: a locally cheap branch may lead to expensive later cells. Forgetting the start cost changes the declared objective.

## Cost and boundary

O(RC) time/state including parents and O(R+C) path output. This implementation prioritizes inspectable reconstruction over rolling-memory optimization.

The reference function is `grid_cost` in [the shared executable library](../../code/dp.py);
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
