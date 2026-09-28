# Solution — Select the k-th Latency Without Full Sorting

## 1. Problem model

A diagnostic tool needs one order statistic from a large latency sample. Full sorting does more work than necessary when only one rank is requested. The algorithmic task is: Return the k-th smallest value using zero-based k. The function may mutate the input. Reject invalid k.

## 2. Baseline / brute-force approach

Sort all n values and index k: O(n log n).

Why keep the baseline? Because optimization without a correct reference makes it harder to distinguish a faster implementation from a subtly wrong one. For small random inputs, the tests can compare the optimized implementation to a direct oracle.

## 3. Better / target approach

Quickselect partitions around a pivot and continues only into the side containing rank k. Expected O(n) time, O(1) auxiliary space; worst-case O(n^2) for adversarial pivot choices.

## 4. Derivation

Start from the output condition and ask what must already be known when each position is finalized. The target method avoids recomputing information that can be maintained incrementally or encoded directly in the array. This reduces repeated work while preserving the exact contract.

## 5. Invariant and correctness

**Invariant:** After partition, every element before pivot position p is <= pivot and every element after p is > pivot for this Lomuto variant; therefore if p==k the answer is fixed.

Initialization establishes the invariant before useful work has been finalized. Each loop transition preserves it by changing only the region/state whose contract is known. When the loop terminates, no unknown region remains, so the required postcondition follows. The executable tests include exhaustive or oracle-based checks on bounded small inputs where practical.

## 6. Complexity

Quickselect partitions around a pivot and continues only into the side containing rank k. Expected O(n) time, O(1) auxiliary space; worst-case O(n^2) for adversarial pivot choices. Complexity claims refer to the number of abstract operations under a RAM-style cost model; they are not claims about exact wall-clock latency. Language overhead, caches, allocation and input distribution can dominate at small sizes.

## 7. Common wrong approach

Claim deterministic O(n) while always choosing the final element as pivot. Adversarial sorted inputs make that strategy quadratic.

## 8. Implementation

```python
def kth_smallest(values,k):
    if not 0<=k<len(values): raise IndexError("k out of range")
    lo=0; hi=len(values)-1
    while True:
        pivot=values[hi]; p=lo
        for i in range(lo,hi):
            if values[i] <= pivot:
                values[p],values[i]=values[i],values[p]; p+=1
        values[p],values[hi]=values[hi],values[p]
        if p==k: return values[p]
        if p<k: lo=p+1
        else: hi=p-1
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

Percentiles and order statistics are common in observability systems. Production implementations often use streaming sketches instead when the full sample cannot be retained. A production implementation would still need workload-specific measurement, input validation, memory accounting and failure behavior. This exercise establishes the algorithmic mechanism, not a production service.

## 11. Transfer questions

1. Which part of the invariant would fail if input arrived as an unbounded stream?
2. Can the algorithm be parallelized without changing the result? What state would workers need to exchange?
3. What benchmark would distinguish asymptotic improvement from a constant-factor regression?
4. Which malformed inputs should a production boundary reject rather than silently reinterpret?
