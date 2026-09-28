# Solution — Stable Compaction of Deleted Records

## 1. Problem model

An append-only staging buffer marks deleted entries with `None`. Before flushing to disk, remove tombstones while preserving the relative order of live records. The algorithmic task is: Mutate `values` so all non-None entries occupy the prefix in original order. Fill the remaining suffix with `None` and return the number of live entries.

## 2. Baseline / brute-force approach

Build a new list of live values and then append the required number of tombstones. O(n) time and O(n) extra space.

Why keep the baseline? Because optimization without a correct reference makes it harder to distinguish a faster implementation from a subtly wrong one. For small random inputs, the tests can compare the optimized implementation to a direct oracle.

## 3. Better / target approach

Use a write index. Scan each item once; when it is live, write it at the next prefix slot. Then overwrite the suffix with None. This is stable, O(n) time and O(1) auxiliary space.

## 4. Derivation

Start from the output condition and ask what must already be known when each position is finalized. The target method avoids recomputing information that can be maintained incrementally or encoded directly in the array. This reduces repeated work while preserving the exact contract.

## 5. Invariant and correctness

**Invariant:** Before processing input index i, `values[:write]` equals exactly the live elements originally seen in `values[:i]`, in the same order.

Initialization establishes the invariant before useful work has been finalized. Each loop transition preserves it by changing only the region/state whose contract is known. When the loop terminates, no unknown region remains, so the required postcondition follows. The executable tests include exhaustive or oracle-based checks on bounded small inputs where practical.

## 6. Complexity

Use a write index. Scan each item once; when it is live, write it at the next prefix slot. Then overwrite the suffix with None. This is stable, O(n) time and O(1) auxiliary space. Complexity claims refer to the number of abstract operations under a RAM-style cost model; they are not claims about exact wall-clock latency. Language overhead, caches, allocation and input distribution can dominate at small sizes.

## 7. Common wrong approach

Call `remove(None)` repeatedly. Each deletion shifts the remaining suffix, leading to quadratic behavior in tombstone-heavy arrays.

## 8. Implementation

```python
def compact_active(values):
    write=0
    for x in list(values):
        if x is not None:
            values[write]=x
            write+=1
    for i in range(write,len(values)):
        values[i]=None
    return write
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

Log compaction, garbage collection, packed columnar buffers and GPU work queues all repeatedly convert sparse logical occupancy into dense storage. A production implementation would still need workload-specific measurement, input validation, memory accounting and failure behavior. This exercise establishes the algorithmic mechanism, not a production service.

## 11. Transfer questions

1. Which part of the invariant would fail if input arrived as an unbounded stream?
2. Can the algorithm be parallelized without changing the result? What state would workers need to exchange?
3. What benchmark would distinguish asymptotic improvement from a constant-factor regression?
4. Which malformed inputs should a production boundary reject rather than silently reinterpret?
