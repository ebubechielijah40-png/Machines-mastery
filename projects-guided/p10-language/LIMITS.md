# Precisely bounded scope

Supported: ASCII identifiers/integer tokens, whitespace/comments, required
semicolons, let rebinding, exact rational +−×÷, unary signs, parentheses, expression
outputs and complete-program commit on success. Python3.10+ standard library;
the retained run used3.12.14.

Constants: source16,384 characters, token count4096 (plus EOF), parser/evaluator
depth64, evaluator steps10,000, rational numerator/denominator4096 bits, decimal
literal length1200. Parser depth is its internal call-depth model, not64 arbitrary
nested parentheses. The regex scanner slices suffixes, so character-copy work
can be quadratic. Arithmetic allocates intermediate host integers before result
size checking; these guards are not a strict memory/time budget.

Absent: functions, loops, closures, blocks, type checker, compiled code, custom
allocator, concurrent/durable state, decimal literals, Unicode names, host objects
and external effects. Errors are exceptions with offsets for lexical/syntax
failures, not a full recoverable diagnostic editor. Tests cover finite selected
cases; broader grammar fuzzing, semantics proofs and resource isolation remain.
