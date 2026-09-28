# Solution — Next Lexicographic Schedule

## 1. Problem model

A deterministic test harness enumerates unique orderings of worker IDs in lexicographic order. Generate the next ordering without sorting every permutation globally. The algorithmic task is: Transform `values` in place into the next lexicographically greater permutation. If none exists, transform it into the smallest permutation. Return `True` if a greater permutation existed, else `False`.

## 2. Baseline / brute-force approach

Generate all permutations, deduplicate, sort them and locate the current one. This is factorial time and space.

Why keep the baseline? Because optimization without a correct reference makes it harder to distinguish a faster implementation from a subtly wrong one. For small random inputs, the tests can compare the optimized implementation to a direct oracle.

## 3. Better / target approach

Find the longest non-increasing suffix, swap its predecessor with the rightmost larger element, then reverse the suffix. O(n) time, O(1) auxiliary space.

## 4. Derivation

Start from the output condition and ask what must already be known when each position is finalized. The target method avoids recomputing information that can be maintained incrementally or encoded directly in the array. This reduces repeated work while preserving the exact contract.

## 5. Invariant and correctness

**Invariant:** The maximal suffix is already the greatest arrangement for its fixed prefix. The smallest possible increase is therefore at the pivot, followed by the smallest suffix arrangement.

Initialization establishes the invariant before useful work has been finalized. Each loop transition preserves it by changing only the region/state whose contract is known. When the loop terminates, no unknown region remains, so the required postcondition follows. The executable tests include exhaustive or oracle-based checks on bounded small inputs where practical.

## 6. Complexity

Find the longest non-increasing suffix, swap its predecessor with the rightmost larger element, then reverse the suffix. O(n) time, O(1) auxiliary space. Complexity claims refer to the number of abstract operations under a RAM-style cost model; they are not claims about exact wall-clock latency. Language overhead, caches, allocation and input distribution can dominate at small sizes.

## 7. Common wrong approach

Swap the last two elements that differ. That does not guarantee the smallest greater permutation.

## 8. Implementation

```python
def next_permutation(values):
    n=len(values)
    if n<2:
        return False
    i=n-2
    while i>=0 and values[i] >= values[i+1]:
        i-=1
    if i<0:
        values.reverse(); return False
    j=n-1
    while values[j] <= values[i]:
        j-=1
    values[i],values[j]=values[j],values[i]
    values[i+1:]=reversed(values[i+1:])
    return True
```

The runnable copy is `solution.py`; tests import that file directly.

## 9. Edge cases to reason through

- Empty input where the contract permits it.
- Minimum-size non-empty input.
- Duplicate values.
- Already-final input.
- Reverse/adversarial ordering when relevant.
- Extreme values allowed by the contract.

## 10. Real-world application and limits

This is useful for exhaustive test generation and exposes lexicographic ordering as a state-transition system rather than a sorting problem. A production implementation would still need workload-specific measurement, input validation, memory accounting and failure behavior. This exercise establishes the algorithmic mechanism, not a production service.

## 11. Transfer questions

1. Which part of the invariant would fail if input arrived as an unbounded stream?
2. Can the algorithm be parallelized without changing the result? What state would workers need to exchange?
3. What benchmark would distinguish asymptotic improvement from a constant-factor regression?
4. Which malformed inputs should a production boundary reject rather than silently reinterpret?
