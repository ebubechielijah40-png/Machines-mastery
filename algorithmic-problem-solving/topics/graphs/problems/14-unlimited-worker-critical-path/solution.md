# Solution — Unlimited worker critical path

For every dependency u→v update earliest_start[v]=max(earliest_start[v],finish[u]); then finish[v]=start[v]+duration[v]. Induction on topology proves feasibility and optimality under unlimited workers. O(V+E) time/O(V) state. Summing all durations ignores parallelism; taking the shortest predecessor ignores an unmet slow one. Resource-limited scheduling can finish later and is not solved by this function.

The complete executable mechanism is [`critical_path`](../../code/graph_algorithms.py). The [lesson](../../LESSON.md) supplies intermediate worked traces; [independent tests](../../code/test_graph_algorithms.py) enumerate routes, cuts, trees or assignments instead of simply copying the implementation recurrence. The tests establish bounded computational behavior, not a deployed network/system guarantee.

**Reconstruction:** close the reference, write the transition from the invariant, derive a different input by hand, and explain one production assumption that can invalidate the graph model.
