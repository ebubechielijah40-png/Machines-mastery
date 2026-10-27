# Build an algorithm library with contracts and independent oracles

A useful library supplies more than correct-looking answers: each operation
has a domain, result meaning, mutation policy, correctness argument and cost
model. Build those interfaces incrementally using the implemented
[array release](../../algorithmic-problem-solving/topics/arrays/README.md) and
[graph release](../../algorithmic-problem-solving/topics/graphs/LESSON.md).
The shared [graph module](../../algorithmic-problem-solving/topics/graphs/code/graph_algorithms.py)
is the reference implementation for this project; its location avoids a second
copy drifting away from the teaching. These releases develop substantial
bounded mechanisms; the full algorithms curriculum remains PARTIAL.

Prerequisites: [Python entry](../../02-programming/python-entry/README.md),
[proofs/counting](../../foundations/mathematics/core/02_PROOFS_DISCRETE.md) and
finite sequence/index reasoning. Python3.10+, standard library only:

```bash
python3 algorithmic-problem-solving/topics/arrays/run_all_tests.py
python3 algorithmic-problem-solving/topics/graphs/run_all_tests.py
python3 algorithmic-problem-solving/topics/graphs/code/experiment_graphs.py
```

Before reading references, derive BFS over `0:[1,2],1:[3],2:[3],3:[]`.
The FIFO frontier begins[0], then[1,2], then[2,3]. Mark on insertion so3 is
not enqueued twice. Parent pointers reconstruct0→1→3, while the distance2
states the objective. A stack can find a path without finding the fewest edges.
This difference should appear in the API and a counterexample test.

Architecture: validated immutable input rows → mechanism-specific local state
(frontier, distances, residual capacity or component labels) → new owned result.
Do not collapse unreachable, zero-cost and unbounded-negative results into one
number. The graph unit derives each contract and proof; the project makes the
interfaces and verification reusable.

Follow [milestones](CHECKPOINTS.md), attempt a solution, then use [hints](HINTS.md)
and [reference reasoning](SOLUTIONS.md). [Tests](TESTS.md), [experiments](EXPERIMENTS.md),
[limits](LIMITS.md) and [engineering tradeoffs](PRODUCTION.md) specify deliverables.
Do not call the whole library excellent merely because every problem has a file.

## Additional implemented milestones

Extend the retained arrays/graphs with [explicit map/heap/tree mechanisms](../../algorithmic-problem-solving/mechanisms/ordered-state/README.md) and [the twenty-problem DP release](../../algorithmic-problem-solving/topics/dynamic-programming/README.md). Deliver independent oracles and proofs, then compare collision, skew and wrong-update failures. The shared library locations avoid duplicate implementations.
