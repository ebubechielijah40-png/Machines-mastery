# Attempts before hints or solutions

1. **Token boundaries.** List kind/text/offset for `letx=12; # note` and explain
   why this is not a valid declaration. Construct a one-character lexical error.
2. **Tree reconstruction.** Draw full tuple ASTs for `7-3-1;`, `8/4/2;`,
   `1--2*3;`, `(1-2)*3;`. State one intermediate result per internal node.
3. **Parser invariant.** What token must remain after parsing the first term in
   `2*3+4;`? Prove the additive loop terminates on a valid bounded token stream.
4. **Errors by stage.** Classify `1+;`, `missing;`, `1/0;`, `let let=3;`, `f(2);`.
   Predict whether any environment mutation is visible to the caller.
5. **Atomicity.** Start with x=2; predict environment and outputs after
   `let x=x+1; x; let y=4; y/0;`. Build a failing nontransactional variant, then
   repair it without trying to undo mutations one by one.
6. **Cost.** Why can a shallow additive source build a deep tree? Why does a
   character-count bound not give a constant-time arithmetic guarantee? Propose
   an experiment separating scan, parse and evaluation time.
7. **New semantics.** Add exponentiation with right association: `2^3^2` should
   mean `2^(3^2)`. Specify its precedence relative to unary minus and reject
   exponents outside a declared bound. Design tests before implementation.
8. **Scope transfer.** Design `{ let x=...; }` with lexical block scope. State
   whether updating an outer x is allowed. Give a lookup example that distinguishes
   your design from a single dictionary; do not silently copy Python's semantics.
9. **Reconstruction.** Close the implementation, rebuild scanner/parser/evaluator
   on a blank page, explain why it never invokes host parsing, and pass the
   existing contract tests. Use an independent arithmetic oracle for your extension.

[Progressive hints](HINTS.md) and [checkable solutions](solutions/README.md) are
separate so your first reasoning attempt remains meaningful.
