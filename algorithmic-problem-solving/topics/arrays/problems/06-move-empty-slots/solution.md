# Solution — Move Empty Slots to the End

## 1. Problem model

A numeric work buffer uses zero to mean an unused slot. Compact active values toward the front without reordering them. The algorithmic task is: Move all zero values to the end in place while preserving the order of nonzero values. Return the list.

## 2. Baseline / brute-force approach

Construct `[x for x in values if x != 0] + [0]*count`. O(n) time and O(n) extra memory.

Why keep the baseline? Because optimization without a correct reference makes it harder to distinguish a faster implementation from a subtly wrong one. For small random inputs, the tests can compare the optimized implementation to a direct oracle.

## 3. Better / target approach

Use a write pointer for nonzero values, then zero-fill the suffix. O(n) time and O(1) auxiliary space.

## 4. Derivation

Start from the output condition and ask what must already be known when each position is finalized. The target method avoids recomputing information that can be maintained incrementally or encoded directly in the array. This reduces repeated work while preserving the exact contract.

## 5. Invariant and correctness

**Invariant:** After scanning i items, the prefix `values[:write]` contains exactly the nonzero values from the original first i items in original order.

Initialization establishes the invariant before useful work has been finalized. Each loop transition preserves it by changing only the region/state whose contract is known. When the loop terminates, no unknown region remains, so the required postcondition follows. The executable tests include exhaustive or oracle-based checks on bounded small inputs where practical.

## 6. Complexity

Use a write pointer for nonzero values, then zero-fill the suffix. O(n) time and O(1) auxiliary space. Complexity claims refer to the number of abstract operations under a RAM-style cost model; they are not claims about exact wall-clock latency. Language overhead, caches, allocation and input distribution can dominate at small sizes.

## 7. Common wrong approach

Swap each zero with the next nonzero found by a fresh forward search; repeated rescans can be quadratic.

## 8. Implementation

```python
def move_zeros(values):
    write=0
    for x in values:
        if x!=0:
            values[write]=x; write+=1
    for i in range(write,len(values)):
        values[i]=0
    return values
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

Stable compaction is common in vectorized execution engines, sparse buffers and work queues. It also exposes the difference between logical deletion and physical movement. A production implementation would still need workload-specific measurement, input validation, memory accounting and failure behavior. This exercise establishes the algorithmic mechanism, not a production service.

## 11. Transfer questions

1. Which part of the invariant would fail if input arrived as an unbounded stream?
2. Can the algorithm be parallelized without changing the result? What state would workers need to exchange?
3. What benchmark would distinguish asymptotic improvement from a constant-factor regression?
4. Which malformed inputs should a production boundary reject rather than silently reinterpret?
