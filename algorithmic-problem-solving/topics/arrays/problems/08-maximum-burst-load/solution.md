# Solution — Maximum Contiguous Burst Load

## 1. Problem model

Per-minute load deltas may be positive or negative. Find the contiguous interval with the largest net increase to identify the strongest burst. The algorithmic task is: Return the maximum sum of any non-empty contiguous subarray.

## 2. Baseline / brute-force approach

Enumerate all O(n^2) intervals and maintain running sums.

Why keep the baseline? Because optimization without a correct reference makes it harder to distinguish a faster implementation from a subtly wrong one. For small random inputs, the tests can compare the optimized implementation to a direct oracle.

## 3. Better / target approach

Kadane's recurrence: the best interval ending at i either starts at i or extends the best ending at i-1. O(n) time, O(1) space.

## 4. Derivation

Every nonempty interval ending at i either contains only values[i], or extends an interval ending at i−1. Among extensions, adding the same values[i] preserves ordering of sums. Therefore ending_i=max(values[i],ending_(i−1)+values[i]). The maximum over all ending_i covers every possible right endpoint. For [-3,-2], initialization at −3 and then max(−2,−5)=−2 preserves the nonempty requirement; initializing zero would invent an empty interval.

## 5. Invariant and correctness

**Invariant:** `ending` is the maximum sum of a non-empty subarray whose right endpoint is the current position; `best` is the maximum over all endpoints seen.

Initialization establishes the invariant before useful work has been finalized. Each loop transition preserves it by changing only the region/state whose contract is known. When the loop terminates, no unknown region remains, so the required postcondition follows. The executable tests include exhaustive or oracle-based checks on bounded small inputs where practical.

## 6. Complexity

Kadane's recurrence: the best interval ending at i either starts at i or extends the best ending at i-1. O(n) time, O(1) space. Complexity claims refer to the number of abstract operations under a RAM-style cost model; they are not claims about exact wall-clock latency. Language overhead, caches, allocation and input distribution can dominate at small sizes.

## 7. Common wrong approach

Reset every negative running total to zero and initialize best to zero. That incorrectly returns zero for all-negative arrays when the required interval is non-empty.

## 8. Implementation

```python
def max_subarray_sum(values):
    if not values:
        raise ValueError("non-empty input required")
    ending=best=values[0]
    for i in range(1, len(values)):
        x = values[i]
        ending=max(x, ending+x)
        best=max(best, ending)
    return best
```

The runnable copy is `solution.py`; tests import that file directly. Indexed iteration avoids allocating `values[1:]`, which would copy O(n) references for a Python list. The constant-space claim counts a fixed number of numeric registers under the stated RAM model; arbitrary-precision integer bit storage can grow with numeric magnitude.

## 9. Edge cases to reason through

- Empty input where the contract permits it.
- Minimum-size non-empty input.
- Duplicate values.
- Already-final input.
- Reverse/adversarial ordering when relevant.
- Extreme values allowed by the contract.

## 10. Real-world application and limits

This models burst detection, profit/loss windows and score accumulation. The important idea is dynamic state compression: a whole set of candidate intervals collapses to one sufficient statistic. A production implementation would still need workload-specific measurement, input validation, memory accounting and failure behavior. This exercise establishes the algorithmic mechanism, not a production service.

## 11. Transfer questions

1. Which part of the invariant would fail if input arrived as an unbounded stream?
2. Can the algorithm be parallelized without changing the result? What state would workers need to exchange?
3. What benchmark would distinguish asymptotic improvement from a constant-factor regression?
4. Which malformed inputs should a production boundary reject rather than silently reinterpret?
