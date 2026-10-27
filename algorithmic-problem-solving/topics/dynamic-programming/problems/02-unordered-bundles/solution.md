# Derivation: Count unordered replenishment bundles

## State, construction and correctness

After processing c, ways[t] counts bundles using only denominations no larger than c. Bundles without c retain the old count; removing one c gives a bijection from bundles with c to bundles for t−c in the current layer. Increasing totals permit repeated c. Processing denominations outside totals fixes one canonical order for every multiplicity vector.

## Failed approach and counterexample

With total outside the denomination loop,1+2 and2+1 are counted separately: the answer for3 becomes3. Duplicate denomination records also cause overcounting and are rejected.

## Cost and boundary

O(Td) additions and O(T) integer cells. Counts can grow far beyond a machine word; bit arithmetic is not constant-time.

The reference function is `coin_combinations` in [the shared executable library](../../code/dp.py);
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
