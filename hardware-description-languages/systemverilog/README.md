# SystemVerilog / Verilog

[Prepared register unit](units/01-enabled-register/README.md). Learner NOT STARTED.

The roadmap covers syntax; signals/wires and state; combinational/sequential modeling; modules/entities and hierarchy; testbenches; simulation time; clock/reset; FSM; parameterization/generics; verification; synthesis; RTL; simulation versus synthesis; inferred hardware; common bugs and races; toolchain; projects.

Teach an observable contract first, then a timing diagram, next-state rule, implementation and independent testbench. Include broken cases that produce a different observable behavior. For Verilog, distinguish the selected language revision and idioms from SystemVerilog's intent-specific processes. For VHDL, signals/variables and delta-cycle behavior need inspected language evidence before drawing equivalences.

Projects: gates → adder → ALU → register → counter → FSM → memory interface → processor component → CPU. Each step requires an internal prerequisite bridge and separate problems/hints/solutions/tests. Do not assign physical voltages or clock limits without a target datasheet. Planned validation: exhaustive small-domain behavior, reset/initialization, width boundaries, mutant detection, synthesis inspection and eventually physical measurement as distinct gates.

Language scope: [all core languages](../../programming-languages-mastery/README.md). Foundations: [electronics/digital logic](../../hardware-electronics-mastery/README.md).
