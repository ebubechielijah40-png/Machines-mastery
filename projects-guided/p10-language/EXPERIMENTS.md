# Parsing and failure-atomicity experiments

Question: does changing grouping/association alter syntax-tree structure and
meaning, and can a later runtime error expose earlier state mutations?
Hypotheses: multiplication binds inside addition; division groups left; whole
program failure leaves external state unchanged.

Run `python3 projects-guided/p10-language/code/experiment_language.py` from root.
The script uses six declared synthetic source programs and records actual AST,
exact string outputs, environment before/after and errors in
[evidence/observed.json](evidence/observed.json). Python/platform are recorded.
Inputs and initial x=2 are controlled; independent variables are grouping/operator
placement and failure location; dependent observations are tree, outputs and state.
This experiment measures semantic behavior, not runtime or memory.

In the retained executed run, `2+3*4;` yielded14, `(2+3)*4;`20 and `8/4/2;`1.
`1/3+1/6;` yielded1/2. `let x=x+3; x/2;` committed x=5 and returned5/2.
`let x=9; 1/0;` produced a division-by-zero LanguageError and retained x=2.
The raw record is authoritative for exact trees and diagnostics.

These cases support the chosen precedence/rational/rollback contracts; they do
not verify every source or make a security claim. A different evaluator could
coincidentally agree on these small examples, so the independent arithmetic and
negative tests add coverage. Repeat with generated operator triples and a late
error following many successful declarations. As a follow-up performance study,
time tokenization, parsing and evaluation separately while varying only nesting,
source size or operand bit length. Record real measurements before conclusions.
