# Derivation: Minimum standard packages

## State, construction and correctness

Let M[t] be minimum package count for total t. M[0]=0; other initially unreachable. Every nonempty filling ends with some c, giving M[t]=1+min M[t−c] over reachable remainders. Conversely, appending c to such a filling is feasible. Induction on t proves optimality because c>0. Store the chosen c separately; reconstruct while the remaining amount decreases.

## Failed approach and counterexample

Largest-first selects4+1+1 for6, but3+3 is better. Zero or negative denominations break the decreasing-state argument and are rejected.

## Cost and boundary

O(Td) arithmetic operations plus denomination sorting; O(T) table/parent storage and output length at most T/min(coins). The input bit length of T is logarithmic, so this is pseudopolynomial.

The reference function is `min_coins` in [the shared executable library](../../code/dp.py);
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
