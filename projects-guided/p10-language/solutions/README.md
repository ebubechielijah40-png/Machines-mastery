# Checkable reasoning after an attempt

1. Tokens are NAME(letx) at0, `=` at4, INTEGER(12) at5, `;` at7, EOF at15
   for the exact text `letx=12; # note` (length15). `#` and following text are a
   comment. As a statement, NAME(letx) parses an expression, then expects `;`
   and sees `=`, so syntax fails. `@;` is a lexical error at0.
2. Abbreviating literal nodes: `(-,(-,7,3),1)` gives3;
   `(/,(/,8,4),2)` gives1; `(-,1,(*,(unary-,2),3))` gives7;
   `(*,(-,1,2),3)` gives-3. The reference's literal format is `('number',n)`.
3. `term` returns the tree for2*3 with `+` unconsumed. Each iteration consumes at
   least one operator and one valid term, so a finite bounded token count decreases.
   An invalid operand raises a defined error; it cannot cause a nonconsuming loop.
4. `1+;` is syntax; `missing;` name resolution; `1/0;` arithmetic; `let let=3;`
   syntax (reserved word where NAME required); `f(2);` syntax (calls unsupported).
   None commits any environment change.
5. Evaluation locally reaches x=3 and y=4, then division fails. Caller stays x=2;
   no y is added and no outputs are returned. Copying one input mapping, evaluating
   all work there, then committing is easier to reason about than an undo log here.
6. A left fold nests its previous AST as a left child every time, even though the
   grammar's additive loop does not recurse. A number with b bits requires storage
   proportional to b and arithmetic work dependent on b. Parse-only timing and
   fixed-size-varying-operand-bit timing answer different questions.
7. One valid design makes power bind more tightly than unary, meaning `-2^2=-4`,
   while exponent operands allow unary so `2^-2=1/4`. Another design is allowed if
   stated and tested. Require an integer exponent and cap its absolute value;
   check rational result limits as well. `2^3^2=512` distinguishes right from left
   association (64). This is an extension specification, not implemented behavior.
8. One valid design: declarations bind only the inner frame, lookup searches out,
   and leaving a block discards its declarations. Starting outer x=2, inner
   `let x=9; x;` produces9 inside but outer x remains2. Assignment to existing
   bindings is a separate feature; the reference has no blocks or assignment.
9. Compare your independently built interpreter on generated bounded expressions
   plus malformed text/rollback limits. Do not treat matching a few examples as
   proof of arbitrary grammar correctness or hosted-code security.
