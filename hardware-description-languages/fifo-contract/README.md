# One queue contract, two hardware description languages

Build a single-clock finite queue before treating memory as an unlimited array.
A producer can offer a word while a consumer takes one, including at the full or
empty boundary. The design must decide which operations happen, preserve order,
and update occupancy once per edge. This unit derives that contract and compares
independent Python queue observations with actual SystemVerilog and VHDL runs.
It does not implement an asynchronous FIFO or claim synthesized hardware timing.

Prerequisites: [finite words/state](../../foundations/mathematics/state-and-logic/README.md),
[Boolean construction](../../hardware-electronics-mastery/03_SEMICONDUCTORS_TRANSISTORS.md),
[register timing](../../hardware-electronics-mastery/04_DIGITAL_TIMING.md) and the
[enabled-register lesson](../systemverilog/units/01-enabled-register/LESSON.md).
Work the state table before opening the source. Syntax is introduced below;
[primary inspection/tool scope](SOURCES.md) and [actual observations](evidence/observed.json)
are separate from assumptions.

## State and a precise transfer rule

Memory stores DEPTH words of WIDTH bits. State is a read pointer rd, a write
pointer wr and occupancy n, with0≤n≤DEPTH. The abstract queue contains exactly n
words in logical arrival order; physical cells outside that active sequence are
irrelevant. Reset synchronously discards all queued words, sets both pointers to0
and sets n=0. Reset has priority over requests. Clearing every memory cell is not
required to make the abstract queue empty; data confidentiality would need a
separate erasure contract.

Before each active edge, compute

\[
 pop\_fire=pop\land(n>0),\qquad
 push\_fire=push\land(n<DEPTH\lor pop\_fire).
\]

At a full queue, a simultaneous real pop makes room for the offered replacement.
At an empty queue, pop_fire is false even if push is true: there is no same-cycle
fall-through transfer. The new word becomes available after that edge.
Consumer data is the **old head** when pop_fire is true. The post-edge visible
head may be a different word. An interface that observes only the post-edge head
must not mistake it for the word just consumed.

| Before edge | Requests | Fires | After edge |
| --- | --- | --- | --- |
|Empty |push+pop |push only |one queued word |
|Full |push only |neither |unchanged |
|Full |push+pop |both |old head removed, new tail appended, still full |
|Partly occupied |pop only |pop |occupancy decreases by1 |
|Any |reset+any requests |reset wins |empty |

Update n'=n+push_fire-pop_fire. This single expression explains why two independent
signal assignments to n are a bug: the last scheduled assignment can overwrite
the first instead of combining the two changes. Update wr only when a push fires,
rd only when a pop fires. Each pointer wraps explicitly at DEPTH-1. The examples
use DEPTH=3 so a power-of-two bit-truncation shortcut fails visibly.

For old queue[4,7,9] and push12/pop1, the consumed word is4 and the new queue is
[7,9,12]. For old queue[] and the same requests, no word is consumed and the new
queue is[12]. These two traces expose a hidden assumption that “simultaneous”
always means the same thing at every boundary.

## Invariant argument

If n=0, pop_fire=0; a fired push gives n'=1, otherwise0. If n=DEPTH and no pop
fires, push is blocked and n remains DEPTH. If a pop fires at full, one push can
replace it and n stays DEPTH, or no push gives DEPTH-1. Interior states can change
by only-1,0,+1. Thus occupancy stays bounded by induction from reset.

Order is preserved because a pop advances only the read position and removes
only the old head; a push writes only the next tail cell. At full occupancy the
read and write pointer coincide, but simultaneous consumption sees the old head
before the clocked write commits. After both pointers advance, the overwritten
cell is logically the new tail. This argument assumes the modeled register-array
read behavior. An inferred block RAM's read-during-write mode can differ; adapting
the design requires checking that memory primitive's contract and latency.

## Read the SystemVerilog mechanism

A module declares ports and parameters; WIDTH determines vector width. logic
variables hold simulation values, while continuous assign statements describe
combinational relationships. They do not wait for the procedural line above them
to run. The @(posedge clk) block describes an active clock event. Nonblocking
assignments such as rd<=next_ptr(rd) evaluate from current state and schedule
updates; they do not make downstream state read a newly updated rd immediately.
The case on the two fire bits combines the occupancy changes once.

