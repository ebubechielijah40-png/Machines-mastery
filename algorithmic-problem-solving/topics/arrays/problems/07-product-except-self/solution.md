# Solution — Per-Sensor Product Without Self

## 1. Problem model

A calibration stage needs, for each sensor, the product of all other gain factors. Division is forbidden because zeros are valid gains in the synthetic model. The algorithmic task is: Return an array where output[i] equals the product of all input values except values[i], without division.

## 2. Baseline / brute-force approach

For each i multiply every j != i. O(n^2) time.

Why keep the baseline? Because optimization without a correct reference makes it harder to distinguish a faster implementation from a subtly wrong one. For small random inputs, the tests can compare the optimized implementation to a direct oracle.

## 3. Better / target approach

Store prefix products in output, then walk from right with a running suffix product. O(n) time and O(1) extra space beyond output.

## 4. Derivation

Start from the output condition and ask what must already be known when each position is finalized. The target method avoids recomputing information that can be maintained incrementally or encoded directly in the array. This reduces repeated work while preserving the exact contract.

## 5. Invariant and correctness

**Invariant:** Before the reverse pass handles i, `out[i]` is the product strictly left of i and `suffix` is the product strictly right of i.

Initialization establishes the invariant before useful work has been finalized. Each loop transition preserves it by changing only the region/state whose contract is known. When the loop terminates, no unknown region remains, so the required postcondition follows. The executable tests include exhaustive or oracle-based checks on bounded small inputs where practical.

## 6. Complexity

Store prefix products in output, then walk from right with a running suffix product. O(n) time and O(1) extra space beyond output. Complexity claims refer to the number of abstract operations under a RAM-style cost model; they are not claims about exact wall-clock latency. Language overhead, caches, allocation and input distribution can dominate at small sizes.

## 7. Common wrong approach

Multiply all values once and divide by each value. Besides violating the constraint, zeros make division invalid and overflow behavior can differ in fixed-width languages.

## 8. Implementation

```python
def product_except_self(values):
    n=len(values); out=[1]*n
    p=1
    for i,x in enumerate(values):
        out[i]=p; p*=x
    s=1
    for i in range(n-1,-1,-1):
        out[i]*=s; s*=values[i]
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

Prefix/suffix decomposition is a general technique for removing one contribution from an aggregate without recomputing the entire aggregate. A production implementation would still need workload-specific measurement, input validation, memory accounting and failure behavior. This exercise establishes the algorithmic mechanism, not a production service.

## 11. Transfer questions

1. Which part of the invariant would fail if input arrived as an unbounded stream?
2. Can the algorithm be parallelized without changing the result? What state would workers need to exchange?
3. What benchmark would distinguish asymptotic improvement from a constant-factor regression?
4. Which malformed inputs should a production boundary reject rather than silently reinterpret?
