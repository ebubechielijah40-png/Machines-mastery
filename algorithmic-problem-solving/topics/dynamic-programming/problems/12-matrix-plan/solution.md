# Derivation: Plan a dense matrix multiplication chain

## State, construction and correctness

M[i,j] is minimum cost of matrices i…j−1. Base M[i,i+1]=0. Split at k to pay M[i,k]+M[k,j]+d[i]d[k]d[j]. Every binary parenthesization has exactly one outer split, and independently replacing either side by a cheaper valid plan improves the total. Evaluate increasing interval lengths so both children are ready; save k for reconstruction.

## Failed approach and counterexample

Choosing the cheapest adjacent multiplication first need not minimize total work. Associativity preserves mathematical results but floating-point rounding can differ; this contract optimizes arithmetic count only.

## Cost and boundary

O(n³) scalar-cost operations, O(n²) tables and O(n) plan output. Actual matrix entries are never multiplied, so no measured BLAS performance is implied.

The reference function is `matrix_chain` in [the shared executable library](../../code/dp.py);
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
