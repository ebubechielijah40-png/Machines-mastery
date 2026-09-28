# Solution — Compute Trapped Capacity Between Barriers

## 1. Problem model

A simplified cross-section of a containment tray gives barrier heights at unit-spaced positions. Compute how many unit volumes of liquid can remain after filling and settling. The algorithmic task is: Given nonnegative integer heights, return total trapped water.

## 2. Baseline / brute-force approach

For each index independently find the maximum height to its left and right, O(n^2).

Why keep the baseline? Because optimization without a correct reference makes it harder to distinguish a faster implementation from a subtly wrong one. For small random inputs, the tests can compare the optimized implementation to a direct oracle.

## 3. Better / target approach

Use two pointers. The smaller boundary is the limiting side; advance it while tracking left/right maxima. Each index is finalized once, O(n) time and O(1) space.

## 4. Derivation

Start from the output condition and ask what must already be known when each position is finalized. The target method avoids recomputing information that can be maintained incrementally or encoded directly in the array. This reduces repeated work while preserving the exact contract.

## 5. Invariant and correctness

**Invariant:** When left_max <= right_max, water at left is determined solely by left_max because some right barrier at least that high is known to exist; symmetric for the right side.

Initialization establishes the invariant before useful work has been finalized. Each loop transition preserves it by changing only the region/state whose contract is known. When the loop terminates, no unknown region remains, so the required postcondition follows. The executable tests include exhaustive or oracle-based checks on bounded small inputs where practical.

## 6. Complexity

Use two pointers. The smaller boundary is the limiting side; advance it while tracking left/right maxima. Each index is finalized once, O(n) time and O(1) space. Complexity claims refer to the number of abstract operations under a RAM-style cost model; they are not claims about exact wall-clock latency. Language overhead, caches, allocation and input distribution can dominate at small sizes.

## 7. Common wrong approach

Use only the global maximum and distance from it. Local valleys may be bounded by lower barriers and cannot all fill to the global maximum.

## 8. Implementation

```python
def trapped_water(heights):
    l=0; r=len(heights)-1; lm=rm=0; total=0
    while l<=r:
        if lm <= rm:
            lm=max(lm,heights[l]); total+=lm-heights[l]; l+=1
        else:
            rm=max(rm,heights[r]); total+=rm-heights[r]; r-=1
    return total
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

This problem trains reasoning about local capacity under two-sided constraints and the proof pattern behind two-pointer elimination. A production implementation would still need workload-specific measurement, input validation, memory accounting and failure behavior. This exercise establishes the algorithmic mechanism, not a production service.

## 11. Transfer questions

1. Which part of the invariant would fail if input arrived as an unbounded stream?
2. Can the algorithm be parallelized without changing the result? What state would workers need to exchange?
3. What benchmark would distinguish asymptotic improvement from a constant-factor regression?
4. Which malformed inputs should a production boundary reject rather than silently reinterpret?
