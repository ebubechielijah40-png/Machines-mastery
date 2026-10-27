# Saturation, sensing and recovery

Research question: does integral memory accumulated during an impossible command
impair later recovery? Predict that conditional integration reduces post-switch
absolute true-speed error, while a sensor offset drives true speed away from the
requested value. Use the same hypothetical motor,6V bound, gains,0initial state,
.002s samples,8s horizon and target20rad/s until4s then2rad/s. Change exactly one
of anti-windup, delay100samples, bias+.5rad/s, or seeded noise/quantization.

Instrumentation records true/measured speed, current, integral, command,
saturation fraction and the post-switch sum |target−true_speed|dt (unitsrad).
Run the command in TESTS.md. Actual [raw JSON](../../17-embedded-robotics/control-path/evidence/control-experiment.json)
includes parameters, interpreter/platform and decimated trajectories. Conditional
integration ended near2.00753rad/s, versus7.51264 without it; chosen recovery
error integrals were3.65797 and38.7934rad. The bias case ended near1.50734rad/s.

The delayed case had a slightly smaller selected recovery integral,3.44923rad.
Do not hide it or claim delay always degrades all metrics. Different phase/gain
relationships can trade transient measures. Follow up by varying delay and gains
separately, extending the horizon and measuring overshoot/settling as well as
integrated error. Noise results are one seeded synthetic realization, not measured
sensor statistics or a confidence interval for a hardware population.

Alternative explanations include numerical step size, the assumed first-order
friction, and the particular target schedule. The recorded sample-refinement
runs check one numerical sensitivity; hidden current limits, nonlinear stiction
and thermal drift remain outside the plant. A physical experiment would need
independent calibration, timestamps and a current-limited test setup; none was run.
