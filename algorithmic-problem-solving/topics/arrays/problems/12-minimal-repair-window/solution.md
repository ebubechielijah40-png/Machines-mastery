# Solution — Find the Minimal Repair Window

## 1. Problem model

A mostly sorted SSTable run was corrupted by one bounded reorder. Find the smallest contiguous interval that must be sorted to restore global order. The algorithmic task is: Return `(left,right)` for the smallest subarray which, if sorted, makes the entire array nondecreasing. Return `(-1,-1)` if already sorted.

## 2. Baseline / brute-force approach

Sort a copy and find the first/last positions where it differs from the input. O(n log n) time and O(n) space.

Why keep the baseline? Because optimization without a correct reference makes it harder to distinguish a faster implementation from a subtly wrong one. For small random inputs, the tests can compare the optimized implementation to a direct oracle.

## 3. Better / target approach

Find the first descent from left and right, compute min/max within that provisional window, then expand boundaries while outside values violate those extrema. O(n) time, O(1) extra space.

## 4. Derivation

Start from the output condition and ask what must already be known when each position is finalized. The target method avoids recomputing information that can be maintained incrementally or encoded directly in the array. This reduces repeated work while preserving the exact contract.

## 5. Invariant and correctness

**Invariant:** After expansion, every value left of `left` is <= the window minimum and every value right of `right` is >= the window maximum, so sorting only the window suffices.

Initialization establishes the invariant before useful work has been finalized. Each loop transition preserves it by changing only the region/state whose contract is known. When the loop terminates, no unknown region remains, so the required postcondition follows. The executable tests include exhaustive or oracle-based checks on bounded small inputs where practical.

## 6. Complexity

Find the first descent from left and right, compute min/max within that provisional window, then expand boundaries while outside values violate those extrema. O(n) time, O(1) extra space. Complexity claims refer to the number of abstract operations under a RAM-style cost model; they are not claims about exact wall-clock latency. Language overhead, caches, allocation and input distribution can dominate at small sizes.

## 7. Common wrong approach

Return only the region between the first left descent and first right ascent. A small value inside may need to move further left, or a large value further right.

## 8. Implementation

```python
def minimal_sort_window(values):
    n=len(values)
    if n<2:
        return (-1,-1)
    l=0
    while l<n-1 and values[l] <= values[l+1]: l+=1
    if l==n-1: return (-1,-1)
    r=n-1
    while r>0 and values[r-1] <= values[r]: r-=1
    wmin=min(values[l:r+1]); wmax=max(values[l:r+1])
    while l>0 and values[l-1] > wmin: l-=1
    while r<n-1 and values[r+1] < wmax: r+=1
    return (l,r)
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

Localized repair is common in sorted-file maintenance and data validation: diagnose the smallest inconsistent region instead of rewriting the whole dataset. A production implementation would still need workload-specific measurement, input validation, memory accounting and failure behavior. This exercise establishes the algorithmic mechanism, not a production service.

## 11. Transfer questions

1. Which part of the invariant would fail if input arrived as an unbounded stream?
2. Can the algorithm be parallelized without changing the result? What state would workers need to exchange?
3. What benchmark would distinguish asymptotic improvement from a constant-factor regression?
4. Which malformed inputs should a production boundary reject rather than silently reinterpret?
