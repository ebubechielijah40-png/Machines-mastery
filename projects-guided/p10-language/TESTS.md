# Executed contracts and debugging

From repository root:

```sh
python3 -m unittest discover -s projects-guided/p10-language/code -v
```

The retained [test log](evidence/tests.txt) reports eight passing unittest methods.
One method enumerates operand triples −2..2 and operator pairs, calculates direct
Fraction results independently and skips undefined denominators. Other methods
check precedence AST, rebindings/unary forms, token offsets/comments, malformed and
host-looking syntax, failure atomicity and resource guards. Eight is a test-method
count, not a claim of eight independent full language proofs.

For a failure, first retain source and token offsets. If tokens are wrong, debug
scanner advancement/maximal matching. If an AST is wrong, inspect which parser
method consumed the next operator and whether a loop folded left. If meaning is
wrong with a correct AST, trace one node and environment lookup at a time. If
rollback fails, inspect the single commit point rather than swallowing the error.
A raw RecursionError, partial output or changed external mapping after an expected
LanguageError violates this bounded contract.

The CLI accepts stdin and prints one exact rational per expression on success;
errors use stderr and exit2. Unit tests do not establish process isolation or
concurrent calls sharing a mapping. Caller dictionary values/keys are trusted
ordinary objects of the documented types.
