# Attempts before references

Keep equations, units, predictions and tests with each answer. The code and raw
synthetic results are references, not evidence that a learner performed the work.

1. Distinguish an atom, an ion, a molecule, a crystal and a material sample.
   Which description is enough to specify a real modulus?
2. Convert a circular diameter of2 mm to area in m². Explain why2 mm² is different.
3. Derive U(r0) and both displayed derivatives from the defined energy law.
4. Explain the signs of internal versus required force on each side of r0.
5. Why does U'=0 fail to guarantee stable equilibrium? Give an explicit function.
6. Derive the force-peak separation and identify the relevant stability condition
   for force control versus a prescribed displacement.
7. For D=2×10^-19 J, r0=2×10^-10 m, m=8, compute k and the ideal-chain E.
8. Double the number of series bonds and then the number of parallel chains.
   Track stiffness, modulus, length and area separately.
9. Reproduce the50 N bar trace, including stored energy. What changes on unloading
   in this model, and what material phenomena cannot be inferred?
10. Two assumed compliances2 and3 micrometers/N are connected in series, then
    in parallel. Derive each equivalent compliance without quoting a formula.
11. Two equal opposite50 N forces act at a bar's ends. Explain why saying
    “net force zero means stress zero” is wrong.
12. Derive the one-length family C_f=s-L/(AE), and bound E if C_f≥0. Is there an
    upper bound from that observation alone?
13. Construct two different physically admissible parameter pairs with the same
    one-length observations. Add more noiseless loads; explain the outcome.
14. Given L1=.1 m, L2=.2 m, A=10^-6 m², slopes6×10^-7 and11×10^-7 m/N,
    reconstruct E and C_f step by step.
15. Derive the centered fit by completing the square. Check both residual sums.
16. Show exactly how a positive offset biases a fit forced through the origin
    for nonnegative loads. Design a negative control that removes this error.
17. Derive the first-order relative uncertainty for modulus and for a diameter-
    derived area. Identify a possible covariance that invalidates independent sums.
18. Reduce the difference of specimen lengths by100 while keeping slope noise
    fixed. Predict the sensitivity before executing a seed sweep.
19. Modify the synthetic frame to include a quadratic term. Plot or tabulate
    residual versus load and explain which assumptions the line fit violates.
20. Diagnose a negative fitted frame compliance without clipping the result.
    List two observation-model failures and one numerical explanation to test.
21. Build an independent Fraction oracle for regression using at least20 small
    integer load/extension examples. Include a constant-load rejection case.
22. Reconstruct the two-length experiment from an empty file without opening
    materials.py. Supply a parameter recovery test, a non-identifiability
    counterexample and a report separating assumptions from actual run data.

Transfer: design a future physical measurement protocol specifying load path,
area/length measurement, calibration, sample conditioning, uncertainty, instrument
compliance identification, safe apparatus limits, acceptance criteria and failure
observations. Do not claim equipment was used when preparing that protocol.
