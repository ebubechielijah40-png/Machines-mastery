# Validation evidence

Run both release runners from [README](README.md). The graph runner executes
the shared independent-oracle suite plus20 distinct problem suites in separate
processes. Oracles enumerate simple paths, topological permutations, component
partitions after removal, spanning-tree subsets, cuts and compatible assignments.
The arrays runner preserves its20 existing mechanisms and adversarial tests.
These were actually executed during repository integration.

Test invalid representations and mutation behavior as well as ordinary answers.
For negative cycles, test which targets are influenced rather than labeling every
reachable vertex negative infinity. For flow, verify the returned cut's capacity
as well as the scalar optimum. For quickselect, include the documented last-pivot
quadratic counterexample instead of assuming random expected behavior.

Exhaustion over tiny graphs is finite evidence. The proofs justify the algorithmic
mechanisms under stated assumptions; neither implies arbitrary resource bounds
or production suitability. Python big integers and recursive call depth need
separate analysis.
