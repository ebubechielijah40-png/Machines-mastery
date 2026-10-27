# Progressive hints

1. Identifier matching consumes letters/digits/underscore as one token before
   checking whether that whole token is the reserved word. Syntax still controls
   what may follow a name.
2. For each AST, first mark parentheses, then unary, then multiplication/division,
   then addition/subtraction. The loops replace the accumulated left subtree.
3. A method owns exactly one grammar level. Consuming `+` inside term would steal
   the expression caller's boundary. Each successful loop consumes an operator
   and a complete operand.
4. Ask first whether every character is a valid token, then whether tokens fit
   the grammar, then whether names/arithmetic have a meaning at runtime.
5. A copied mapping is safe here because values are immutable rationals and the
   language performs no external I/O. A shallow copy would not undo mutation of
   arbitrary shared mutable values.
6. Draw the tree for `1+1+1+1` and distinguish syntax recursion from tree depth.
   Big-integer multiplication depends on operand bits, not only token count.
7. Right association normally requires recursing at the exponent level instead
   of using the same left-fold loop. Decide `-2^2` before choosing method order.
8. Think of a stack of environments. Name lookup searches from inner to outer;
   declaration can affect only the innermost map if that is your specified rule.
9. Use only a grammar and meaning contract during the blank-file attempt. Compare
   traces before reading the reference; a memorized tuple shape is not a proof.