An integer pointer is deliberately readable here. It is not an area-optimized
encoding or a promise that a synthesis tool will choose a particular register
width. The active data path has WIDTH-bit words. Parameters are positive by
contract; supplied test configuration is DEPTH3,WIDTH4. Full parameter-space
verification is not claimed.

## Read the VHDL mechanism

An entity declares the interface; an architecture declares its implementation.
The generic DEPTH is a positive integer. unsigned(WIDTH-1 downto0) comes from
ieee.numeric_std and supports explicitly unsigned arithmetic/conversions. The
memory type is an array of those words. natural range declarations constrain
pointer and occupancy values in simulation; violating the declared range is an
error, not automatic modulo arithmetic.

Concurrent <= assignments connect outputs to state. Inside process(clk),
rising_edge(clk) selects the sampling event. Signal assignment <= schedules a
new signal value; := assigns a process-local variable immediately. Therefore
we calculate take_pop with := before calculating take_push, so the latter uses
that same event's Boolean result. If both were signals assigned with <= and then
read immediately, the old signal value could be used. The count signal is still
updated once from the old occupancy. VHDL case-insensitivity does not remove its
type distinctions; mixing std_logic and boolean requires an explicit expression
or conversion.

The testbench drives requests while the clock is low, waits, checks that state
has not changed without an edge, raises the clock, waits for scheduled updates,
then checks occupancy/head/full/empty. A delay in a testbench is simulation
instrumentation, not synthesized delay hardware. The IEEE multivalue library
also includes unknown/weak states, while generated stimuli in this unit are
restricted to binary inputs. No universal X-propagation claim follows.

## Build it in milestones

1. Implement a plain list/deque acceptance model and the two boundary traces.
2. Derive the invariant and represent the queue with pointers and fixed cells.
3. Write a positive-edge implementation with reset priority and one occupancy
   update. Check empty/full before optimizing anything.
4. Port the state contract to the other HDL; explain signal/variable scheduling.
5. Generate independent requests and compare all visible post-edge state, retaining
   both implementations' actual outputs and tool versions.
6. Introduce the two specified mutants and confirm failure at the intended queue
   assertion. A compiler syntax error is not the intended negative control.
7. Reconstruct a small depth without copying source and justify its memory mode,
   timing boundary and reset/data-erasure distinction.

```sh
python3 hardware-description-languages/fifo-contract/run.py
python3 hardware-description-languages/fifo-contract/run.py --language sv
python3 hardware-description-languages/fifo-contract/run.py --language vhdl
```

The full run requires iverilog/vvp and ghdl on PATH. Missing tools are BLOCKED;
they are not simulated by Python as a substitute. No third-party Python package
is needed. The runner works in temporary directories and records exact compiler
and simulator commands. [fifo.sv](fifo.sv) and [fifo.vhd](fifo.vhd) are reference
solutions; the [practice](EXERCISES.md), [hints](HINTS.md) and
[solutions](SOLUTIONS.md) separate learner attempts from them.

## Actual experiment and what it supports

The question was whether both HDLs implement the same declared boundary contract,
and whether two plausible semantic defects are detected. A fixed independent
Python deque generates short binary-content queue states/input combinations,
then2000 seeded cycles with values0..15, wrapping pointers and occasional resets.
This produced2992 vectors. Both reference HDL simulations passed all vectors.
For each language, rejecting full replacement and decrementing count on a
simultaneous transfer both failed the intended queue-transition assertion.
[evidence/observed.json](evidence/observed.json) retains actual commands, outputs,
vector hash and code hashes. Tool versions were Icarus12.0 and GHDL4.1.0.

These are finite functional observations, not exhaustive RTL state-space proof.
The short cases reset between constructions; long random cases cover additional
pointer histories but not every possible history. No synthesis, routed path,
setup/hold measurement, metastability, asynchronous crossing, real RAM mode or
production deployment was executed. Follow-ups include parameter sweeps, an
independent consumed-word scoreboard, a registered-read RAM version, formal
invariant checking and a separately specified multi-clock design. Do not extend
this single-clock count across independent clocks without a new protocol.
