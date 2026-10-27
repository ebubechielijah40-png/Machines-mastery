# Selected concept dependency map

[Companion lesson](README.md) teaches lexical scope after names, environments,
functions, calls and closures. Its executable AST is deliberately supplied so
parsing does not hide the binding problem. Follow declaration order → static
resolution → environment-depth access → shared mutable cells → closure capture →
shadowing and rejected declarations. Predict the binding bug before executing it.

The author source scopes actually inspected are chapter11 §§11.1–11.5 and
chapter10 §10.6. This original companion does not reproduce every book chapter,
its source code or complete Lox semantics. [EXERCISES](EXERCISES.md),
[HINTS](HINTS.md), [SOLUTIONS](SOLUTIONS.md) and [EXPERIMENTS](EXPERIMENTS.md)
provide a bounded build and independently checkable traces.
