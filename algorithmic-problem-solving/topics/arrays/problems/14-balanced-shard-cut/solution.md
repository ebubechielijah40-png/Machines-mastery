# Solution — Find Balanced Shard Cut Points

## 1. Problem model

For a synthetic weighted array, a cut point is “balanced” when total weight strictly left equals total weight strictly right. Find every such candidate. The algorithmic task is: Return all indices i where sum(values[:i]) == sum(values[i+1:]).

## 2. Baseline / brute-force approach

For every i sum both sides from scratch, O(n^2).

Why keep the baseline? Because optimization without a correct reference makes it harder to distinguish a faster implementation from a subtly wrong one. For small random inputs, the tests can compare the optimized implementation to a direct oracle.

## 3. Better / target approach

Compute total once, keep a running left sum, and derive right sum as `total-left-values[i]`. O(n) time, O(1) auxiliary state beyond output.

## 4. Derivation

Start from the output condition and ask what must already be known when each position is finalized. The target method avoids recomputing information that can be maintained incrementally or encoded directly in the array. This reduces repeated work while preserving the exact contract.

## 5. Invariant and correctness

**Invariant:** Before checking i, `left` equals exactly the sum of values before i; `total-left-values[i]` therefore equals exactly the sum after i.

Initialization establishes the invariant before useful work has been finalized. Each loop transition preserves it by changing only the region/state whose contract is known. When the loop terminates, no unknown region remains, so the required postcondition follows. The executable tests include exhaustive or oracle-based checks on bounded small inputs where practical.

## 6. Complexity

Compute total once, keep a running left sum, and derive right sum as `total-left-values[i]`. O(n) time, O(1) auxiliary state beyond output. Complexity claims refer to the number of abstract operations under a RAM-style cost model; they are not claims about exact wall-clock latency. Language overhead, caches, allocation and input distribution can dominate at small sizes.

## 7. Common wrong approach

Use integer average or midpoint index. Balance concerns aggregate weights, not geometric position.

## 8. Implementation

```python
def equilibrium_indices(values):
    total=sum(values); left=0; out=[]
    for i,x in enumerate(values):
        right=total-left-x
        if left==right: out.append(i)
        left+=x
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

The same conservation-style reasoning appears in load partitioning, checksums and streaming aggregates: derive an unseen remainder from a total and a prefix. A production implementation would still need workload-specific measurement, input validation, memory accounting and failure behavior. This exercise establishes the algorithmic mechanism, not a production service.

## 11. Transfer questions

1. Which part of the invariant would fail if input arrived as an unbounded stream?
2. Can the algorithm be parallelized without changing the result? What state would workers need to exchange?
3. What benchmark would distinguish asymptotic improvement from a constant-factor regression?
4. Which malformed inputs should a production boundary reject rather than silently reinterpret?
