# Acceptance tests and independent oracles

From the repository root:

```sh
python3 -m unittest discover -s 01-computation/toy-cpu -p 'test_*.py' -v
python3 01-computation/toy-cpu/experiment.py
```

The executed [test transcript](../../01-computation/toy-cpu/evidence/tests.txt)
contains eight passing tests. They exhaust eight full-adder triples and65,536
byte additions; trace a six-instruction program; check225 small multiplications
plus modular overflow; check carry/zero branching, invalid decode atomicity,
PC wrap, self-modification, cycle exhaustion and invalid boundaries.

These are not just comparisons to a second copy of the implementation. Integer
addition modulo256 is an independently expressed oracle; the program trace and
multiplication invariant are hand-checkable. Copy the tests to your learner build
and change the import to your module. Before doing so, write at least one new
hand program and one malformed state test yourself.

A failed final result should be reduced to the first incorrect transition.
Check input-list copying separately from output accuracy: a correct result may
still accidentally mutate the caller's program. A timeout must retain state for
inspection. An unsupported opcode must leave registers, memory and cycle count
unchanged. Passing these checks establishes this finite ISA contract, not HDL
correctness, timing closure or absence of all software defects.
