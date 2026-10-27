# Solution — Capacity throughput

Augment by the smallest residual capacity on a BFS path. When no path remains, let S be residual-source-reachable vertices. Every S→outside capacity is saturated and conservation makes net crossing flow equal the flow value. Any flow is bounded by that cut, so equality certifies optimality. Dense BFS scans O(V²); an O(V³E) upper bound accounts for this implementation, with O(V²) residual storage. A forward-only residual model can get stuck below optimum.

The complete executable mechanism is [`maximum_flow`](../../code/graph_algorithms.py). The [lesson](../../LESSON.md) supplies intermediate worked traces; [independent tests](../../code/test_graph_algorithms.py) enumerate routes, cuts, trees or assignments instead of simply copying the implementation recurrence. The tests establish bounded computational behavior, not a deployed network/system guarantee.

**Reconstruction:** close the reference, write the transition from the invariant, derive a different input by hand, and explain one production assumption that can invalidate the graph model.
