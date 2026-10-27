# Investigation tasks

Record attempts and predictions before opening hints or solutions. Q and U are
the coordinate and drive units declared by the public boundary.

1. Derive the units of a,b,c,g,o,α andω from `a q''+b q'+c q=u` and `y=gq+o`.
2. A reference at−.01Q reads14counts and at.01Q reads6counts. Calibrate a reading8.
3. Your calibrated affine detector predicts10 at q=0, but a third reading is11.
   What can you conclude with and without an independently justified error bound?
4. Drives−.3U and.6U settle at8.3333333 and58.3333333counts. With gain1000 and
   offset25, calculate both coordinates and c. Why do differences help?
5. For a=2,b=.8,c=18, derive α,ω and the cosine/sine weights for q0=.01,v0=0.
6. Derive the power balance. Calculate stored energy at q=.01,v=0 for this
   mechanical model and decide whether its initial dissipation rate is positive.
7. Derive the sampled recurrence from conjugate powers. Evaluate its coefficients
   at h=.05s for task5 and explain the negative sign on C_d.
8. Generate z0=1,z1=0 and the next four exact rational samples under
   `z[n+2]=(3/4)z[n+1]-(1/4)z[n]`. Recover the sampled pole radius.
9. Differentiate the least-squares objective with respect to both coefficients.
   Derive the2×2 elimination formulas and state when division is invalid.
10. All ten samples equal1. Show that infinitely many recurrence coefficients
    fit. Explain why the number of samples does not solve this ambiguity.
11. Prove the free-response scale ambiguity between(2,.8,18) and(6,2.4,54).
    Design one allowed intervention to distinguish them and predict equilibrium.
12. Construct an alias pair at h=.2 with α=.2 and frequencies3 and3+10πrad/s.
    Choose q0,v0 so their sampled traces agree, and explain the acos branch limit.
13. Would collecting another hour at the same interval necessarily eliminate
    task12's alias? Propose a useful additional constraint or intervention.
14. Fit amber with the detector offset incorrectly set to zero. Before running,
    predict a failure in changed-drive holdout. After running, explain whether a
    small one-step residual establishes the correct state law.
15. Design a sampling-interval experiment that keeps the observation horizon and
    noise magnitude fixed. How many samples correspond to h=.2,.05,.005 over10s?
    Explain why noisy regressors can defeat this estimator despite more samples.
16. Specify and execute negative tests for zero excitation, nonfinite samples,
    too many samples, a growing fitted pole and an overdamped candidate.
17. Give the time/memory cost of the present fit. Explain why normal equations
    need conditioning checks and what a QR-based extension would change.
18. Reinterpret a=2,b=.8,c=18 as a series RLC charge-coordinate port. Give L,R,C,
    the two stored-energy terms, and a reason the same numeric trace cannot
    establish the internal physical topology.
19. Reconstruct calibration, normal sums, pole recovery and constant-drive
    prediction from memory in a new file. Pass the declared unseen holdout for
    all four cases without importing either reference or reveal.
20. Transfer the investigation to an actual unfamiliar passive device. Name
    the missing measurement references, safety/energy boundary, settling rule,
    instrument-loading checks and a new observable needed to separate two
    port-equivalent physical interpretations. State what remains hypothetical.
