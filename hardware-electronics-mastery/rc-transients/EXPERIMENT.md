# RC simulation experiment — executed, physical validation outstanding

**Research question:** when does a finite-step approximation violate the
monotonic behavior of an ideal first-order RC circuit, and how does a measurement
load bias an inferred time constant?

**Hypotheses written from the equations:** forward-Euler deviations multiply by
1-h/τ. At ratios0.5,1.5,2,2.5 they respectively decay monotonically, alternate
and decay, alternate without decay, and grow. Halving a sufficiently small
step at fixed end time should approximately halve forward-Euler global error.
A finite parallel meter changes both equilibrium and time constant.

**Controlled variables:** constant3.3V source; R=10,000Ω; C=10µF; initial0V;
same Python process, source equation and analytic oracle. **Independent variables:**
step ratio/integration rule, then a declared meter/probe branch. The loading
case separately uses R=100kΩ,C=1µF,R_m=1MΩ,C_p=100pF. These are two specified
simulation setups, not a physical component comparison.

**Instrumentation:** exact exponential voltage, Euler/backward-Euler trajectories,
absolute end-time error in V, inferred τ in s, declared tolerance corner bounds.
Python/platform are emitted by the script. No timer or oscilloscope is used.

From the repository root:

```sh
python3 hardware-electronics-mastery/code/test_rc_lab.py
python3 hardware-electronics-mastery/code/run_rc_experiments.py
```

**Actual retained evidence:** [raw JSON](evidence/rc-experiment.json),
[test output](evidence/tests.txt). The integrated verification report separately
reruns the tests; neither log is learner evidence.

**Observed in this deterministic run:** exact voltage at τ was2.08599784413424V.
Forward-Euler errors with10,20,40,80,160 steps were approximately0.0633633,
0.0309986,0.0153351,0.00762728,0.00380367V. Step halving approached a factor-two
error reduction. This is evidence for first-order behavior in this tested regime,
not a proof of stability for a nonlinear circuit. The four stability trajectories
are retained in full, including the nonphysical growing/alternating cases.

The loading setup produced a3.0V asymptote and τ≈0.0909182s. The same generated
sample at0.05s gives different inferred τ if3.3V is incorrectly assumed as its
asymptote. Inspect both inference fields in the JSON; input assumptions can
bias an answer even when the inversion code is arithmetically correct.

**Interpretation/alternatives:** agreement with an analytic solution tests our
computer model. It cannot establish that a real capacitor is linear, a meter
has the hypothetical impedance, or the source is ideal. Numerical overshoot is
explained here by the step multiplier; real overshoot could involve additional
energy storage, source behavior, measurement ringing or wiring effects.

**Follow-ups:** hold RC fixed while varying R and C separately; compare voltage,
current and energy. Add a piecewise source and check continuity. Only after
obtaining appropriate equipment/specifications perform a low-energy physical
experiment with documented calibration, component uncertainty, sampling interval
and measurement loading. That physical procedure remains **NOT PERFORMED**.
