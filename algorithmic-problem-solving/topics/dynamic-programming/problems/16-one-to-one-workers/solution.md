# Derivation: Minimum-cost one-to-one assignment

## State, construction and correctness

A[mask] is minimum cost for the first popcount(mask) workers using exactly those jobs. Assign the next worker to any unset bit j, producing mask∪{j}. Every complete assignment has a unique sequence of these job additions; the sum accumulated is its cost. A[0]=0 and increasing numeric masks visit each proper-subset dependency first. Save the previous mask and job for backtracking.

## Failed approach and counterexample

Choosing the cheapest remaining job greedily fails: [[1,2],[1,100]] should give jobs(1,0),cost3, not101. This is an exponential teaching method; it does not replace polynomial assignment algorithms for large n.

## Cost and boundary

O(n2^n) transitions and O(2^n) states/parents. The hard n≤16 bound prevents accidentally treating the method as scalable.

The reference function is `assignment` in [the shared executable library](../../code/dp.py);
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
