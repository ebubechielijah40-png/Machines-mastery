# Engineering consequences of a small CPU

Keep architecture tests separate from host-interpreter concerns. The eight-bit
model intentionally permits self-modification, so an execution host must bound
cycles and validate memory before each step. A bytecode interpreter embedded in
a service would also need isolation, host resource limits and a defined policy
for traces that contain user data. This local teaching script exposes no server.

For an HDL extension, implement a synchronous reset state, derive the longest
combinational path, state memory read/write timing and test read-during-write
behavior. A design that passes instruction tests can still fail at the requested
clock frequency. Keep a software golden model for differential instruction traces,
but also verify gate-level timing independently: models can share the same mistake.

Measure hardware cost only after synthesis for a named tool/device/version.
The35 abstract cycles for3×4 do not imply35nanoseconds, a fixed instruction rate
or a power budget. Preserve raw reports rather than translating operation counts
into invented physical performance. Reconstruction challenge: explain how a
register's retained value differs from the combinational adder's current output.
