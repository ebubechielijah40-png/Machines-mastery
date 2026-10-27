# Compiler/runtime experiments and actual observations

Question: how do emitted code size, executed work, verifier acceptance and
runtime failure differ? Hypotheses: a counted loop keeps its static shape while
executed instructions grow linearly with iterations; malformed stack joins are
rejected; incorrect mathematics and zero division can still pass structure.

Controlled inputs use the exact Flow semantics in README, the same compiler/VM,
fixed loop bodies, signed32 numbers and default fuel unless explicitly changed.
Independent expectations use the closed-form sum and hand-counted instructions.
Instrumentation retains immutable states, disassembly, verifier summaries,
source SHA256 and actual Python/platform/version. No timings are inferred from
instruction counts. The optional host disassembly inspects only the trusted
function defined in experiment.py; Flow never invokes a host source compiler.

From repository root:

```sh
python3 -m unittest discover -s 02-programming/compiler-runtime -v
python3 02-programming/compiler-runtime/experiment.py
python3 02-programming/compiler-runtime/experiment.py --output /tmp/flow-new-run.json
```

The output flag is create-only and refuses an existing path, preserving earlier
evidence. The tracked [raw record](evidence/observed-2026-10-25.json) and
[test log](evidence/tests-2026-10-25.txt) are actual runs, not predicted data.
They record CPython3.12.14 on Linux; the inspected documentation was3.12.15.

| Loop boundn | Observed output | Static instructions | Executed instructions | Maximum stack |
| ---: | ---: | ---: | ---: | ---: |
| 0 | 0 | 20 | 11 | 2 |
| 1 | 0 | 20 | 24 | 2 |
| 2 | 1 | 20 | 37 | 2 |
| 5 | 10 | 20 | 76 | 2 |
| 10 | 45 | 20 | 141 | 2 |
| 30 | 435 | 20 | 401 | 2 |

The counts agree with13n+11 and outputs with n(n-1)/2. The experiment's wrong
increment changes i by2 at n=5, passes the same structural proof, and returns6
instead of10. The deliberately malformed join fails with incompatible stack
depths. The division case verifies, then faults at pc8/source character19 after
eight successful instructions with stack[8,0],locals[8],output[8]. The empty-body
infinite loop runs17 instructions and then faults at its global budget. Its
state is not a normal HALT.

Interpretation: code size, abstract well-formedness, work, intended result and
normal completion are different observables. Changing a loop bound changes
work without changing this template's instruction count. A green verifier is
not an oracle for a learner's mathematical specification. Atomic instruction
publication lets a debugger retain a trustworthy failure boundary for this
machine, while preserving already committed effects.

Alternative explanations/limits: finite tests can miss compiler and verifier
bugs; multiple instructions can share one source position; no path-sensitive
constant proof is performed; host Python object allocation/copying affects real
cost. CPython opcode names observed for the trusted function are neither Flow
instructions nor native CPU opcodes. No sandbox, production runtime, general
language implementation or learner mastery is established.

Follow-up investigations: hold n fixed and increase expression stack depth;
compare snapshot copying with a separately specified mutable execution engine;
add constant propagation and identify new accepted programs; add CALL/RETURN
only after specifying frame/return/fuel invariants. Record new results only
after execution and retain the original semantic contract for comparisons.
