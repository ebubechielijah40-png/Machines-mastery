# From source text to a verified, debuggable runtime

A loop is compact text describing repeated state changes. A processor does not
read that sentence and infer its intent. Some mechanism must recognize its
structure, select operations and control where execution goes next. This unit
builds that bridge: source characters → tokens → a structured parser → explicit
instructions → a control-flow check → an executing state machine. It connects
the earlier expression interpreter with later native compilation and debugging.

Start with [Python values, loops, functions and errors](../python-entry/README.md),
then [aliases and object identity](../../programming-languages-mastery/08-python/units/objects-and-aliases/README.md),
then [scanner/parser/evaluator composition](../../projects-guided/p10-language/README.md).
The [proof and discrete-mathematics bridge](../../foundations/mathematics/core/02_PROOFS_DISCRETE.md)
introduces invariants and sets. Entry task: trace a counted loop, explain why a
new tuple preserves an old snapshot, and distinguish source syntax errors from
errors reached during execution. Use the linked instruction before attempting
those tasks if the vocabulary is unfamiliar.

## Choose a language contract before implementing its parser

Our original language, Flow, operates on signed32 integers. Its statements are:

```text
let name = expression;
name = expression;
print expression;
if (expression) { statements } else { statements }
while (expression) { statements }
```

`else` is optional. Declarations are top-level, appear before use and cannot
repeat a name. Names have ASCII letters/digits/underscore and cannot start with
a digit or equal a keyword. A declaration's initializer cannot read its own new
name. This small language has one flat frame of slots; it does not pretend to
provide lexical block variables, functions, closures or dynamically typed values.
Study [lexical binding](../../books/crafting-interpreters/generated/chapters/11/README.md)
after this unit for environments and captured state. The distinct mechanisms
are connected, not silently treated as one language.

Nonnegative decimal literals range0…2147483647. Unary minus, `* / + - < ==`, and
parentheses form expressions. Unary minus binds most tightly, followed by `* /`,
then `+ -`, then `< ==`. Every binary operator is left-associative. Therefore
`20-6-3` means `(20-6)-3=11`; `3<2<1` means `(3<2)<1=1`, **not** Python's chained
comparison. Comparisons produce0 or1. A condition treats zero as false and any
other integer, including a negative one, as true. `#` comments run to newline.
Whitespace separates tokens but does not define blocks; braces do.

All computed values must remain in[-2147483648,2147483647]. Overflow is a runtime
fault, not wrapping arithmetic. To construct the minimum value in source, use
`-2147483647-1`: the magnitude in `-2147483648` exceeds our deliberately restricted
literal grammar before unary negation executes. This choice is explicit, not a
universal rule about programming languages.

Division truncates toward zero. Let a=-7 and b=3. Divide magnitudes:7//3=2;
restore the negative sign to obtain-2. Computing Python's floor operation
directly yields-3, so copying the host operator would implement the wrong
language. The implementation never converts a quotient to float. Zero divisors
fault. MIN_INT/-1 gives2147483648 and therefore faults; NEG(MIN_INT) faults too.
See [SOURCES](SOURCES.md) for the selected primary comparisons, not an attribution
of this original language's choices to Python or Java.

## Compile expressions by preserving evaluation order

The scanner consumes the input left to right and records each token's starting
**character** offset. It recognizes `==` before individual operators; an unknown
character is an error rather than a skipped byte. The source is a Python string,
so an offset is not a UTF-8 byte offset. Comments can contain Unicode even though
identifiers are ASCII. Source maps must name their coordinate system.

The expression parser reads an operand, then binary operators whose precedence
meets a minimum. It parses the right operand with minimum `precedence+1`. This
prevents an equal-precedence operator from being consumed into the right side,
making the enclosing loop combine operators left-associatively. Parentheses
start a fresh expression; unary minus parses at a higher minimum. This parser
emits code directly; the earlier language project instead makes tree structure
explicit. Neither design is the definition of compilation.

For `let x=2+3*4;`, emit postorder evaluation:

| Instruction | Stack after success | Reason |
| --- | --- | --- |
| CONST2 | [2] | preserve left operand of addition |
| CONST3 | [2,3] | multiplication's left operand |
| CONST4 | [2,3,4] | multiplication's right operand |
| MUL | [2,12] | consume3 and4, push their product |
| ADD | [14] | consume2 and12 |
| STORE0 | [] | put14 into the declared slotx |

The stack is a sequence whose rightmost element is the top. A binary instruction
must read `(left,right)` in that order; SUB cannot reverse them without changing
the program. STORE consumes an operand; LOAD copies a frame value onto the stack.
PRINT appends one value to a bounded output tuple. It does not call a host file,
network, shell or arbitrary function.

