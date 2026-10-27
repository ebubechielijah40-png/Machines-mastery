# Hold semantics constant while changing execution mode

Question: do object/resource/concurrency contracts in this finite build survive
ordinary versus interpreter-only execution? Prediction: ownership copies, reverse
cleanup with suppressed failures, and the controlled split-update counterexample
are semantic outcomes, not consequences of one JIT strategy.

Controls: identical Java source compiled for release17, fixed arrays, two workers,
a barrier forcing both volatile reads before writes, and an explicit join. Run
run.py to retain compiler/runtime/javap commands. Actual OpenJDK17.0.20 runs in
both modes passed15 checks, retained close:B before close:A, preserved two
suppressed exceptions, and printed split:1,atomic:2,monitor:2. Bytecode contains
arraylength and clone instructions/calls as recorded. These are finite tests,
not performance measurements or a proof for every memory-model schedule.
Follow-up: add an initializer failure, an accessor leak and a lock covering only
the write, keeping each intended failure separate from compiler errors.
