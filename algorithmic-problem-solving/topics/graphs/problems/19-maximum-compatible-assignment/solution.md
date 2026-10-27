# Solution — Maximum compatible assignment

A successful augmenting path adds one assignment while preserving uniqueness. If a larger matching existed, its symmetric difference with the current one would contain an augmenting alternating path. Searching every new left vertex therefore reaches maximum cardinality. O(L*E) reference time, O(L+R) search/owner state; L≤500 because recursion is bounded. Greedily assigning0→0 without allowing reassignment strands left1 despite a size-two solution.

The complete executable mechanism is [`bipartite_matching`](../../code/graph_algorithms.py). The [lesson](../../LESSON.md) supplies intermediate worked traces; [independent tests](../../code/test_graph_algorithms.py) enumerate routes, cuts, trees or assignments instead of simply copying the implementation recurrence. The tests establish bounded computational behavior, not a deployed network/system guarantee.

**Reconstruction:** close the reference, write the transition from the invariant, derive a different input by hand, and explain one production assumption that can invalidate the graph model.
