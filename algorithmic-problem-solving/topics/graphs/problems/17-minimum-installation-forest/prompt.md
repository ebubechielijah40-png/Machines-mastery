# 17. Minimum installation forest

Return total cost and a minimum spanning forest for a simple undirected integer-weight graph. Disconnection is allowed.

## Contract and examples

The public entry is `minimum_spanning_forest`. Vertices use integer IDs0..n−1; duplicate edges are rejected. See the [complete model and worked mechanisms](../../LESSON.md) before choosing a method.

Example input arguments: `3,[(0,1,4),(1,2,1),(0,2,2)]`. One expected result: `(3,[(1,2,1),(0,2,2)])`. Outputs whose order is not specified should be checked by their invariant, not a memorized order.

Before implementing, give a direct exhaustive approach for small inputs and state why its cost is worse. Then derive an invariant, prove preservation and termination, state time and storage including representation, and construct an edge case plus a wrong-algorithm counterexample. Retain your attempt before consulting hints.

## Build and transfer

Implement the API in your own file and compare with the shared independent oracle suite on bounded inputs. Explain how changing edge direction/weight semantics changes this objective. Source/model limits are in [SOURCES](../../SOURCES.md). A correct result on the sample alone is insufficient.
