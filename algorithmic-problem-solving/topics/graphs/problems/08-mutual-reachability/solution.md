# Solution — Mutual reachability

Collapse each true strong component; the collapsed graph has no cycle, since a component cycle would imply mutual reachability. DFS finish order places a source component ahead of successors. Reverse-edge searches in that order isolate one component at a time. O(V+E) time/storage. A one-direction edge does not merge its endpoints. Compare returned partitions as sets of sets, not an arbitrary traversal order.

The complete executable mechanism is [`strongly_connected`](../../code/graph_algorithms.py). The [lesson](../../LESSON.md) supplies intermediate worked traces; [independent tests](../../code/test_graph_algorithms.py) enumerate routes, cuts, trees or assignments instead of simply copying the implementation recurrence. The tests establish bounded computational behavior, not a deployed network/system guarantee.

**Reconstruction:** close the reference, write the transition from the invariant, derive a different input by hand, and explain one production assumption that can invalidate the graph model.
