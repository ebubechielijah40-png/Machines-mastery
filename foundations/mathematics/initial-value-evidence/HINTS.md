# Hints

1–2. Divide force by mass; subtractF/b before applying an integrating factor.
3–4. Start the next step from the corrected state, not the previous predictor.
5–6. A geometric sum accounts for propagation. Use(exp(LT)-1)/L→T.
7–9. Every RK4 stage starts from the same originaly with a different increment.
Expand coefficients symbolically, not with a second copy of the stage loop.
10–12. Sign and magnitude answer different questions. Repeated multiplication
by-19 can overwhelm a tiny positive starting value.
13–15. Cross terms cancel. A positive invariant bounds state only while its
quadratic is positive definite; use determinant and trace to inspect phase.
16–18. Two half steps contribute two local errors of size(h/2)⁵. Rejected attempts
still perform work. Keep component units visible in the tolerance denominator.
19–20. Expand(1-u)⁶ and integrate seven monomials. Supplying an event's support
is additional model knowledge; do not silently rename it automatic detection.
21–22. Check derivatives at the waiting-time join; separate dy/y²=dt for blowup.
23–24. Compare dimensionlessh/(RC), not the numericalh alone. At very larget,
ask whether addingh changes its floating representation at all.
