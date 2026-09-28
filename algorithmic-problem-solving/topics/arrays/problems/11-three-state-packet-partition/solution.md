# Solution — Partition Three Packet States

## 1. Problem model

A packet inspection pipeline labels packets 0=drop, 1=inspect, 2=forward. Group the states in one pass before handing ranges to specialized workers. The algorithmic task is: Sort an array containing only 0, 1 and 2 in place using O(1) auxiliary space.

## 2. Baseline / brute-force approach

Use a general O(n log n) sort.

Why keep the baseline? Because optimization without a correct reference makes it harder to distinguish a faster implementation from a subtly wrong one. For small random inputs, the tests can compare the optimized implementation to a direct oracle.

## 3. Better / target approach

Maintain three regions with low/current/high pointers: finalized zeros, unknown middle, finalized twos. Each inspection moves one boundary. O(n) time.

## 4. Derivation

Start from the output condition and ask what must already be known when each position is finalized. The target method avoids recomputing information that can be maintained incrementally or encoded directly in the array. This reduces repeated work while preserving the exact contract.

## 5. Invariant and correctness

**Invariant:** At every step: indices < low are 0; low..mid-1 are 1; mid..high are unknown; > high are 2.

Initialization establishes the invariant before useful work has been finalized. Each loop transition preserves it by changing only the region/state whose contract is known. When the loop terminates, no unknown region remains, so the required postcondition follows. The executable tests include exhaustive or oracle-based checks on bounded small inputs where practical.

## 6. Complexity

Maintain three regions with low/current/high pointers: finalized zeros, unknown middle, finalized twos. Each inspection moves one boundary. O(n) time. Complexity claims refer to the number of abstract operations under a RAM-style cost model; they are not claims about exact wall-clock latency. Language overhead, caches, allocation and input distribution can dominate at small sizes.

## 7. Common wrong approach

After swapping a 2 with `high`, increment mid immediately. The incoming value from the high end has not been classified and must be reexamined.

## 8. Implementation

```python
def dutch_flag(values):
    low=mid=0; high=len(values)-1
    while mid<=high:
        if values[mid]==0:
            values[low],values[mid]=values[mid],values[low]; low+=1; mid+=1
        elif values[mid]==1:
            mid+=1
        elif values[mid]==2:
            values[mid],values[high]=values[high],values[mid]; high-=1
        else:
            raise ValueError("only 0,1,2 allowed")
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

Multiway partitioning appears in quicksort variants, memory allocators, packet classification and work-queue bucketing. A production implementation would still need workload-specific measurement, input validation, memory accounting and failure behavior. This exercise establishes the algorithmic mechanism, not a production service.

## 11. Transfer questions

1. Which part of the invariant would fail if input arrived as an unbounded stream?
2. Can the algorithm be parallelized without changing the result? What state would workers need to exchange?
3. What benchmark would distinguish asymptotic improvement from a constant-factor regression?
4. Which malformed inputs should a production boundary reject rather than silently reinterpret?
