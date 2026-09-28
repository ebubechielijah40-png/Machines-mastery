# Solution — First Missing Positive Identifier

## 1. Problem model

A compact synthetic allocator stores positive slot IDs in an unsorted array. Find the smallest positive ID absent from the set without allocating another O(n) set. The algorithmic task is: Return the smallest missing positive integer using O(n) time and O(1) auxiliary space; mutating the input is allowed.

## 2. Baseline / brute-force approach

Insert positive values into a hash set and scan 1,2,... until missing. O(n) expected time but O(n) extra space.

Why keep the baseline? Because optimization without a correct reference makes it harder to distinguish a faster implementation from a subtly wrong one. For small random inputs, the tests can compare the optimized implementation to a direct oracle.

## 3. Better / target approach

Only values 1..n can affect an answer <= n. Repeatedly place value v at index v-1 when possible. Then the first index i not holding i+1 reveals the answer; otherwise n+1.

## 4. Derivation

Start from the output condition and ask what must already be known when each position is finalized. The target method avoids recomputing information that can be maintained incrementally or encoded directly in the array. This reduces repeated work while preserving the exact contract.

## 5. Invariant and correctness

**Invariant:** After each successful swap, at least one in-range value is placed in its unique canonical slot. Duplicate values cannot cause infinite swapping because an equal target stops movement.

Initialization establishes the invariant before useful work has been finalized. Each loop transition preserves it by changing only the region/state whose contract is known. When the loop terminates, no unknown region remains, so the required postcondition follows. The executable tests include exhaustive or oracle-based checks on bounded small inputs where practical.

## 6. Complexity

Only values 1..n can affect an answer <= n. Repeatedly place value v at index v-1 when possible. Then the first index i not holding i+1 reveals the answer; otherwise n+1. Complexity claims refer to the number of abstract operations under a RAM-style cost model; they are not claims about exact wall-clock latency. Language overhead, caches, allocation and input distribution can dominate at small sizes.

## 7. Common wrong approach

Sort and scan. It works but costs O(n log n), missing the linear-time in-place structure supplied by the constrained value range.

## 8. Implementation

```python
def first_missing_positive(values):
    n=len(values); i=0
    while i<n:
        v=values[i]
        if 1<=v<=n and values[v-1] != v:
            values[i],values[v-1]=values[v-1],values[i]
        else:
            i+=1
    for i,v in enumerate(values):
        if v != i+1:
            return i+1
    return n+1
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

This is an example of using the input array itself as an implicit hash table when keys map bijectively to a bounded index range. A production implementation would still need workload-specific measurement, input validation, memory accounting and failure behavior. This exercise establishes the algorithmic mechanism, not a production service.

## 11. Transfer questions

1. Which part of the invariant would fail if input arrived as an unbounded stream?
2. Can the algorithm be parallelized without changing the result? What state would workers need to exchange?
3. What benchmark would distinguish asymptotic improvement from a constant-factor regression?
4. Which malformed inputs should a production boundary reject rather than silently reinterpret?