## Translate decisions into explicit instruction addresses

The program counter pc is an index in an immutable instruction tuple. Normal
instructions advance to pc+1. `JUMP target` selects an absolute instruction index.
`JZ target` pops a condition and branches if it is zero; otherwise it falls
through. Targets are instruction indices, not source characters or byte addresses.

Compile the condition first. Emit JZ with a temporary target because the end of
the then-block is not yet known. For an else-block, emit a JUMP after the then
code so successful then execution skips the alternative. Patch JZ to the else
start and JUMP to the common continuation once those positions exist.

For `let x=2+3*4;if(x<15){print x;}else{print 0;}` the preceding six instructions
are followed by:

| pc | Instruction | Incoming stack height |
| ---: | --- | ---: |
| 6 | LOAD0 | 0 |
| 7 | CONST15 | 1 |
| 8 | LT | 2 |
| 9 | JZ13 | 1 |
| 10 | LOAD0 | 0 |
| 11 | PRINT | 1 |
| 12 | JUMP15 | 0 |
| 13 | CONST0 | 0 |
| 14 | PRINT | 1 |
| 15 | HALT | 0 |

Both paths reach15 with empty stacks. Actual execution chooses the then path,
produces14 and successfully executes14 instructions, including HALT. The trace
and character offsets are retained in [actual observations](evidence/observed-2026-10-25.json).

A while-loop places its condition at a remembered start, emits JZ to the future
exit, compiles the body, then emits JUMP back to the condition. The condition is
recomputed on every iteration. Jumping back only to the body would keep an old
condition and could run forever. A body need not run at all; reasoning about
initialization must account for that path.

## Derive the structural proof that execution needs

A raw instruction tuple can be malformed even if our source compiler normally
emits good code. Check its shape first: permitted operations, correct operands,
valid slot/branch indices, bounded source-map positions, immutable containers
and an ending HALT. Python's Boolean is not accepted as an integer operand in
this contract. Shape checks also cover unreachable instructions.

Then reason about reachable instructions using abstract state `(h,I)`: h is
incoming stack height and I is the set of definitely initialized slots. The
entry state is `(0,empty)`. CONST/LOAD add one stack item; STORE/PRINT/JZ consume
one; binary operations consume two and produce one. NEG needs one and preserves
height. LOAD slotj requires `j in I`; STOREj addsj toI. HALT requires h=0.

Every successor receives the resulting abstract state. First visits record it.
At a join, incoming heights must agree; otherwise a subsequent pop has no one
consistent structural interpretation. Definitely initialized sets merge by
**intersection**, since a variable is definitely initialized only if every
incoming path initialized it. Union would confuse "some path did" with "all
paths did." Revisit a successor when its initialized set becomes smaller.

Example raw instructions have a condition, then STORE0 on one path, and LOAD0
after the merge. The path that bypasses STORE0 must make LOAD0 invalid. Even
`CONST1; JZ...` propagates both successors: this proof tracks shapes and
initialization, not actual integer constants. It intentionally trades precision
for a transparent conservative analysis. The source language's declaration rule
helps avoid these cases, while raw bytecode tests probe the verifier directly.

Why does this analysis stop even when a program loops? Code positions and local
slots are finite. First discovery adds a position once; a later change can only
remove members of its initialized set. A finite set cannot shrink indefinitely.
Reaching a mismatched stack height fails immediately. The worklist computes an
abstract fixed point; it does not execute every loop iteration.

The resulting invariant is: along modeled reachable edges, instructions have
enough stack operands, stack height stays within64, initialized-slot reads are
permitted, branches remain in the tuple, and reached HALTs have empty stacks.
This is a derivation of the intended property plus finite tests, not a machine-
checked proof of our Python implementation or source/bytecode equivalence.
The selected JVM structural/dataflow ideas are mapped in SOURCES; Flow has only
one value type and no Java object initialization, exception handlers or class
format. It is not a JVM verifier implementation.

## What the verifier cannot promise

`JUMP0; HALT` is structurally valid even though HALT is unreachable. The VM's fuel
bound stops it. `print 1/0;` is structurally valid and fails dynamically. A loop
that incrementsi by2 instead of1 is structurally valid and computes the wrong
sum. This separates well-formed execution structure, runtime value checks and
algorithm-specific correctness. Test each with an appropriate oracle rather
than turning one green verifier result into a general correctness claim.

The finite arithmetic suite independently uses Fraction for exact quotients;
the counted-loop suite uses the closed form n(n-1)/2. Negative controls alter
control structure and intended behavior. They are evidence for chosen cases,
not coverage of every possible source program or a proof of termination.

