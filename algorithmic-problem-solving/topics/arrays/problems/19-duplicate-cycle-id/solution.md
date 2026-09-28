# Solution — Find a Duplicate Without Modifying the ID Array

## 1. Problem model

A read-only array of n+1 references stores IDs in the range 1..n, guaranteeing at least one duplicate. Find one duplicate using constant extra memory. The algorithmic task is: Return a duplicated value without modifying the input and using O(1) auxiliary space.

## 2. Baseline / brute-force approach

Use a set of seen IDs, O(n) expected time and O(n) space.

Why keep the baseline? Because optimization without a correct reference makes it harder to distinguish a faster implementation from a subtly wrong one. For small random inputs, the tests can compare the optimized implementation to a direct oracle.

## 3. Better / target approach

Interpret each index as a node whose next pointer is `values[index]`. Because n+1 positions map into n possible nonzero indices, a cycle exists; Floyd's tortoise-hare algorithm finds its entrance, which corresponds to a duplicate value. O(n) time, O(1) space.

## 4. Derivation

Start from the output condition and ask what must already be known when each position is finalized. The target method avoids recomputing information that can be maintained incrementally or encoded directly in the array. This reduces repeated work while preserving the exact contract.

## 5. Invariant and correctness

**Invariant:** During phase one, slow and fast follow the same deterministic functional graph at speeds 1 and 2 and must meet inside the reachable cycle. Resetting one pointer to the start makes equal-speed pointers meet at the cycle entrance.

Initialization establishes the invariant before useful work has been finalized. Each loop transition preserves it by changing only the region/state whose contract is known. When the loop terminates, no unknown region remains, so the required postcondition follows. The executable tests include exhaustive or oracle-based checks on bounded small inputs where practical.

## 6. Complexity

Interpret each index as a node whose next pointer is `values[index]`. Because n+1 positions map into n possible nonzero indices, a cycle exists; Floyd's tortoise-hare algorithm finds its entrance, which corresponds to a duplicate value. O(n) time, O(1) space. Complexity claims refer to the number of abstract operations under a RAM-style cost model; they are not claims about exact wall-clock latency. Language overhead, caches, allocation and input distribution can dominate at small sizes.

## 7. Common wrong approach

Use XOR cancellation. With arbitrary duplicate multiplicity and potentially multiple repeated values, XOR does not isolate a valid duplicate in general.

## 8. Implementation

```python
def find_duplicate(values):
    if len(values)<2: raise ValueError("invalid input")
    n=len(values)-1
    if any(not isinstance(v,int) or v<1 or v>n for v in values): raise ValueError("values out of range")
    slow=values[0]; fast=values[values[0]]
    while slow!=fast:
        slow=values[slow]; fast=values[values[fast]]
    slow=0
    while slow!=fast:
        slow=values[slow]; fast=values[fast]
    return slow
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

The deeper lesson is representation: an integer array can encode a directed functional graph. Reinterpreting data structure semantics can unlock algorithms unavailable in the “just an array” view. A production implementation would still need workload-specific measurement, input validation, memory accounting and failure behavior. This exercise establishes the algorithmic mechanism, not a production service.

## 11. Transfer questions

1. Which part of the invariant would fail if input arrived as an unbounded stream?
2. Can the algorithm be parallelized without changing the result? What state would workers need to exchange?
3. What benchmark would distinguish asymptotic improvement from a constant-factor regression?
4. Which malformed inputs should a production boundary reject rather than silently reinterpret?
