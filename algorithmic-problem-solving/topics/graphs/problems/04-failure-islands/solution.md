# Solution — Failure islands

Mutual reachability is an equivalence relation in an undirected graph. The traversal from a new root finds precisely its equivalence class; no edge connects two returned classes. O(V+E) total scan, because assigned vertices are never searched as new roots. O(V) visited/output beyond input. Directed reachability does not have the symmetry needed for this proof; asymmetric adjacency is rejected rather than silently reinterpreted.

The complete executable mechanism is [`components`](../../code/graph_algorithms.py). The [lesson](../../LESSON.md) supplies intermediate worked traces; [independent tests](../../code/test_graph_algorithms.py) enumerate routes, cuts, trees or assignments instead of simply copying the implementation recurrence. The tests establish bounded computational behavior, not a deployed network/system guarantee.

**Reconstruction:** close the reference, write the transition from the invariant, derive a different input by hand, and explain one production assumption that can invalidate the graph model.
