# Solution — Single node failures

For nonroot u, a child v with low[v]>=discovery[u] cannot escape without u, so removing u separates that subtree. A root has no ancestor side and is a cut vertex only with at least two DFS children. O(V+E) time/O(V) state, V≤500 for this recursive reference. Applying the nonroot test blindly wrongly marks a root with one child; an isolated vertex is not an articulation point.

The complete executable mechanism is [`articulation_points`](../../code/graph_algorithms.py). The [lesson](../../LESSON.md) supplies intermediate worked traces; [independent tests](../../code/test_graph_algorithms.py) enumerate routes, cuts, trees or assignments instead of simply copying the implementation recurrence. The tests establish bounded computational behavior, not a deployed network/system guarantee.

**Reconstruction:** close the reference, write the transition from the invariant, derive a different input by hand, and explain one production assumption that can invalidate the graph model.
