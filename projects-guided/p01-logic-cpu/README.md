# Build a stored-program computer from a full adder

Build an original eight-bit accumulator machine, then run repeated-addition
multiplication. Success means you can predict the transitions and locate the
first faulty transition, not merely run a supplied program. This project is a
complete abstract software build; a clocked HDL/FPGA implementation remains an
extension requiring separate timing and board validation.

Read [PREREQUISITES.md](PREREQUISITES.md), then implement the milestones in
[CHECKPOINTS.md](CHECKPOINTS.md) in a learner-owned directory. The reference
[lesson](../../01-computation/toy-cpu/README.md) supplies all equations, an ISA
contract and worked hand cases. Try each milestone before opening the matching
part of [cpu.py](../../01-computation/toy-cpu/cpu.py). There are no missing reference
implementation steps or external packages.

The architecture has sixteen shared code/data bytes, an accumulator, four-bit PC,
carry and halt flags. A cycle fetches the current byte, decodes its high nibble,
computes a new state and commits it. ADD uses eight explicitly connected full
adders; instruction operands either contain a four-bit literal or address memory.
Different operand rules make encoding mistakes visible. Decode failure is atomic,
PC wraps modulo16, and program execution has a configurable cycle budget.

Deliver your implementation, a handwritten six-step trace, all test output,
raw branch-fault evidence, multiplication proof and a one-page limitations note.
[TESTS.md](TESTS.md) gives independent acceptance oracles; [EXPERIMENTS.md](EXPERIMENTS.md)
defines the branch experiment. [HINTS.md](HINTS.md) contains progressive help.
The separate [solutions](../../01-computation/toy-cpu/SOLUTIONS.md) are for checking
a written attempt. [LIMITS.md](LIMITS.md) and [PRODUCTION.md](PRODUCTION.md) explain
what the abstract build cannot establish.

Rubric: 25 points for truth-table/modular-addition derivation; 25 for faithful
state transitions and exact hand traces; 20 for independent boundary/failure tests;
15 for predicted and executed experiments; 15 for memory reconstruction and
limitations. A passing total requires a correct arithmetic invariant, a genuine
invalid-decode test and an honest hardware boundary. A run that returns12 but
cannot explain its35 cycles does not pass the mechanism criterion.
