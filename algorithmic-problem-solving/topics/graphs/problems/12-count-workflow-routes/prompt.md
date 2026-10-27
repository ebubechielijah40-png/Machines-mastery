# 12. Count workflow routes

Count distinct directed source-to-target paths in a DAG. The source-to-itself empty path counts once. Reject any cycle.

## Contract and examples

The public entry is `dag_path_count`. Vertices use integer IDs0..n−1; duplicate edges are rejected. See the [complete model and worked mechanisms](../../LESSON.md) before choosing a method.

Example input arguments: `[[1,2],[3],[3],[]],0,3`. One expected result: `2`. Outputs whose order is not specified should be checked by their invariant, not a memorized order.

Before implementing, give a direct exhaustive approach for small inputs and state why its cost is worse. Then derive an invariant, prove preservation and termination, state time and storage including representation, and construct an edge case plus a wrong-algorithm counterexample. Retain your attempt before consulting hints.

## Build and transfer

Implement the API in your own file and compare with the shared independent oracle suite on bounded inputs. Explain how changing edge direction/weight semantics changes this objective. Source/model limits are in [SOURCES](../../SOURCES.md). A correct result on the sample alone is insufficient.
