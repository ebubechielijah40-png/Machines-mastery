# Derivation: Find a cheapest route with a hop budget

## State, construction and correctness

D[k,v] is the minimum cost of a walk reaching v with exactly k edges. Initialize D[0,source]=0 and others unreachable. Every k-edge walk ends in edge(u,v), so relax from D[k−1,u]+w(u,v). No current-layer value may feed another transition. Compare target costs across k=0…budget; reconstruct predecessor vertices using decreasing k.

## Failed approach and counterexample

Updating one distance array in-place may traverse several edges during one budget step. A negative cycle does not imply unbounded cost with a finite hop limit; discarding all repeated vertices changes the problem.

## Cost and boundary

O(H(V+E)) time with full layer initialization, O(HV) retained layers/parents in this implementation, plus O(H) output. Edge-list storage is additional O(E).

The reference function is `bounded_route` in [the shared executable library](../../code/dp.py);
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
