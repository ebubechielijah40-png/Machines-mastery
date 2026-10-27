# Motor/control exercises

1. Derive the units of every term in the electrical and mechanical equations.
2. Recompute the hand derivative and energy balance after changing load to .04 N·m.
3. At zero supply/load, prove the continuous stored-energy rate is nonpositive.
4. Derive the no-load steady speed. How much voltage is needed for 20 rad/s?
5. Derive the steady speed with load .05 N·m at 6 V. Which modeled assumptions
   are least credible close to a stall or reversal?
6. A gear reduces speed by five. Reflect .5 kg·m² load inertia to the motor and
   verify equal kinetic energy at motor speed 10 rad/s.
7. Derive the derivative-on-measurement term. Give a target step for which
   derivative-on-error has a kick but the reference does not.
8. Trace five conditional-integrator steps with Kp=1, Ki=1, U=2, dt=.1 and
   errors [3,3,1,-1,-3]. State each integral and clipped command.
9. A sensor reads true speed plus .4 rad/s bias. If measured error tends to zero
   at a 3 rad/s target, what true speed follows? Can more repeat samples remove it?
10. Show by a counterexample why clipping output while integrating error does
    not guarantee quick recovery.
11. Predict and run an additional delay/gain pair. Compare true/observed error,
    record the trace and identify what the one run does not establish.
12. Reconstruct the model, controller and sensor from blank files. Replace the
    motor by a force-driven translating mass; map each parameter and its units,
    then identify which electrical/back-EMF terms no longer apply.
