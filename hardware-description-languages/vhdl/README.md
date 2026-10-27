# VHDL: typed concurrent structures and scheduled state

Start with the original [single-clock FIFO build](../fifo-contract/README.md).
It teaches entity/architecture, generics, unsigned arrays, constrained integer
ranges, concurrent assignments, clocked processes, rising_edge and the crucial
signal <= versus variable := distinction through a real queue state transition.
The VHDL implementation, self-checking bench, independent vectors, negative
controls, exercises and actual GHDL outputs are all included.

This is a developed bounded VHDL unit. Full VHDL semantics, resolution/delta-cycle
edge cases, synthesis, timing closure, physical memory and FPGA integration remain
unfinished. A logical FIFO is not an asynchronous crossing circuit.
