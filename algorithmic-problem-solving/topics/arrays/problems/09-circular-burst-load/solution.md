# Solution — Maximum Burst in a Circular Buffer

## 1. Problem model

A periodic telemetry buffer wraps at midnight. The strongest contiguous burst may cross the physical end of the array. The algorithmic task is: Return the maximum sum of a non-empty contiguous segment in a circular array.

## 2. Baseline / brute-force approach

Duplicate the array and enumerate wrapped intervals whose length is at most n, which is O(n^2) with careful bounding.

Why keep the baseline? Because optimization without a correct reference makes it harder to distinguish a faster implementation from a subtly wrong one. For small random inputs, the tests can compare the optimized implementation to a direct oracle.

## 3. Better / target approach

The best segment is either ordinary non-wrapping max-subarray, or total sum minus the minimum non-empty subarray. Handle the all-negative case separately. O(n).

## 4. Derivation

Start from the output condition and ask what must already be known when each position is finalized. The target method avoids recomputing information that can be maintained incrementally or encoded directly in the array. This reduces repeated work while preserving the exact contract.

## 5. Invariant and correctness

**Invariant:** Any wrapped segment is the complement of one contiguous excluded middle segment, so maximizing wrapped sum equals minimizing the excluded segment when at least one element remains.

Initialization establishes the invariant before useful work has been finalized. Each loop transition preserves it by changing only the region/state whose contract is known. When the loop terminates, no unknown region remains, so the required postcondition follows. The executable tests include exhaustive or oracle-based checks on bounded small inputs where practical.

## 6. Complexity

The best segment is either ordinary non-wrapping max-subarray, or total sum minus the minimum non-empty subarray. Handle the all-negative case separately. O(n). Complexity claims refer to the number of abstract operations under a RAM-style cost model; they are not claims about exact wall-clock latency. Language overhead, caches, allocation and input distribution can dominate at small sizes.

## 7. Common wrong approach

Always return `total - min_subarray`. For all-negative input that chooses the empty complement, which violates the non-empty requirement.

## 8. Implementation

```python
def max_circular_subarray_sum(values):
    if not values:
        raise ValueError("non-empty input required")
    total=sum(values)
    max_end=max_all=values[0]
    min_end=min_all=values[0]
    for x in values[1:]:
        max_end=max(x,max_end+x); max_all=max(max_all,max_end)
        min_end=min(x,min_end+x); min_all=min(min_all,min_end)
    if max_all < 0:
        return max_all
    return max(max_all,total-min_all)
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

Circular storage and ring buffers turn physical boundaries into an implementation detail. Reasoning by complements often simplifies wraparound algorithms. A production implementation would still need workload-specific measurement, input validation, memory accounting and failure behavior. This exercise establishes the algorithmic mechanism, not a production service.

## 11. Transfer questions

1. Which part of the invariant would fail if input arrived as an unbounded stream?
2. Can the algorithm be parallelized without changing the result? What state would workers need to exchange?
3. What benchmark would distinguish asymptotic improvement from a constant-factor regression?
4. Which malformed inputs should a production boundary reject rather than silently reinterpret?
