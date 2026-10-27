# Solution — Two group compatibility

Along a rooted traversal, color encodes path parity. An equal-color edge would close an odd cycle, which cannot alternate two colors all the way around. Conversely, if no conflict occurs every edge satisfies the required relation. Check every component. O(V+E) time/O(V) state. A triangle is a counterexample to assuming every undirected graph is bipartite; an isolated vertex is not a failure.

The complete executable mechanism is [`bipartition`](../../code/graph_algorithms.py). The [lesson](../../LESSON.md) supplies intermediate worked traces; [independent tests](../../code/test_graph_algorithms.py) enumerate routes, cuts, trees or assignments instead of simply copying the implementation recurrence. The tests establish bounded computational behavior, not a deployed network/system guarantee.

**Reconstruction:** close the reference, write the transition from the invariant, derive a different input by hand, and explain one production assumption that can invalidate the graph model.
