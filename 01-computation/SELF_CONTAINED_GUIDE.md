# Computation: from representation to stored-program execution

Start with the [coursebook](../coursebooks/01-machine-foundations.md), then work
through the [toy CPU lesson](toy-cpu/README.md). This phase now has a substantive
bounded path, rather than asking the learner to invent missing mechanisms.
The wider architecture domain remains PARTIAL.

## Representation and combinational arithmetic

Represent a byte by Σb_i2^i. A full adder's sum and carry satisfy a+b+c=s+2d;
connecting eight columns gives A+B=result+256carry. Thus unsigned addition wraps
modulo256. Signed interpretation changes meaning, not wire arithmetic:255+1 gives
0/carry1 while127+1 gives128/carry0 and signed overflow. The local lesson derives
the truth table and ripple invariant, implements the columns, and exhaustively
checks all65,536 byte pairs against independent integer arithmetic.

## Sequential state and control

A retains a value across cycles; a combinational adder does not. The abstract
CPU stores A, PC, flags and sixteen bytes. Fetch/decode/compute/commit is an exact
state-transition contract; it omits real clock/reset/delay behavior. High nibble
selects the operation and low nibble is an immediate or memory address according
to that opcode. LDI3;STA14;LDI4;ADD14;STA15;HLT produces A3,3,4,7,7,7 in six cycles.
The complete instruction table, validation rules and hand trace are local.

## An algorithm and its failure cases

Repeated addition stores p≡ka(mod256) after k loop iterations and decrements a
positive counter. The loop's proof and8b+3 cycle count are independently checkable.
The real JSON trace records3×4=12 in35cycles. Changing JMP2 to JMP9 at address9
produces a100-cycle timeout with retained PC9; changing the target to0 instead
terminates with3 after41cycles. Valid instruction encoding is not semantic
correctness. Unified memory also permits STORE to overwrite a future instruction.

## Build and assessment

Use the [guided project](../projects-guided/p01-logic-cpu/README.md) for milestones,
acceptance tests, fault injection, performance interpretation and protection limits.
Attempt [exercises](toy-cpu/EXERCISES.md) before [hints](toy-cpu/HINTS.md) and
[solutions](toy-cpu/SOLUTIONS.md). Reconstruct the machine from the encoding table
without the reference; passing reference tests alone is preparation evidence.

```sh
python3 -m unittest discover -s 01-computation/toy-cpu -p 'test_*.py' -v
python3 01-computation/toy-cpu/experiment.py
```

[Source verification](toy-cpu/SOURCES.md) records the inspected author project
pages and original local ISA. No HDL, board timing, cache, memory bus, interrupt,
peripheral, ABI or physical CPU validation is claimed. These are remaining
architecture topics; the abstract cycle count is not a physical benchmark.
