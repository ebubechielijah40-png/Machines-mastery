# Build milestones, deliverables and rubric

Implement in a new learner file; [reference code](code/minilang.py) is available
for comparison after an attempt. A runnable complete reference is not a substitute
for building and explaining each intermediate mechanism.

| Milestone | Build and learner task | Independently observable gate |
|---|---|---|
| A0: specification | Write the grammar, exact-rational division, required semicolon and error categories. Predict `8/4/2;` and `letx;`. | A partner can determine valid text and expected meaning without the implementation. |
| A1: scanner | Return kind/text/offset records, skip comments, add EOF, reject unknown characters. | ` 12 + x;` starts at1,4,6,7; `@` fails at its offset. `letx` is one name. |
| A2: atoms/unary | Parse integer/name/parentheses/sign into tuple nodes; leave next token unconsumed. | `--2;` and `(2);` parse; unmatched `(` fails. |
| A3: precedence | Compose term and expression methods with left-associated loops. Draw before coding. | `2+3*4;` has a multiply child and yields14; `(2+3)*4;` yields20; `8/4/2;` yields1. |
| A4: exact evaluation | Evaluate trees with Fraction; distinguish unbound name and zero denominator. | `1/3+1/6;` yields1/2; neither `missing;` nor `1/0;` succeeds. |
| A5: program state | Parse all statements; evaluate into a private mapping; commit on complete success. | Starting x=2, `let x=9; 1/0;` leaves external x=2 and emits no partial outputs. |
| A6: bounded failure | Enforce source/token/nesting/tree/number limits and CLI exit2. | Long nesting and a long shallow additive source fail as defined language errors, not raw recursion errors. |
| A7: transfer | Extend one operator or add nested block scopes with written semantics. | New independent tests distinguish precedence/association/scope and preserve old contracts. |

Debugging exercise: change the term loop into a recursive right operand and
explain why division changes. Then remove the private mapping and show the
rollback test catches the new partial-state failure. Perform these mutations
only in your learner copy, retain the failing evidence, then repair them.

Deliver source, hand AST trace, grammar, tests, actual experiment output, one
failure analysis and a reconstruction written from a blank file. Rubric (100):
20 specification/trace,25 parsing correctness,20 evaluation/state correctness,
15 independent/negative tests,10 measurement interpretation,10 limitations and
transfer. Passing reference tests alone earns at most the implementation portions;
it does not establish the learner's explanations or reconstruction.
