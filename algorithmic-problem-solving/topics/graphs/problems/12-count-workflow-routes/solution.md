# Solution — Count workflow routes

Partition paths into v by their last edge u→v. These classes are disjoint, so count[v] is the sum of predecessor counts. Initialize one empty prefix at source and process a topological order. O(V+E) arithmetic operations/O(V) state; bit complexity grows with the count. A visited boolean loses multiple prefixes, while a cycle makes unbounded-walk counts a different problem.

The complete executable mechanism is [`dag_path_count`](../../code/graph_algorithms.py). The [lesson](../../LESSON.md) supplies intermediate worked traces; [independent tests](../../code/test_graph_algorithms.py) enumerate routes, cuts, trees or assignments instead of simply copying the implementation recurrence. The tests establish bounded computational behavior, not a deployed network/system guarantee.

**Reconstruction:** close the reference, write the transition from the invariant, derive a different input by hand, and explain one production assumption that can invalidate the graph model.
