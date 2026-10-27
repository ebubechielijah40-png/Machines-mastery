# Derive the library in increments

1. Specify an array operation's valid sizes, returned value and mutation policy.
   Derive its invariant and check empty/singleton/boundary inputs independently.
2. Freeze a graph representation: integer IDs, direction, duplicate/loop policy,
   integer weights and ownership. Validate malformed IDs before searching.
3. Derive reachability and BFS distance/parent state. Prove first-discovery
   optimality from the FIFO layer invariant, then test against enumerated paths.
4. Add topological ordering and a cycle witness. A nonempty DAG has an indegree-zero
   vertex; empty graphs have an empty order. Test cyclic graphs explicitly.
5. Separate nonnegative Dijkstra, zero/one deque search, DAG negative-edge search
   and Bellman–Ford with reachable negative-cycle influence. Supply a counterexample
   showing why their assumptions are not interchangeable.
6. Add connectivity obstructions, spanning forests, residual flow and matching.
   Use edge/vertex removal, tree subsets, cut enumeration and assignment enumeration
   as oracles, rather than comparing each algorithm with a renamed copy.
7. Package documented operations with isolated tests. Run all20 graph problem
   contracts and the shared exhaustive suite; preserve expected and actual traces.
8. Instrument graph size, edge density, operation counts and wall time separately.
   Reconstruct one graph and one array mechanism from blank files, then change
   the representation or update pattern and explain the new cost model.
