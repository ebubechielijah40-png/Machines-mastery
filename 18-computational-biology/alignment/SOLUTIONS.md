# Alignment solutions — compare after recording an attempt

1. Columns score 2,-2,2, total 2; removing gaps gives `AG` and `ACG`.

2. Rows for empty and A, columns empty/A/C: `(0,-2,-4)` and `(-2,2,0)`. A zero first row permits free leading symbols in B; it changes the objective and can produce a different alignment.

3. The final column consumes both symbols, only A's symbol, or only B's symbol. These exhaust the admissible progress steps. A gap/gap column consumes nothing; allowing it with zero or positive rewards creates ambiguity or unbounded behavior in an unrestricted-length model.

4. `AA`/`-A` and `AA`/`A-` both score 0. Diagonal-first traceback selects the final A, returning `AA`/`-A`. It does not establish which correspondence is real.

5. Global empty versus `AC` is `--`/`AC`, score -2 with default scores. Local returns empty/empty, score 0. Local `AA`/`CC` with unfavorable mismatches has no positive correspondence and also returns empty/empty at spans (0,0). When zero-valued nonempty alignments exist, choosing empty is a deterministic policy rather than uniqueness.

6. Matrix rows: `(0,-2,-4,-6)`, `(-2,2,0,-2)`, `(-4,0,1,2)`. Backtrack diagonal from (2,3), left from (1,2), diagonal from (1,1); reverse columns to get `A-G`/`ACG`, score 2.

7. `ACGT`/`ACGT`, score 8; both spans (2,6). `a[2:6]` and `b[2:6]` recover the consumed intervals. The optimum excludes dissimilar flanks; it does not explain why they differ.

8. Mismatch scores -5; two gaps score -2. The permitted model correctly prefers the latter. If opposing gaps are scientifically inappropriate, change the admissible transitions or scoring model and prove/test the new optimizer. Hiding this case by changing a test expectation is incorrect.

9. Possibilities include forgetting to reverse traceback columns, decrementing the wrong input index, and emitting the wrong side's gap for up/left. Test the `AG`/`ACG` worked matrix; then remove gaps and compare with spans; then independently rescore each emitted column. Reversal alone preserves the score in this additive model, so reconstruction order checks are needed even if rescoring passes.

10. Suppose two prefix paths score 5: one ends in a gap in B and one in a match. Appending a second gap costs only extension for the first but opening for the second. A scalar score discards this distinction. Track match-ending, gap-in-A, and gap-in-B states, including their transition constraints. This is an outline for a future affine-gap unit, not a verified implementation of it.

11. Original score-only implementation below. It uses O(len(b)) stored cells; swap inputs first to achieve O(min(n,m)) space under this symmetric substitution model. It does not reconstruct an alignment.

```python
def score_only(a, b, match=1, mismatch=-1, gap=-1):
    previous = [j * gap for j in range(len(b) + 1)]
    for i, x in enumerate(a, 1):
        current = [i * gap]
        for j, y in enumerate(b, 1):
            current.append(max(previous[j - 1] + (match if x == y else mismatch),
                               previous[j] + gap, current[j - 1] + gap))
        previous = current
    return previous[-1]
```

This function is illustrative solution code: unlike the checked public API it omits type, gap, and resource validation. Test it on empty, singleton, repeated-symbol, mismatch-heavy, and exhaustive short inputs before using it. The committed execution record includes those oracle comparisons.

12. See [executed observations](EXPERIMENTS.md); the score objective changes with gap cost, while the input strings stay fixed. The toy null enumerates distinct composition-preserving permutations, equally weighted. A model retaining dinucleotide counts would answer a different conditional question and can give different tail behavior. Neither null establishes ancestry, function, or causation. Parameter selection and repeated searches need separate statistical treatment.

13. One defensible text-diff design consumes all lines globally, rewards exact equal lines, penalizes added/deleted lines, and defines whether a modified line is a substitution or two gaps. Record newline normalization and encoding; bound byte size and table size before allocation. Alternative weights change what "minimal change" means. Require tests that preserve line order and reconstruct both inputs. A successful unaided reconstruction must derive boundaries, transitions, tie policy, and complexity rather than reproduce a memorized table.
