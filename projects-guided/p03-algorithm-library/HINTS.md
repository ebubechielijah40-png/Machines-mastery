# Hints after the initial attempt

Mark a BFS neighbor when enqueuing, not after later removal. For a shortest-route
proof use the first allegedly incorrect distance and its predecessor. For a
cut-based oracle enumerate vertex subsets containing the source but excluding
the sink; do not reuse residual search. An unreachable node and a reachable
zero-cost node need different results. A topological order constrains every
edge; checking only that all vertex IDs appear once is insufficient. Before
optimizing a recursive implementation, preserve a correctness oracle and its
input assumptions.
