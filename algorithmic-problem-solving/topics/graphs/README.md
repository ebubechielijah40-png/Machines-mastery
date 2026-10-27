# Graphs: a developed twenty-contract release

A graph separates a system's entities from the relationships that constrain
movement, dependencies, capacity or connectivity. Choosing the meaning of an
edge comes before choosing a search algorithm.

Start with [proofs, counting and complexity](../../../foundations/mathematics/core/02_PROOFS_DISCRETE.md),
then read [LESSON](LESSON.md). Attempt [the twenty problems](PROBLEMS.md) in order.
Each problem separates its prompt, progressive hints and solution. The reference
library is runnable standard-library Python; it is not pseudocode or twenty
copies of one traversal.

| Stage | Question | Problems |
|---|---|---|
| Frontier state | What is reachable, and in how many hops? | 1–3 |
| Structure | Can the graph be partitioned, ordered or collapsed? | 4–8 |
| Costs | Which route objective and edge assumptions apply? | 9–11 |
| Acyclic recurrence | How do route counts and job times accumulate? | 12–14 |
| Failure and optimization | What disconnects, costs least or carries most? | 15–19 |
| Transfer | How can all-pairs reachability reuse intermediate vertices? | 20 |

From repository root:

```sh
python3 algorithmic-problem-solving/topics/graphs/run_all_tests.py
python3 algorithmic-problem-solving/topics/graphs/code/experiment_graphs.py
```

[Validation evidence](evidence/release-tests.txt) contains one ten-test shared
oracle suite plus twenty one-test worked contracts: 21 passing groups. Exhaustive
oracles enumerate routes, permutations, colorings, partitions, spanning subsets,
cuts or assignments on small graphs. They validate the optimized algorithms by
independent definitions rather than invoking the same implementation twice.
[EXPERIMENT](EXPERIMENT.md) interprets actual synthetic observations and their
limits. [SOURCES](SOURCES.md) records inspected resources and original derivations.

Scope: **STRONG bounded graph unit**. This release does not complete every
algorithms topic, prove correctness for all programs or reproduce graph research.
Low-link and matching references have an explicit 500-vertex recursion cap;
maximum flow uses a small dense matrix. Multigraphs, changing graphs, distributed
routing, advanced flow and large-scale graph storage remain outside this unit.
A mastery pass requires a proof, a new counterexample and reconstruction from a
blank file, not only green tests.
