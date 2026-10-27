# Machine foundations: quantities, bits, memory and instructions

A machine connects physical change to symbolic rules. A capacitor retains charge;
a register retains a bit pattern; a program counter selects the next rule. These
are related ideas, but a physical component and a mathematical state variable
are different objects. This coursebook teaches a bounded path through their
mechanisms, with complete local derivations and executable builds. The wider
hardware curriculum still needs deeper transistor, timing, cache and peripheral
units; the path below does not claim whole-domain completion.

## 1. Begin with a measured quantity

A voltage is energy transfer per charge, V=J/C; current is charge transfer per
time, A=C/s. Thus vi has units J/s and represents electrical power with a stated
sign convention. An ideal resistor obeys v=Ri. A linear capacitor obeys q=Cv,
so current entering its positive node is i=C dv/dt. A voltage is not a current,
and a stored number3.3 is not meaningful until its unit/reference are stated.

Read the [electrical quantities bridge](../foundations/physics/electrical-quantities/README.md)
before the [complete RC unit](../hardware-electronics-mastery/02_RC_TRANSIENTS.md).
For a source Vs feeding R then C to reference, node-current balance is
C dv/dt=(Vs−v)/R. At equilibrium v=Vs. Subtract it with e=v−Vs; then
de/dt=−e/(RC), giving e=e0 exp(−t/RC). The state remembers initial voltage.
For hypothetical R10kΩ,C10µF, Vs3.3V and v0=0, RC=.1s and v(.1s)≈2.086V.
The exact derivation, worked timing/energy examples and loaded-meter model are
local in the RC lesson; do not replace them by memorizing one charging formula.

An observer changes a physical system if it draws current or adds capacitance.
A finite input resistance can lower the final voltage. A discrete simulation
can also create a false oscillation: forward Euler's deviation multiplier is
1−h/(RC), unstable in magnitude when h>2RC. These are distinct mechanisms.
Before blaming hardware, identify which equations and which numerical method
produced the observation. The RC unit's tests use exact trajectories, energy
accounting and interval invariants rather than one plausible plot.

## 2. Discrete representation is a contract

An eight-bit pattern represents a=Σa_i2^i under the unsigned convention.01111111
is127;10000000 is128 unsigned or−128 under two's complement. The physical wires
do not choose that interpretation. Software and instruction semantics do.

A full adder accepts a,b,c and returns s=a XOR b XOR c, carry=(a AND b) OR
(c AND(a XOR b)). Count the input ones to verify a+b+c=s+2carry. Connect eight
columns and induction gives A+B=result+256carry_out. The low byte is addition
modulo256.255+1 returns0/carry1;127+1 returns128/carry0 even though the latter
exceeds the signed positive range. This is the first connection from representation
to machine-level consequences: one physical operation supports several meanings.

The [full CPU lesson](../01-computation/toy-cpu/README.md) implements each column
and checks all65,536 byte pairs against independent integer arithmetic. Attempt
its bit-arithmetic exercises before running the reference. Exhaustiveness is
feasible here because the domain is tiny; it does not make exhaustive testing of
an entire large computer practical.

## 3. State turns a circuit into a machine

A combinational function's output depends on its current input. Retained state
lets a machine's future depend on history. In the abstract CPU, registers store
an accumulator A, program counter PC, carry and halt flags; memory stores sixteen
bytes. A successful cycle is a function from old state plus fetched instruction
to new state. A real flip-flop/clock/reset circuit must implement retention and
sampling despite finite propagation delays; the Python transition is a model of
that behavior, not evidence that timing constraints have been met.

Instruction bytes have an opcode in the high nibble and an operand in the low.
LDI3 means A←3; ADD14 means A←A+M[14], not A+14. PC chooses which byte to decode,
so ordinary data can become an instruction if control flow reaches it. STORE
can overwrite code because this machine has unified memory and no protection.
A bounded interpreter makes this failure visible without pretending it is safe
firmware or a privileged kernel.

Worked program: LDI3;STA14;LDI4;ADD14;STA15;HLT. The accumulator after each step
is3,3,4,7,7,7; only memory14/15 change; final PC6/cycles6. Explain each intermediate
state before execution. The [guided CPU project](../projects-guided/p01-logic-cpu/README.md)
provides staged construction, exact acceptance tests, debugging exercises, a
branch-fault experiment, hints and separated solutions.

## 4. Algorithms emerge from a small instruction vocabulary

Multiplication need not be a primitive. Initialize p=0,c=b; repeatedly add a to p
and subtract one from c. After k iterations, p≡ka(mod256),c=b−k. For a byte a and
positive byte b, c reaches0 after b steps without wrapping; the invariant proves
p≡ab. A zero entry count needs a separate path and is rejected by this program.
The sixteen-word layout stores code at0–11 and data at12–15. Exact instruction
count8b+3 gives35cycles for3×4. That is an abstract count, not nanoseconds.

A validly encoded wrong branch can terminate incorrectly or loop forever.
Changing JMP2 at address9 to JMP9 gives a stable self-loop under the recorded
100-cycle budget. Changing it to JMP0 restarts product initialization and yields3
rather than12 after41cycles. The difference explains why checking only a halted
flag misses real bugs. Check state transitions, final value, memory effects and
termination budget against independent predictions.

## 5. Connect symbolic commands back to energy

The CPU can compute a desired voltage, but a motor responds through current and
force. Begin the next path with [motion/energy](../foundations/physics/MOTION_ENERGY.md):
net force changes momentum; torque changes angular momentum about a fixed axis;
load inertia matters through squared distance. For a linear constant-field motor,
L di/dt=v−Ri−kω and J dω/dt=ki−bω−τ_load. Multiplying by i andω shows the same
conversion term leaves the electrical store and enters the mechanical one.
Software cannot request more steady speed than supply/current/heat constraints
permit. Follow [Embedded and Robotics](08-embedded-robotics.md) into that complete
bounded control build after the arithmetic/state mechanism is clear.

## 6. Assessment and source boundary

Without notes, derive an adder, trace a branch and distinguish carry from signed
overflow. Reconstruct the CPU from its ISA table. Explain how a nonloading observer
assumption and an atomic-cycle assumption simplify different layers. Give one
counterexample to each simplification. A complete learner submission contains
predictions, original implementation, independent tests, raw experiments and a
limitation statement; reading the reference is preparation rather than proof of
reconstruction skill.

The [RC source map](../hardware-electronics-mastery/rc-transients/SOURCES.md),
[CPU source map](../01-computation/toy-cpu/SOURCES.md) and
[mechanics/control source map](../17-embedded-robotics/control-path/SOURCES.md)
record inspected authoritative material, versions, scope and failed access
attempts. These original examples/code do not redistribute textbook chapters.
Remaining work includes semiconductor device derivations, clocked HDL with
validated timing, buses, interrupts, caches, peripherals and physical experiments.
