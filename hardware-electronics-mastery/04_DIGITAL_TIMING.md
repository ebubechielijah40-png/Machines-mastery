# Digital timing: values must arrive and remain valid

Study [device behavior](03_SEMICONDUCTORS_TRANSISTORS.md) and
[RC dynamics](02_RC_TRANSIENTS.md) first. A truth table describes values after
settling. It does not say when a receiver can safely use them. The executable
[timing calculator](device-logic/devices.py), [tests](device-logic/test_devices.py)
and [source scopes](device-logic/SOURCES.md) make the following model checkable.
All example timing values are assumed, not manufacturer guarantees.

## Separate a value from a voltage range and a time interval

A digital receiver interprets a specified low input range and high input range.
The interval between those ranges is not a third guaranteed Boolean value.
Output guarantees and input requirements must be compatible: if a driver
promises output low≤VOL and the receiver accepts input low≤VIL, the low noise
margin is VIL-VOL. The high margin is VOH-VIH. Load, supply and temperature
conditions are part of these guarantees. This lesson has not measured them for
a real logic family. A typical curve alone does not establish worst-case margins.

When an input changes, a combinational block can temporarily be invalid or
produce a hazard even if its final truth table is right. Distinguish minimum
contamination delay, the earliest output may stop representing the old input,
from maximum propagation delay, the latest output is guaranteed to settle under
the declared input transition and load conditions. A gate's “delay” cannot serve
both inequalities interchangeably.

A latch follows data while its enable is active, then retains state. An
edge-triggered register samples at a specified edge and exposes a later output.
The clock edge in a functional model is an abstraction of a physical sampling
process. Setup t_s is the required valid interval before capture; hold t_h is the
required interval afterward. Clock-to-Q also has a minimum and maximum. A
simulation that assigns ideal0/1 at an edge does not model the physical aperture.

## Derive setup and hold from event times

Let the launch clock edge be time0. Let the corresponding current capture edge
be s, where s=t_capture-t_launch is **signed skew**. The next capture edge is
T+s for clock period T. Let launch clock-to-Q lie in[q_min,q_max], and
combinational delay lie in[d_min,d_max]. Inputs and clocks otherwise meet the
single-domain assumptions. Let u≥0 bound additional relative edge uncertainty.

The latest new data arrives at q_max+d_max. The earliest relevant next capture
edge is T+s-u, and it needs setup time before it:

\[
 q_{max}+d_{max}+t_s\le T+s-u.
\]

The earliest new data can disturb the old capture value at q_min+d_min. The
latest current capture edge is s+u, and it needs hold time after it:

\[
 q_{min}+d_{min}\ge s+u+t_h.
\]

Consequently setup slack is T+s-u-q_max-d_max-t_s, while hold slack is
q_min+d_min-s-u-t_h. Negative slack violates the declared guarantee. Positive
skew helps this setup constraint but hurts this hold constraint. If the skew
sign is unknown, budget its worst sign separately for each inequality. Multiple
paths require checking every relevant path; the slowest max path and fastest min
path may be different paths.

For T=10 ns,q_min=.2 ns,q_max=1 ns,d_min=.3 ns,d_max=5 ns,t_s=1 ns,t_h=.4 ns,u=0:
setup slack=10-1-5-1=3 ns, hold slack=.2+.3-.4=.1 ns. Now let capture be.2 ns later.
Setup slack becomes3.2 ns, but hold slack becomes-.1 ns. Increasing T to100 ns
makes setup much easier and **does not change the hold failure**. Hold compares
events around the same edge. Repair can require an added minimum path delay,
clock-tree change or a different receiving/launch element. Such a change also
consumes setup budget and must be rechecked.

The calculator reports a setup lower bound on period from this path. It does
not produce a full static-timing analysis, constrain clock phase/membership,
calculate routing, incorporate library corners or certify an achievable clock.
Do not infer real maximum frequency from hypothetical delay inputs.

## Where a delay approximation comes from

A resistor charging a capacitor from0 toward VDD gives
V(t)=VDD(1-e^-t/RC). At half supply, e^-t/RC=1/2, so t_50=RC ln2. This is a
particular RC model and threshold; transistor current varies with voltage.
The [device experiment](device-logic/EXPERIMENTS.md) integrates a resistor-loaded
MOSFET circuit and compares step sizes. Its rising and falling transitions differ
because the current paths differ. Doubling an ideal load capacitance scales the
same autonomous trajectory's time by2; real changes can also alter the driver
and interconnect model.

Synchronous composition hides intermediate hazards only when all sampling
constraints are met. It does not make the hazards cease to exist. An asynchronous
reset, unsynchronized external pin or clock crossing creates additional contracts
that a single-clock Boolean test does not prove.

## Metastability and what a model can establish

If an asynchronous input changes in a sampling aperture, a physical storage node
can take unusually long to settle to a valid state. The failure relevant to the
next receiver is nonresolution by its required time. An abstract X in simulation
is a conservative symbol, not a quantitative analog trajectory or a measured
failure probability. A simulator that never produces X has not ruled out
metastability.

A synchronizer gives a signal time to resolve before downstream use. Device-
specific models often make residual nonresolution fall exponentially with
available resolution time; determining their constants requires relevant device
measurements/specifications. A second stage can reduce failure probability but
does not guarantee zero risk or make independent sampling of a multi-bit bus
coherent. Data buses often require an explicit handshake or a properly designed
crossing protocol. Our new FIFO build is **single-clock**, not an asynchronous
FIFO. The inspected TI report's historical measured parameters are not reused as
modern-device guarantees or as results reproduced here.

## From timing contract to HDL and a machine

The existing [enabled-register build](../hardware-description-languages/systemverilog/units/01-enabled-register/README.md)
checks reset/enable priority, hold and no-edge stability. A new
[single-clock FIFO](../hardware-description-languages/fifo-contract/README.md)
compares VHDL/SystemVerilog state-update semantics against an independent queue.
Both are functional simulations. Neither performs physical setup/hold checking,
FPGA synthesis, timing closure or clock-domain-crossing verification.

In SystemVerilog, separate combinational next-state calculation from clocked
state updates and use nonblocking assignments for the latter. Each right-hand
side is evaluated from the relevant current state; the updates commit later in
the event schedule. Writing a procedural statement earlier does not make one
flip-flop physically update before another at the same ideal edge. VHDL signal
assignment likewise schedules an update; a variable assignment has different
local semantics. Derive the state transition before choosing syntax.

Attempt [the timing/device exercises](device-logic/EXERCISES.md). For an unaided
rebuild, draw launch/current-capture/next-capture event times, rederive both
inequalities including signed skew, then reproduce a hold failure that a slower
clock cannot fix. Explain the boundary between your finite transition checks
and unperformed physical validation.
