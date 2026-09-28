# Electrical energy and the digital abstraction

PREPARED; learner NOT STARTED. Unit F-ELECTRIC. Original explanation and derivation; see [foundation policy](../../README.md).

Why can a logic operation consume energy although we draw only zeros and ones? A logical drawing omits the physical system that maintains and changes distinguishable electrical conditions. Begin with quantities: charge Q is measured in coulombs; current I is charge crossing a boundary per time; voltage V is energy transferred per charge between two points. For a constant rate, I=ΔQ/Δt. For a constant potential difference, ΔE=VΔQ. Substitution into power P=ΔE/Δt yields P=VI. Units: (joule/coulomb)*(coulomb/second)=joule/second, a watt. These definitions motivate the derivation; signs depend on the declared direction and passive sign convention.

For an invented constant load at 2 V taking 0.01 A, power received is 0.02 W; over 5 s, E=Pt=0.1 J. Doubling voltage while holding current constant doubles power, but a real load may change current. The statement that current stays fixed is an assumption, not a law. For an ideal ohmic resistor, V=IR defines proportional behavior with resistance R in ohms. Substituting gives P=I^2 R. Real devices need measured or sourced operating limits.

```text
source -> energy transfer -> load -> stored energy / heat / other work
signal -> interpreted level -> logical value (a separate abstraction)
```

A switch changes whether a conducting path is available. A transistor can control a path electrically; this lesson does not specify its device physics, pinout or safe limits. A logic receiver classifies ranges of voltage into logical values. Thresholds, supply range and noise margins are device-specific: UNVERIFIED — verification required. Voltages in the excluded region may not have a reliable logical interpretation. A flip-flop model samples logical inputs at a clock event; real storage also needs power and timing margins. Setup and hold name intervals around that event in which input stability is required for specified behavior. RTL tests do not measure those intervals or eliminate metastability.

Wrong: a digital zero means no electrical activity or energy. Correct: it is an interpreted state, not an energy balance. Edge: zero current makes VI zero for that ideal port, but other ports can still transfer energy. Application: the SystemVerilog unit validates a Boolean transition contract only. A physical implementation requires device datasheets, circuit theory and measurements before energizing anything. The prepared experiment uses an energy ledger on paper; no equipment, current or voltage observation is asserted.

Study [problems](problems/README.md), then [hints](hints/README.md) after an attempt. [Solutions](solutions/README.md) are separate. Complete the [experiment](experiments/README.md) and transfer before returning to the dependent unit.
