# Derivation: Cut a reversible-symbol log into palindromes

## State, construction and correctness

P[i,j] holds when endpoint symbols agree and the interior is palindromic, with length1/2 bases. Fill decreasing i. Q[j] is minimum number of palindrome pieces in text[:j]. For each palindromic final interval[i,j), Q[j]≤Q[i]+1, and every valid partition has such a final piece. Minimize candidates with Q[0]=0. For nonempty text cuts=pieces−1.

## Failed approach and counterexample

Choosing the longest palindrome beginning at the current position can block a better later partition. Counting pieces directly returns1 for an already-palindromic string, but it needs0 cuts.

## Cost and boundary

O(n²) time and O(n²) palindrome storage plus O(n) piece/parent cells. Unicode code points are the unit; no biological sequence symmetry is implied.

The reference function is `palindrome_cuts` in [the shared executable library](../../code/dp.py);
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
