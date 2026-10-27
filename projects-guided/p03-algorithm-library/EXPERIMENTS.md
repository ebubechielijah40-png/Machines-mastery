# Representation and density experiment

Question: how does edge density change work as vertex count grows? Predict
adjacency storage/work in V+E before timing. Keep algorithm, interpreter and
input-generation rule fixed; vary vertex count and sparse-chain versus dense
edge pattern. Instrument V,E, operation counts and elapsed time separately.
Run the graph [experiment](../../algorithmic-problem-solving/topics/graphs/code/experiment_graphs.py)
and inspect its retained [evidence directory](../../algorithmic-problem-solving/topics/graphs/evidence).
No hypothetical timing is supplied as an observation here.

Use exact independently solved tiny cases to protect correctness while measuring.
A dense graph can make an O(V+E) pass quadratic in V without contradicting its
linear-input bound. Allocation, validation, queue implementation and interpreter
noise can explain timing departures; counting only main-loop operations excludes
some of those costs. Follow up with another representation, changed edge order
or a deep chain near the declared recursion boundary. Preserve failed predictions.
