# Algorithms: contracts, proofs and independent counterexamples

This developed entry chapter connects original array/graph mechanisms and guided
builds. The full algorithms coursebook remains PARTIAL; hashing, balanced trees,
broad dynamic programming and further analysis still require developed units.
Begin with [Python](../02-programming/python-entry/README.md) and
[proofs/counting](../foundations/mathematics/core/02_PROOFS_DISCRETE.md).

## Derive a contract before naming the algorithm

“Find a route” is incomplete. A fewest-edge route and a minimum-cost route can
select different answers. In graph `0→1` cost10 and `0→2→1` costs1+1, BFS
correctly prefers the one-edge route but fails the minimum-cost objective.
Dijkstra supports nonnegative costs; a negative edge invalidates its finalized-
distance argument. A reachable negative cycle can make some walk costs unbounded
below, which differs from an unreachable vertex. These meanings belong in the
API before code is written.

Read the [graph lesson](../algorithmic-problem-solving/topics/graphs/LESSON.md).
It derives FIFO layers, topological removal, shortest-path relaxation, low links,
cut/cycle arguments, residual flow and augmenting assignment. Each of the
[20 contracts](../algorithmic-problem-solving/topics/graphs/PROBLEMS.md) has a
worked example, proof/complexity discussion, executable reference and separate
practice. The [arrays release](../algorithmic-problem-solving/topics/arrays/README.md)
provides a different representation/ownership starting point.

## Match the proof to an independent check

A BFS path must use existing edges and have the minimum number of edges; merely
returning a list of IDs is insufficient. For a tiny graph, enumerate all simple
paths independently. A topological result must constrain every edge, while a
flow result should match an independently enumerated cut. Reusing the same
recurrence as a test oracle can preserve the same defect twice.

For a loop that marks each vertex once and scans each adjacency entry once,
work is O(V+E) under the declared operation model. A dense graph has E=Θ(V²),
so “linear in input” is not “linear in vertices.” Python slices allocate;
large integers have bit costs; a last-element quickselect pivot has a quadratic
sorted-family counterexample. Expected and worst-case statements need distinct
premises. Read the implementation's recursion and input bounds before scaling.

## Build and assess

Complete [the guided library](../projects-guided/p03-algorithm-library/README.md)
in milestones. Derive one array and two graph mechanisms before consulting
solutions. Run both release runners and retain the graph experiment's V,E,
operation counts and timings separately. Explain why a correct small oracle
and a conditional proof complement each other.

Transfer task: model a build dependency graph, then change it into a road network.
Which operations retain their meaning and which need new direction/weight rules?
Reconstruct one algorithm from blank files and supply a counterexample to an
incorrect alternative. Tests and files measure the prepared implementation;
they do not certify that a learner can perform this reconstruction.
