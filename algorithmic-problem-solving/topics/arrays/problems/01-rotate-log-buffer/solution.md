# Solution — Rotate a Log Buffer Right

## 1. Problem model

A bounded diagnostic buffer is exported in chronological order, but the hardware DMA cursor means the last k entries physically appear at the front of the next snapshot. Reconstruct the logical order by rotating the array right by k positions. The algorithmic task is: Given a mutable list `values` and integer `k`, rotate the list to the right by `k` positions in place. Empty input must remain empty. Negative `k` is allowed and follows Python modulo semantics.

## 2. Baseline / brute-force approach

Create a second array and copy each element to `(i+k) mod n`. This is O(n) time and O(n) extra space.

Why keep the baseline? Because optimization without a correct reference makes it harder to distinguish a faster implementation from a subtly wrong one. For small random inputs, the tests can compare the optimized implementation to a direct oracle.

## 3. Better / target approach

Normalize k modulo n, reverse the whole array, reverse the first k values, then reverse the remaining suffix. This preserves O(n) time while using O(1) auxiliary space.

## 4. Derivation

Start from the output condition and ask what must already be known when each position is finalized. The target method avoids recomputing information that can be maintained incrementally or encoded directly in the array. This reduces repeated work while preserving the exact contract.

## 5. Invariant and correctness

**Invariant:** After the whole-array reversal, the elements that must become the new prefix are contiguous in reverse order. Reversing the two partitions restores each partition's internal order without changing their membership.

Initialization establishes the invariant before useful work has been finalized. Each loop transition preserves it by changing only the region/state whose contract is known. When the loop terminates, no unknown region remains, so the required postcondition follows. The executable tests include exhaustive or oracle-based checks on bounded small inputs where practical.

## 6. Complexity

Normalize k modulo n, reverse the whole array, reverse the first k values, then reverse the remaining suffix. This preserves O(n) time while using O(1) auxiliary space. Complexity claims refer to the number of abstract operations under a RAM-style cost model; they are not claims about exact wall-clock latency. Language overhead, caches, allocation and input distribution can dominate at small sizes.

## 7. Common wrong approach

Repeatedly pop the last item and insert it at index 0. It is simple but each front insertion shifts O(n) elements, producing O(n*k) behavior.

## 8. Implementation

```python
def rotate_right(values, k):
    n=len(values)
    if n==0:
        return values
    k%=n
    if k==0:
        return values
    def rev(lo,hi):
        while lo<hi:
            values[lo],values[hi]=values[hi],values[lo]
            lo+=1; hi-=1
    rev(0,n-1); rev(0,k-1); rev(k,n-1)
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

Ring buffers, circular queues, storage pages and media buffers all use logical order that differs from physical layout. Rotation is a small model of translating between those views. A production implementation would still need workload-specific measurement, input validation, memory accounting and failure behavior. This exercise establishes the algorithmic mechanism, not a production service.

## 11. Transfer questions

1. Which part of the invariant would fail if input arrived as an unbounded stream?
2. Can the algorithm be parallelized without changing the result? What state would workers need to exchange?
3. What benchmark would distinguish asymptotic improvement from a constant-factor regression?
4. Which malformed inputs should a production boundary reject rather than silently reinterpret?
