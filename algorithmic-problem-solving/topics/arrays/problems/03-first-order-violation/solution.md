# Solution — Find the First Ordering Violation

## 1. Problem model

A storage engine expects a batch to be nondecreasing by timestamp before bulk-loading it into an ordered index. Detect the first adjacent pair that violates that contract. The algorithmic task is: Return the smallest index `i` such that `values[i] > values[i+1]`. Return -1 when the array is nondecreasing.

## 2. Baseline / brute-force approach

Sort a copy and compare it to the input. This can detect disorder but costs O(n log n) and does not directly identify the earliest local violation.

Why keep the baseline? Because optimization without a correct reference makes it harder to distinguish a faster implementation from a subtly wrong one. For small random inputs, the tests can compare the optimized implementation to a direct oracle.

## 3. Better / target approach

Scan adjacent pairs once and stop at the first descent. O(n) worst-case time and O(1) space.

## 4. Derivation

Start from the output condition and ask what must already be known when each position is finalized. The target method avoids recomputing information that can be maintained incrementally or encoded directly in the array. This reduces repeated work while preserving the exact contract.

## 5. Invariant and correctness

**Invariant:** All adjacent pairs before the current index have already satisfied `values[j] <= values[j+1]`; therefore the first failing pair is globally the earliest one.

Initialization establishes the invariant before useful work has been finalized. Each loop transition preserves it by changing only the region/state whose contract is known. When the loop terminates, no unknown region remains, so the required postcondition follows. The executable tests include exhaustive or oracle-based checks on bounded small inputs where practical.

## 6. Complexity

Scan adjacent pairs once and stop at the first descent. O(n) worst-case time and O(1) space. Complexity claims refer to the number of abstract operations under a RAM-style cost model; they are not claims about exact wall-clock latency. Language overhead, caches, allocation and input distribution can dominate at small sizes.

## 7. Common wrong approach

Compare every element against every later element. That proves global order but wastes O(n^2) comparisons.

## 8. Implementation

```python
def first_descent(values):
    for i in range(len(values)-1):
        if values[i] > values[i+1]:
            return i
    return -1
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

Sorted-run validation appears before merge operations, index construction, event-time processing and binary-search based query paths. A production implementation would still need workload-specific measurement, input validation, memory accounting and failure behavior. This exercise establishes the algorithmic mechanism, not a production service.

## 11. Transfer questions

1. Which part of the invariant would fail if input arrived as an unbounded stream?
2. Can the algorithm be parallelized without changing the result? What state would workers need to exchange?
3. What benchmark would distinguish asymptotic improvement from a constant-factor regression?
4. Which malformed inputs should a production boundary reject rather than silently reinterpret?
