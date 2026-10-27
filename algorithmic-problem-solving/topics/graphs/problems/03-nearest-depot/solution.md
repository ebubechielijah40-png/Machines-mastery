# Solution — Nearest depot

A conceptual zero-cost super-source would connect every depot. Initializing the actual queue with all depots establishes the same distance-zero frontier without adding a vertex. The BFS layer proof then applies. O(V+E+S) time including source enumeration, O(V) auxiliary state. Running one source after another while keeping old nonzero labels can preserve the wrong distances. An empty source set yields all None, not a fabricated origin.

The complete executable mechanism is [`multi_source_distances`](../../code/graph_algorithms.py). The [lesson](../../LESSON.md) supplies intermediate worked traces; [independent tests](../../code/test_graph_algorithms.py) enumerate routes, cuts, trees or assignments instead of simply copying the implementation recurrence. The tests establish bounded computational behavior, not a deployed network/system guarantee.

**Reconstruction:** close the reference, write the transition from the invariant, derive a different input by hand, and explain one production assumption that can invalidate the graph model.
