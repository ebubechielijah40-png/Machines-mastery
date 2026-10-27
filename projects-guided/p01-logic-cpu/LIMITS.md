# What this build establishes

The reference is a complete executable model of the stated tiny ISA. A cycle is
an atomic Python state transition; it has no clock period, propagation delay,
metastability, transistor model, bus contention or reset distribution. A software
carry chain explains arithmetic but does not measure gate speed or power.

Sixteen unified bytes make code/data aliasing observable. There is no MMU,
privilege, executable-memory protection, interrupt, device I/O, stack or ABI.
A bounded execution timeout does not solve arbitrary program termination. An
unsigned modulo result is not automatically a signed arithmetic interpretation.
The ISA and layout are original and incompatible with Hack, ARM and RISC-V.

A next physical milestone would implement the combinational adder in HDL with
an exhaustive testbench, then a clocked register/control path, explicit reset and
memory timing. Board-specific synthesis/timing reports, power measurements and
reset tests are still required. None were performed for this abstract unit.
