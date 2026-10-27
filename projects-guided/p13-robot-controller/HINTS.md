# Progressive help

Plant sign error: multiply the voltage equation by current and the torque equation
by speed. The two kiω terms must cancel in total stored-energy rate. If they add,
the electrical back-EMF or mechanical torque sign is wrong.

Gear error: equate kinetic energies before equating torques. Output speed is
motor speed/G; its square makes reflected inertia J_load/G².

Integrator error: clipping the final command does not clip the integral state.
Form a candidate integral, then reject only increments that drive farther into
saturation. A negative error should still be able to unwind a positive integral.

Sensor error: distinguish true state from measured history. With positive fixed
bias c and near-zero measured steady error, true speed approaches target−c.
The controller cannot infer calibration from its own biased feedback alone.

For derivative noise, examine the difference divided by dt; reducing dt can
magnify noisy differences. For suspicious delay claims, compare multiple metrics
and preserve contradictory results. Use the separate
[solutions](../../17-embedded-robotics/control-path/SOLUTIONS.md) after writing a derivation.
