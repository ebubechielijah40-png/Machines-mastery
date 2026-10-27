# Derive, build, falsify and transfer

Record an attempt before consulting [hints](HINTS.md) or [solutions](SOLUTIONS.md).

1. Give units for cartm,b,F,v,τ andf. Explain what the initial condition adds.
2. Derivev* andτ for arbitrarym,b>0 and constantF, then the exact solution.
   Compute the lesson'sv(.5).
3. Work both cart Euler steps ath=.25, including start slopes. Explain the
   error direction from the rate's evolution, rather than the final numbers.
4. Work both Heun steps and distinguish each prediction from an accepted state.
5. Derive Euler's one-step defect from Taylor's formula. Why is global order
   one power lower under controlled error propagation?
6. Sum the stated Lipschitz error recurrence. TakeL→0 and add initial error.
   Identify which physical uncertainty this bound has not included.
7. Reconstruct the complete RK4 trace fory'=-y,y=1,h=.5 without opening code.
8. DeriveR(z) forRK4. Explain why matching a linear exponential series alone
   cannot prove all nonlinear order conditions.
9. For y=3/4,λ=-2,h=1/8, calculate all three one-step outputs exactly with
   Fraction. Explain why this oracle is independent of the implementation.
10. Forhk=.5,1,1.5,2,3, classify Euler's sign and strict decay in magnitude.
    Identify the physical and stability questions answered by each property.
11. Derive backward Euler's decay multiplier. Compare it with exact decay
    fork=1000,h=.1. Does positivity/stability make a transient accurate?
12. Explain why a component initially1e-6 can dictate explicit stability in
    the two-rate model. Give one justified and one unjustified reduction argument.
13. Expand Euler's oscillator energy update and derive itsN-step formula.
    Use that formula as a test without duplicating the state-update code.
14. Derive the velocity-first matrixA and checkdetA. Verify the full quadratic
    invariant by substitution or byAᵀMA=M, not just a numeric coincidence.
15. Complete its square, inspecthω=2, and derive the phase angle fromtraceA.
    Explain why bounded energy does not establish accurate timing of peaks.
16. Derive the divisor15 for step doubling and state its asymptotic assumptions.
17. Change one position coordinate from metres to millimetres. Transform its
    derivative and absolute tolerance; predict the normalized error decisions.
18. A run accepts44 steps and rejects3. Calculate field calls. Explain behavior
    if the callback budget permits only11 calls in a twelve-call attempt.
19. Independently integrateu⁶(1-u)⁶ by expansion and locate every distinct
    sampled time in the single[0,1]adaptive attempt. Predict its pulse output.
20. Design the known-support contrast with method and tolerances fixed. Explain
    what new information it supplies and what automatic capability it cannot prove.
21. Verify every waiting-time solution toy'=2√y and identify the missing
    regularity assumption behind a uniqueness claim.
22. Derive the finite-time blowup ofy'=y²,y(0)=1. Interpret a finite solver
    output aftert=1 without pretending it is an exact continued solution.
23. Transfer toRC and a mass-spring oscillator: state variables, units and laws.
    Design a controlled unit-conversion test and a separate step-stability test.
24. Close the reference. Rebuild Euler and one adaptive acceptance decision,
    design a smooth pulse between its samples, and compare with an independent
    integral. Include a zero-duration case, nonadvancing-time rejection and a
    model-uncertainty limitation. Submit prediction, raw run and interpretation.