## Commit one instruction, then preserve its evidence

The concrete runtime state is `(pc,stack,locals,output,steps,halted)`. Before a
step, copy its immutable tuples into working lists. Check fuel and operands,
calculate the candidate transition, then publish one new Snapshot only after
the instruction succeeds. A division/overflow/output/fuel fault retains the
incoming snapshot. The exception records that snapshot and the instruction's
source character offset.

For `let x=8;print x;x=x/(x-8);`, evaluating the failed assignment reaches DIV
with stack[8,0]. The prior x=8 and output[8] remain committed. DIV changes
nothing, and STORE has not run. Retrying that instruction without changing the
program/state repeats the fault. This is instruction-level atomicity; it is
not a transaction rolling back the entire source statement or whole program.

`until(breakpoints=(pc,),steps=k)` advances at mostk instructions and pauses
**before** a selected pc. Calling it again at the same breakpoint makes no
progress; explicitly step once to cross it. Snapshots retained by a caller do
not mutate when the machine advances. Fuel is global to the machine and is
never replenished by debugger calls. HALT itself consumes one instruction:
`print 1;` with budget2 commits its output then faults before HALT. "Output was
produced" and "program halted normally" are distinct observations.

The source/API bounds are8192 characters,2048 tokens,4096 instructions,64 local
slots,64 operand entries,32 nesting depth,100,000 maximum fuel and1000 maximum
output values. These bound teaching workloads. Snapshot tuple copying adds work
proportional to retained frame/stack/output sizes on each step; a VM instruction
is not necessarily constant host time. Fuel does not impose a hard wall-clock
deadline on Python or an OS call. Host Python can mutate Machine attributes or
replace code; this implementation is not an isolation boundary for hostile code.

## Connect this runtime to real language implementations

The experiment disassembles one trusted host Python function with `dis` and
records actual opcode names/runtime. Those are CPython implementation details,
not stable source-language semantics, native CPU instructions or Flow's ISA.
Our explicit stack model makes that distinction visible without reproducing
CPython's parser, optimizer, object model, garbage collector or adaptive runtime.

Continue with [real C compilation, linking and relocation](../../04-computer-systems/compile-link/README.md),
[the C byte parser](../../programming-languages-mastery/01-c/units/01-byte-parser/README.md),
[memory allocation](../../projects-guided/p04-memory-allocator/README.md) and
[the shell's process boundary](../../projects-guided/p02-shell/README.md).
The native compiler emits machine code and the linker resolves symbols; the
current VM instead interprets its own instructions inside Python. Memory layout,
ownership, ABI, OS descriptors and concurrency require those separate mechanisms.

## Build it before reading the reference

1. Specify valid/invalid sources and exact integer results. Implement a scanner
   retaining character offsets. Reject rather than skip unknown syntax.
2. Build arithmetic emission and hand-check2+3*4 and20-6-3. Test operand order,
   zero division, minimum/maximum values and overflow before adding control flow.
3. Map names to slots. Add declarations, assignment, output and immutable state.
   Explain the difference between a copied binding and a preserved snapshot.
4. Add patched if/else and while targets. Trace both branches, zero iterations,
   nested control and a loop with no progress.
5. Implement abstract stack/init propagation, joins and a worklist. Deliberately
   corrupt one target, one stack depth and one initialized-slot path.
6. Add atomic faults, fuel, breakpoints, source maps and disassembly. Run actual
   experiments and explain which wrong algorithms the verifier must still accept.

Deliver grammar/contracts, a worked trace, implementation, independent tests,
raw observations, one diagnosed fault and one transfer extension. Rubric:25
points semantic/translation reasoning,20 verifier derivation,20 independent
tests/negative controls,15 debugger/failure evidence,10 prerequisite/native
connections,10 reproducibility/limits. A high total cannot compensate for a
wrong division contract, silently corrupted join or invented execution evidence.

Attempt [EXERCISES](EXERCISES.md), use [HINTS](HINTS.md) only after recording an
attempt, then compare [SOLUTIONS](SOLUTIONS.md). Reconstruction: from a blank
file, rebuild arithmetic, slots, one branch, loop, verifier and step debugger
without copying the reference. Transfer: design CALL/RETURN frames and explain
which current proof states must expand before adding recursion.

```sh
python3 -m unittest discover -s 02-programming/compiler-runtime -v
python3 02-programming/compiler-runtime/experiment.py
```

Python3.10+ standard library is sufficient. [EXPERIMENTS](EXPERIMENTS.md) records
the executed environment, observations and limitations. Author evidence does not
establish learner mastery. Broader language/runtime/compiler, advanced debugging,
native optimization and the full original programming mandate remain unfinished.
