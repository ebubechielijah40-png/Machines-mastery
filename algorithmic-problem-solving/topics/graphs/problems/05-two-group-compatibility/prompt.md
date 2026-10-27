# 05. Two group compatibility

Return 0/1 colors that separate every undirected edge, or None if no bipartition exists.

## Contract and examples

The public entry is `bipartition`. Vertices use integer IDs0..n−1; duplicate edges are rejected. See the [complete model and worked mechanisms](../../LESSON.md) before choosing a method.

Example input arguments: `[[1,3],[0,2],[1,3],[0,2]]`. One expected result: `[0,1,0,1]`. Outputs whose order is not specified should be checked by their invariant, not a memorized order.

Before implementing, give a direct exhaustive approach for small inputs and state why its cost is worse. Then derive an invariant, prove preservation and termination, state time and storage including representation, and construct an edge case plus a wrong-algorithm counterexample. Retain your attempt before consulting hints.

## Build and transfer

Implement the API in your own file and compare with the shared independent oracle suite on bounded inputs. Explain how changing edge direction/weight semantics changes this objective. Source/model limits are in [SOURCES](../../SOURCES.md). A correct result on the sample alone is insufficient.
