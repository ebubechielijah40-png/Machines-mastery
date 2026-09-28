# Solution — Run-Length Encode Repeated Events

## 1. Problem model

A telemetry stream often contains long runs of the same categorical state. Compress consecutive repeats without changing sequence semantics. The algorithmic task is: Return a list of `(value,count)` pairs describing maximal consecutive runs.

## 2. Baseline / brute-force approach

For every position, scan forward to recount its run, then skip it. Careless implementations may repeatedly inspect the same elements and approach O(n^2).

Why keep the baseline? Because optimization without a correct reference makes it harder to distinguish a faster implementation from a subtly wrong one. For small random inputs, the tests can compare the optimized implementation to a direct oracle.

## 3. Better / target approach

Maintain the current run value and count; emit when the value changes. Every item is consumed once: O(n) time and O(r) output space for r runs.

## 4. Derivation

Start from the output condition and ask what must already be known when each position is finalized. The target method avoids recomputing information that can be maintained incrementally or encoded directly in the array. This reduces repeated work while preserving the exact contract.

## 5. Invariant and correctness

**Invariant:** Before consuming the next item, all completed runs are final and the pending `(current,count)` exactly represents the maximal suffix of processed input containing `current`.

Initialization establishes the invariant before useful work has been finalized. Each loop transition preserves it by changing only the region/state whose contract is known. When the loop terminates, no unknown region remains, so the required postcondition follows. The executable tests include exhaustive or oracle-based checks on bounded small inputs where practical.

## 6. Complexity

Maintain the current run value and count; emit when the value changes. Every item is consumed once: O(n) time and O(r) output space for r runs. Complexity claims refer to the number of abstract operations under a RAM-style cost model; they are not claims about exact wall-clock latency. Language overhead, caches, allocation and input distribution can dominate at small sizes.

## 7. Common wrong approach

Count global frequencies with a dictionary. That destroys ordering and merges separated runs, changing the meaning of the stream.

## 8. Implementation

```python
def run_length_encode(values):
    if not values:
        return []
    out=[]; cur=values[0]; count=1
    for x in values[1:]:
        if x==cur:
            count+=1
        else:
            out.append((cur,count)); cur=x; count=1
    out.append((cur,count))
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

RLE is used in bitmap formats, column encodings, state traces and sparse event timelines. The key distinction is local repetition versus global frequency. A production implementation would still need workload-specific measurement, input validation, memory accounting and failure behavior. This exercise establishes the algorithmic mechanism, not a production service.

## 11. Transfer questions

1. Which part of the invariant would fail if input arrived as an unbounded stream?
2. Can the algorithm be parallelized without changing the result? What state would workers need to exchange?
3. What benchmark would distinguish asymptotic improvement from a constant-factor regression?
4. Which malformed inputs should a production boundary reject rather than silently reinterpret?
