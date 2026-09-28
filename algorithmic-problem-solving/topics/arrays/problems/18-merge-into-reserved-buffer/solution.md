# Solution — Merge Into a Reserved Storage Buffer

## 1. Problem model

A storage page contains m sorted live entries followed by reserved empty slots. Another sorted run must be merged without allocating a third page. The algorithmic task is: `a` has length m+n; its first m values are sorted live entries and the remaining n slots are placeholders. `b` contains n sorted values. Merge b into a in place.

## 2. Baseline / brute-force approach

Copy the live prefix and b into a new array, sort/merge, then copy back. O(m+n) extra space.

Why keep the baseline? Because optimization without a correct reference makes it harder to distinguish a faster implementation from a subtly wrong one. For small random inputs, the tests can compare the optimized implementation to a direct oracle.

## 3. Better / target approach

Fill from the end. The largest remaining value belongs at the largest remaining output index, so overwriting cannot destroy an unread value from a's live prefix. O(m+n) time, O(1) auxiliary space.

## 4. Derivation

Start from the output condition and ask what must already be known when each position is finalized. The target method avoids recomputing information that can be maintained incrementally or encoded directly in the array. This reduces repeated work while preserving the exact contract.

## 5. Invariant and correctness

**Invariant:** All positions greater than write are already final and contain the largest consumed elements in sorted order; unread live values remain at indices <= i.

Initialization establishes the invariant before useful work has been finalized. Each loop transition preserves it by changing only the region/state whose contract is known. When the loop terminates, no unknown region remains, so the required postcondition follows. The executable tests include exhaustive or oracle-based checks on bounded small inputs where practical.

## 6. Complexity

Fill from the end. The largest remaining value belongs at the largest remaining output index, so overwriting cannot destroy an unread value from a's live prefix. O(m+n) time, O(1) auxiliary space. Complexity claims refer to the number of abstract operations under a RAM-style cost model; they are not claims about exact wall-clock latency. Language overhead, caches, allocation and input distribution can dominate at small sizes.

## 7. Common wrong approach

Merge forward directly into a. Writing a small b value can overwrite an unread a value before it has been compared.

## 8. Implementation

```python
def merge_into_buffer(a,m,b):
    if m<0 or m+len(b)!=len(a): raise ValueError("invalid lengths")
    i=m-1; j=len(b)-1; w=len(a)-1
    while j>=0:
        if i>=0 and a[i] > b[j]:
            a[w]=a[i]; i-=1
        else:
            a[w]=b[j]; j-=1
        w-=1
    return a
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

Backward merge exploits reserved capacity and is directly related to in-place page maintenance in storage engines and fixed-capacity buffers. A production implementation would still need workload-specific measurement, input validation, memory accounting and failure behavior. This exercise establishes the algorithmic mechanism, not a production service.

## 11. Transfer questions

1. Which part of the invariant would fail if input arrived as an unbounded stream?
2. Can the algorithm be parallelized without changing the result? What state would workers need to exchange?
3. What benchmark would distinguish asymptotic improvement from a constant-factor regression?
4. Which malformed inputs should a production boundary reject rather than silently reinterpret?
