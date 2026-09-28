# Holding a value is behavior over time

[EXPLANATION] A device receives a new 4-bit setting, but should commit it only when enable is asserted at a rising clock edge. Reset should clear it even if enable is also true. A wire alone continuously exposes input; we need retained state to keep an earlier value. This motivates a register and an explicit update rule rather than a software assignment executed once.

The interface has clk, reset, enable and four-bit d inputs and four-bit q output. Logical state is q. A rising edge means clk changes from 0 to 1 in this bounded two-state model. At each rising edge: if reset is 1, q_next=0; otherwise if enable is 1, q_next=d; otherwise q_next=q. Between rising edges q holds. Reset is synchronous: changing reset alone between edges does not update q. Initial q is unspecified until the first effective reset; our testbench establishes it before comparing values.

```text
d ------------+             +-------------+
0 -----[priority choice]---->| clocked q   |----> q
q feedback ---+             +-------------+
             reset/enable          clk
```

For q=9, d=3, reset=0, enable=0, the next value is 9. With enable=1 it is 3. With reset=1 it is 0 regardless of enable. This last combined-input case catches an implementation that gives enable the wrong priority. Input changes between clock edges do not alter the committed state.

## Read the description as hardware intent

A module declares ports and a component boundary. `logic [3:0]` declares four positions indexed 3 through 0, not a variable-length software list. `always_ff @(posedge clk)` describes a clock-event process. `if` chooses a next-state rule, and `<=` schedules a nonblocking assignment. [SOURCE] The inspected AMD synthesis documentation distinguishes always_comb from always_ff; [sources](SOURCES.md) identify exact evidence.

[EXPLANATION] In our RTL, the absence of an else assignment in a clocked process means retain state. In an incomplete combinational process, retaining an old value may instead infer a latch and violate an intended pure function. Those situations are different. `logic` by itself does not promise a physical flip-flop; the behavior and synthesis context determine hardware inference.

Nonblocking assignment separates evaluating the right-hand side at the triggering event from updating the left-hand side later in the simulation scheduling sequence. Two clocked registers described with `a <= b; b <= a;` use the old values and swap in the intended model. Replacing these with ordered blocking assignments inside one process can make both take the same old value. Our one-register model does not require the full scheduler standard, but the testbench must avoid sampling before its update.

## A waveform by reasoning

Let the initial reset edge occur at simulated time 5. q then becomes 0. Drive reset=0, enable=1, d=6 while clk is low; the next rising edge commits 6. Drive d=2 during the high phase: q remains 6. Disable before the next edge: q remains 6 there too. Assert reset while clk is low: q still remains 6 until the following rising edge, then becomes 0. These are model predictions. The time unit in the testbench is nanoseconds for simulation scheduling, not a measured device clock limit.

```text
edge          reset enable d   q after edge
reset edge      1      0    ?       0
load edge       0      1    6       6
hold edge       0      0    2       6
priority edge   1      1    9       0
```

## Correctness and implementation limits

The truth table has 16 current values * 16 input values * 2 resets * 2 enables = 1024 combinations. For each, one of three mutually prioritized cases yields the required next value. Initialization is deliberately excluded until reset; after reset, every case returns a four-bit value. That establishes the logical range invariant. A separate between-edge check verifies that d changes do not trigger state updates in this RTL model.

A synthesizer can realize a bank of state elements with selection logic. Tool mapping may use dedicated enable/reset support or equivalent multiplexing. RTL → elaboration fixes widths/hierarchy → synthesis transforms supported processes into a logic network → placement/routing maps physical resources. We have simulated only the RTL. Transistor behavior, supply voltage, propagation delay, setup/hold margins, clock distribution and metastability are not established by these tests. Physical implementation needs verified device data and timing analysis.

Alternatives: an asynchronous reset changes the event sensitivity and behavior between edges; it is not interchangeable. A combinational selector without state cannot hold the previous setting. A software variable may model the transition but is not automatically a physical register implementation. These alternatives solve different interface contracts.

## Debug using a distinguishing input

The deliberately broken reference gives enable precedence over reset. Most load-only tests pass. The input reset=1, enable=1, d≠0 distinguishes it immediately. The test harness requires the correct implementation to pass and the mutant to fail. This checks that the tests are sensitive to a real contract defect rather than merely compiling the same mistaken idea twice. A passing mutant would be a problem in the tests or the chosen mutation, not evidence of correctness.

Logical state storage is four bits; transition work is bounded in this example. Actual gate count, delay and power depend on mapping and device and remain unmeasured. Extending width changes storage and selection resources; claiming linear physical delay from the RTL would be unjustified.
