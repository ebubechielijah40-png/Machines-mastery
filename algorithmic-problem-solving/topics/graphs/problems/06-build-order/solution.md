# Solution — Build order

A zero-indegree choice has no unmet predecessor. Removing it preserves that invariant. If tasks remain without such a choice, repeatedly following a predecessor must eventually repeat a vertex, establishing a cycle. O(V+E) time/O(V) state. Numeric sorting of task IDs is not a valid general solution; IDs need not encode dependencies. Returning only an acyclic prefix must not be mislabeled a complete order.

The complete executable mechanism is [`topological_order`](../../code/graph_algorithms.py). The [lesson](../../LESSON.md) supplies intermediate worked traces; [independent tests](../../code/test_graph_algorithms.py) enumerate routes, cuts, trees or assignments instead of simply copying the implementation recurrence. The tests establish bounded computational behavior, not a deployed network/system guarantee.

**Reconstruction:** close the reference, write the transition from the invariant, derive a different input by hand, and explain one production assumption that can invalidate the graph model.
