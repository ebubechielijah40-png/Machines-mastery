# Build a bounded expression language

**Developed bounded interpreter; whole compiler/language field remains PARTIAL.**
This project converts text into tokens, a syntax tree, exact arithmetic and a
transactionally committed environment. It does not call Python `eval`, `exec`,
`ast.parse` or a third-party parser. [The complete lesson](LESSON.md) explains
how to derive it; [EXERCISES](EXERCISES.md), [HINTS](HINTS.md) and
[solutions](solutions/README.md) keep attempts separate from reference code.

Prerequisites: functions, loops, lists, dictionaries, integer/fraction arithmetic,
induction and simple tree traversal. Use [the proof/discrete bridge](../../foundations/mathematics/core/02_PROOFS_DISCRETE.md)
and [Python aliasing/lifetime](../../programming-languages-mastery/08-python/units/objects-and-aliases/README.md).
No physical-science prerequisite is needed because this language manipulates
abstract rational numbers with no physical units. Math and programming readiness
must be checked by an actual learner attempt, not inferred from directory presence.

Python3.10+ standard library. From repository root:

```sh
python3 -m unittest discover -s projects-guided/p10-language/code -v
python3 projects-guided/p10-language/code/experiment_language.py
printf 'let x=2; (x+3)*4;\n' | python3 projects-guided/p10-language/code/minilang.py
```

The last command prints20. A malformed program exits2 with a language-error
message. [Actual traces](evidence/observed.json) and [test output](evidence/tests.txt)
are retained; expected examples are not relabeled as measurements.

Architecture: source→bounded token stream with offsets→recursive-descent parser
→tuple AST→tree evaluator with a private environment→commit on success. Exact
rationals make arithmetic semantics checkable without rounding ambiguity.
Lexing, syntax, name binding, evaluation errors and state commit are distinct
interfaces. A valid token stream can still be syntactically invalid, and a valid
AST can still divide by zero.

Build milestones, debugging, experiments, rubric and production limits are in
[CHECKPOINTS](CHECKPOINTS.md), [EXPERIMENTS](EXPERIMENTS.md), [TESTS](TESTS.md),
[PRODUCTION](PRODUCTION.md) and [LIMITS](LIMITS.md). The source map records original
language design separately from inspected host-language/library facts.

A reconstruction pass requires rebuilding parser precedence and atomic state
behavior from a blank file, adding a new operator with a stated associativity,
and demonstrating that hostile-looking host syntax remains ordinary rejected
text. This interpreter is a local teaching mechanism, not a secure hosted-code
sandbox or production compiler.
