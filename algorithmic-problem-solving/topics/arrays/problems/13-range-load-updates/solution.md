# Solution — Apply Bulk Range Load Updates

## 1. Problem model

A capacity planner receives many updates saying “add delta to every minute in [start,end]”. Applying each update cell-by-cell is too slow. The algorithmic task is: Given array length n and inclusive updates `(start,end,delta)`, return the final values after all updates. Initially every position is zero.

## 2. Baseline / brute-force approach

For every update loop through every covered index. Worst case O(n*q).

Why keep the baseline? Because optimization without a correct reference makes it harder to distinguish a faster implementation from a subtly wrong one. For small random inputs, the tests can compare the optimized implementation to a direct oracle.

## 3. Better / target approach

Record only boundary changes in a difference array: +delta at start, -delta after end, then prefix-sum once. O(n+q) time.

## 4. Derivation

Start from the output condition and ask what must already be known when each position is finalized. The target method avoids recomputing information that can be maintained incrementally or encoded directly in the array. This reduces repeated work while preserving the exact contract.

## 5. Invariant and correctness

**Invariant:** The running prefix sum at index i equals the sum of deltas from exactly those ranges whose start has occurred and whose end has not passed.

Initialization establishes the invariant before useful work has been finalized. Each loop transition preserves it by changing only the region/state whose contract is known. When the loop terminates, no unknown region remains, so the required postcondition follows. The executable tests include exhaustive or oracle-based checks on bounded small inputs where practical.

## 6. Complexity

Record only boundary changes in a difference array: +delta at start, -delta after end, then prefix-sum once. O(n+q) time. Complexity claims refer to the number of abstract operations under a RAM-style cost model; they are not claims about exact wall-clock latency. Language overhead, caches, allocation and input distribution can dominate at small sizes.

## 7. Common wrong approach

Store only the start increments without the end cancellation. Effects then incorrectly continue through the rest of the array.

## 8. Implementation

```python
def apply_range_deltas(n, updates):
    if n<0: raise ValueError("n must be nonnegative")
    diff=[0]*(n+1)
    for start,end,delta in updates:
        if not (0<=start<=end<n): raise ValueError("invalid range")
        diff[start]+=delta
        if end+1<n: diff[end+1]-=delta
    out=[]; cur=0
    for i in range(n):
        cur+=diff[i]; out.append(cur)
    return out
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

Difference arrays model batched counters, reservation windows and offline range updates. They are the discrete derivative/integral pair of prefix sums. A production implementation would still need workload-specific measurement, input validation, memory accounting and failure behavior. This exercise establishes the algorithmic mechanism, not a production service.

## 11. Transfer questions

1. Which part of the invariant would fail if input arrived as an unbounded stream?
2. Can the algorithm be parallelized without changing the result? What state would workers need to exchange?
3. What benchmark would distinguish asymptotic improvement from a constant-factor regression?
4. Which malformed inputs should a production boundary reject rather than silently reinterpret?
