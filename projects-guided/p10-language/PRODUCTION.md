# Engineering boundary

Run this locally as a teaching CLI. There is no network listener, credential
access, package installation or deployment step. Do not expose this Python process
as an execution service merely because host eval is absent.

A hosted design would need independent process/resource isolation, request-size
and work quotas before allocation, timeouts/cancellation, per-request environments,
input/schema validation, failure logging without confidential source, versioned
language semantics and fuzzing of parser/resource guards. A copied dictionary
provides no thread isolation or durable recovery. Adding external I/O would require
an explicit effects/commit design; dictionary rollback alone cannot undo it.

For performance, profile scanning/parsing/evaluation separately. Replace suffix
slicing only after preserving positions/error behavior. A bytecode backend or
iterative evaluator can avoid deep-tree recursion but requires a new equivalence
argument and tests. The current implementation is deliberately bounded and does
not claim a production compiler's optimizer, type system, ABI or debugger.
