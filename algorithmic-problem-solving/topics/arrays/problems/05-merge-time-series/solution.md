# Solution — Merge Two Sorted Time Series

## 1. Problem model

Two shards emit records already sorted by timestamp. A downstream stage needs one globally sorted sequence while preserving duplicates. The algorithmic task is: Given two sorted lists, return one sorted list containing all values from both.

## 2. Baseline / brute-force approach

Concatenate the lists and sort the result, costing O((n+m) log(n+m)).

Why keep the baseline? Because optimization without a correct reference makes it harder to distinguish a faster implementation from a subtly wrong one. For small random inputs, the tests can compare the optimized implementation to a direct oracle.

## 3. Better / target approach

Use two cursors and repeatedly consume the smaller current item. O(n+m) time and O(n+m) output space.

## 4. Derivation

Start from the output condition and ask what must already be known when each position is finalized. The target method avoids recomputing information that can be maintained incrementally or encoded directly in the array. This reduces repeated work while preserving the exact contract.

## 5. Invariant and correctness

**Invariant:** The output is sorted and contains exactly the smallest `i+j` elements from the consumed prefixes `a[:i]` and `b[:j]`.

Initialization establishes the invariant before useful work has been finalized. Each loop transition preserves it by changing only the region/state whose contract is known. When the loop terminates, no unknown region remains, so the required postcondition follows. The executable tests include exhaustive or oracle-based checks on bounded small inputs where practical.

## 6. Complexity

Use two cursors and repeatedly consume the smaller current item. O(n+m) time and O(n+m) output space. Complexity claims refer to the number of abstract operations under a RAM-style cost model; they are not claims about exact wall-clock latency. Language overhead, caches, allocation and input distribution can dominate at small sizes.

## 7. Common wrong approach

Perform repeated insertion into the middle of one Python list. Insertions shift suffixes and can become quadratic.

## 8. Implementation

```python
def merge_sorted(a,b):
    i=j=0; out=[]
    while i<len(a) and j<len(b):
        if a[i] <= b[j]:
            out.append(a[i]); i+=1
        else:
            out.append(b[j]); j+=1
    out.extend(a[i:]); out.extend(b[j:])
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

This is the merge primitive behind merge sort, LSM-tree compaction, ordered stream fusion and external sorting. A production implementation would still need workload-specific measurement, input validation, memory accounting and failure behavior. This exercise establishes the algorithmic mechanism, not a production service.

## 11. Transfer questions

1. Which part of the invariant would fail if input arrived as an unbounded stream?
2. Can the algorithm be parallelized without changing the result? What state would workers need to exchange?
3. What benchmark would distinguish asymptotic improvement from a constant-factor regression?
4. Which malformed inputs should a production boundary reject rather than silently reinterpret?
