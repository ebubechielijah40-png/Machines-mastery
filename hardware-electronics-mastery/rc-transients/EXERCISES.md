# RC exercises: attempt before revealing solutions

Record units, assumptions and predictions with each answer. The reference
implementation is an answer key, not the required derivation.

## Basic understanding

1. Convert `4.7 kΩ`, `22 μF` and `15 ms` to SI. Compute `RC` and `t/(RC)`.
   Which of these quantities can legally be an argument of `exp`?
2. A `10 μF` capacitor gains `2 μC` in `1 ms`. Find the voltage change and
   average current. Does this determine instantaneous current throughout the interval?
3. For `V_s=5 V`, `R=2 kΩ`, `C=2 μF`, `v_0=1 V`, derive `v(t)` and evaluate
   it at one time constant. State the initial current direction and magnitude.
4. For the same `R,C`, discharge a capacitor initially at `5 V` to `0 V`.
   Find the time to `1 V` and the sign of current under the lesson convention.
5. Find the times to 50%, 90%, 100% and 110% of supply starting from zero.
   Explain which answers are finite, asymptotic or unreachable without trying
   to take a logarithm outside its domain.

## Applications

6. A nominal delay must reach half supply in `0.2 s` using `C=10 μF`.
   Derive the required ideal resistance. If capacitance can vary ±20%,
   give worst-case delay bounds at fixed exact resistance and threshold fraction.
7. A source of `4 V` drives `R=100 kΩ`, `C=1 μF` observed through a
   hypothetical `R_m=100 kΩ` meter with negligible added capacitance.
   Derive the endpoint and time constant from node-current balance. Is `3 V`
   reachable? Why is using the unloaded threshold helper wrong?
8. For initially uncharged charging with `C=22 μF` and `V_s=5 V`, calculate
   limiting source work, capacitor energy and resistor loss. If `R` doubles,
   which values change? Which time-dependent quantities do change?

## Reasoning and debugging

9. Someone computes `exp(-t/R*C)` and obtains a smooth-looking curve.
   Find the mathematical and unit error. Give an invariant or scaling test
   that catches the bug without prescribing a single expected number.
10. Forward Euler at `h=2τ` alternates between `0` and `2V_s`. A learner
    concludes that an RC circuit is an oscillator. Derive the algorithm's
    error recurrence, identify the inference failure, and design two controls
    that distinguish numerical artifact from real dynamics.

## Challenge

11. Two experiments have equal `RC`: A uses `R=1 kΩ,C=100 μF`; B uses
    `R=10 kΩ,C=10 μF`. Both use a `3 V` ideal source and start at zero.
    Prove equality of ideal voltage trajectories. Find ratios of initial
    current, final stored energy and instantaneous resistor power A/B.
    Can voltage data alone identify both `R` and `C`? Name one extra observation.

## Experimental task

12. Before running code, predict the Euler voltage error at `t=τ` for
    `N=10,20,40,80` equal steps. Execute both Euler variants and exact mode.
    Save parameters, commands and raw outputs, then compute adjacent error
    ratios. Keep the end time fixed. Explain why running each step size for
    ten steps does not measure convergence at a common physical time.

## Transfer and reconstruction

13. A lumped object cools in a constant-temperature environment, with stored
    thermal energy change `H dT` and heat outflow `G(T-T_env)dt` for positive
    heat capacity `H` in J/K and conductance `G` in W/K. Derive the equation,
    units of its time constant, exact solution and explicit-Euler stability
    bound. State two physical assumptions and an observation that would
    challenge the lumped model. Rebuild the RC model without opening its source.

## Evaluation rubric

- **Mechanism (0–3):** conservation → governing equation → initial condition,
  with a consistent sign convention and units.
- **Derivation (0–3):** correct general solution, threshold domain, numerical
  multiplier and at least one edge-case argument.
- **Implementation (0–3):** runnable reconstruction, boundary tests,
  independent oracle and failure diagnosis.
- **Evidence (0–3):** prediction saved before execution, actual raw output,
  correct interpretation, explicit simulation/measurement boundary.

A total alone does not establish mastery. A zero in any category calls for
remediation; repeat an unaided transfer/reconstruction after a delay before
claiming retention. [Hints](hints/README.md) and
[solutions](solutions/README.md) are separate to protect the initial attempt.
