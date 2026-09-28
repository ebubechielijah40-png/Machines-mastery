# C — deep self-contained guide

## Why this language/tool exists

C is studied here for **native compiled systems programming**. Learn it as a model of execution, memory/state, interfaces, errors, and tooling—not as syntax trivia.

## Core mechanisms

Study **manual object lifetimes, pointers, arrays, structs, ABI, undefined behavior**. For each feature, answer: what representation exists at runtime/hardware level, what guarantees are enforced by compiler/runtime, what remains the programmer's responsibility, and what failure modes exist?

## Execution trace

For every nontrivial example, trace:

```text
source/input
→ parse/compile/runtime representation
→ state/memory changes
→ OS/hardware interaction
→ output/error
```

For HDL, replace sequential software execution with elaboration/synthesis and clocked/combinational hardware semantics.

## Example ladder

1. smallest valid program and toolchain invocation;
2. values/types and representation;
3. control flow with explicit state trace;
4. data structures and memory/lifetime;
5. I/O and OS/runtime interaction;
6. failure/error handling;
7. concurrency where applicable;
8. performance measurement;
9. security boundary;
10. binary/bytecode/RTL inspection.

## Assignments

For every major language topic do 5 small exercises, 3 medium exercises, 1 difficult exercise, 1 debugging task, 1 performance experiment, and 1 reconstruction-from-memory task. Write tests before inspecting the reference implementation.

## Project ladder

memory viewer → allocator → shell → HTTP server. Each project must have correctness tests, edge/failure tests, a design note, a benchmark where meaningful, and an explanation of what production concerns the toy project omits.

## What not to overlearn

Do not memorize the entire standard library. Learn the execution model and mechanisms deeply; keep API surface as searchable reference.
