# Solution — Single link failures

low[child] is the earliest ancestor reachable from its subtree through tree descent and one nonparent back edge. An escape above/equal parent means an alternate route; low[child]>discovery[parent] means no escape, hence the tree edge is a bridge. O(V+E) time/O(V) DFS state after validation; this recursive reference caps V at500. Parallel edges need edge IDs and are rejected; skipping all parent edges would be wrong for a multigraph.

The complete executable mechanism is [`bridges`](../../code/graph_algorithms.py). The [lesson](../../LESSON.md) supplies intermediate worked traces; [independent tests](../../code/test_graph_algorithms.py) enumerate routes, cuts, trees or assignments instead of simply copying the implementation recurrence. The tests establish bounded computational behavior, not a deployed network/system guarantee.

**Reconstruction:** close the reference, write the transition from the invariant, derive a different input by hand, and explain one production assumption that can invalidate the graph model.
