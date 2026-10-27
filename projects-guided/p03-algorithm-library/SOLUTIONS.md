# Reference reasoning and rubric

The [array solutions](../../algorithmic-problem-solving/topics/arrays/README.md)
and [graph solutions](../../algorithmic-problem-solving/topics/graphs/SOLUTIONS.md)
contain mechanism-specific derivations and alternatives. Read them only after
an attempt. The shared module is the implemented reference, not a starter stub.
For the worked BFS, layer0 contains0, layer1 contains1,2 and layer2 contains3.
A shorter path to3 would need a predecessor in an earlier processed layer,
which would already have discovered3. Parent reconstruction supplies a witness.

Rubric: precise contract20%, proof/invariant25%, implementation20%, independent
oracles20%, experiment interpretation10%, unaided transfer5%. A passing result
with the wrong objective, hidden mutation, false expected-time claim or incorrect
negative-cycle scope does not satisfy the contract. Rebuild one operation and
its alternative oracle from memory with changed inputs before declaring your
own learning complete. Repository test execution never establishes learner mastery.
