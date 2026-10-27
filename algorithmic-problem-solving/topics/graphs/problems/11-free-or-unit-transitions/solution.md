# Solution — Free or unit transitions

The deque preserves distance priority: a zero edge stays at the current distance and a unit edge advances one layer. Stale labels are skipped, so a poor first discovery can improve. O(V+E) graph work in the standard deque argument and O(V+E) normalized input/queued labels. Ordinary BFS would prefer fewer edges and return cost1 to vertex1 in the worked graph, missing the free two-edge route.

The complete executable mechanism is [`zero_one_distances`](../../code/graph_algorithms.py). The [lesson](../../LESSON.md) supplies intermediate worked traces; [independent tests](../../code/test_graph_algorithms.py) enumerate routes, cuts, trees or assignments instead of simply copying the implementation recurrence. The tests establish bounded computational behavior, not a deployed network/system guarantee.

**Reconstruction:** close the reference, write the transition from the invariant, derive a different input by hand, and explain one production assumption that can invalidate the graph model.
