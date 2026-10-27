# Solution — All pairs reachability

A route using only intermediate vertices through k either avoids k or splits into an i→k route and k→j route using earlier intermediates. This derives the boolean recurrence by induction. O(V³) time/O(V²) storage. Omitting the initial identity incorrectly loses empty paths. Repeated BFS is an alternative O(V(V+E)) approach and can be preferable on sparse adjacency lists.

The complete executable mechanism is [`transitive_closure`](../../code/graph_algorithms.py). The [lesson](../../LESSON.md) supplies intermediate worked traces; [independent tests](../../code/test_graph_algorithms.py) enumerate routes, cuts, trees or assignments instead of simply copying the implementation recurrence. The tests establish bounded computational behavior, not a deployed network/system guarantee.

**Reconstruction:** close the reference, write the transition from the invariant, derive a different input by hand, and explain one production assumption that can invalidate the graph model.
