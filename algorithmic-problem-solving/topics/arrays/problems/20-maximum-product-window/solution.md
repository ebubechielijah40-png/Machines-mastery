# Solution — Maximum Product Contiguous Window

## 1. Problem model

A synthetic multiplicative score can flip sign when a negative factor arrives. Find the contiguous interval whose factors produce the maximum product. The algorithmic task is: Return the maximum product of any non-empty contiguous subarray.

## 2. Baseline / brute-force approach

Enumerate every interval and multiply incrementally: O(n^2).

Why keep the baseline? Because optimization without a correct reference makes it harder to distinguish a faster implementation from a subtly wrong one. For small random inputs, the tests can compare the optimized implementation to a direct oracle.

## 3. Better / target approach

Track both maximum and minimum product ending at the current position. A negative value swaps their roles because multiplying by a negative reverses order. O(n) time, O(1) space.

## 4. Derivation

Start from the output condition and ask what must already be known when each position is finalized. The target method avoids recomputing information that can be maintained incrementally or encoded directly in the array. This reduces repeated work while preserving the exact contract.

## 5. Invariant and correctness

**Invariant:** After each element, `hi` and `lo` are respectively the maximum and minimum products among all non-empty subarrays ending exactly there. Those two extremes are sufficient for the next transition.

Initialization establishes the invariant before useful work has been finalized. Each loop transition preserves it by changing only the region/state whose contract is known. When the loop terminates, no unknown region remains, so the required postcondition follows. The executable tests include exhaustive or oracle-based checks on bounded small inputs where practical.

## 6. Complexity

Track both maximum and minimum product ending at the current position. A negative value swaps their roles because multiplying by a negative reverses order. O(n) time, O(1) space. Complexity claims refer to the number of abstract operations under a RAM-style cost model; they are not claims about exact wall-clock latency. Language overhead, caches, allocation and input distribution can dominate at small sizes.

## 7. Common wrong approach

Track only the maximum ending product. A very negative minimum can become the next maximum after multiplication by another negative value.

## 8. Implementation

```python
def max_product_subarray(values):
    if not values: raise ValueError("non-empty input required")
    hi=lo=best=values[0]
    for x in values[1:]:
        if x<0: hi,lo=lo,hi
        hi=max(x,hi*x)
        lo=min(x,lo*x)
        best=max(best,hi)
    return best
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

This is dynamic programming over sufficient extremes and illustrates why sign changes can make “bad” intermediate states valuable later. A production implementation would still need workload-specific measurement, input validation, memory accounting and failure behavior. This exercise establishes the algorithmic mechanism, not a production service.

## 11. Transfer questions

1. Which part of the invariant would fail if input arrived as an unbounded stream?
2. Can the algorithm be parallelized without changing the result? What state would workers need to exchange?
3. What benchmark would distinguish asymptotic improvement from a constant-factor regression?
4. Which malformed inputs should a production boundary reject rather than silently reinterpret?
