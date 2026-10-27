# Explained solutions and checkable contracts

1. `a:Us²/Q`, `b:Us/Q`, `c:U/Q`, `g:counts/Q`, `o:counts`, `α:s^-1`,
   `ω:rad/s`. Radians describe phase and are dimensionless in dimensional algebra.
   A slope in counts/s is not velocity until the detector map is calibrated.
2. `g=(6−14)/(.01+.01)=−400`, `o=14−(−400)(−.01)=10`.
   `q=(8−10)/(−400)=.005Q`. Taking abs(g) would reverse the coordinate sign.
3. The affine model has a residual+1count at that reference. This can be noise,
   drift, bad references or nonlinearity. If every relevant error were bounded
   tightly enough that+1 cannot occur, reject that model/premise combination.
   Without that bound, the observation raises a question rather than proving
   a particular fault. Repeated and separated references distinguish hypotheses.
4. q0≈−.0166666667Q and q1≈.0333333333Q; `c=.9/.05=18U/Q`.
   A fixed additive detector offset cancels, but gain error still scales the
   estimate. A changing bias between the two interventions does not cancel.
5. `α=.8/4=.2/s`, `ω=sqrt(9−.04)=sqrt(8.96)≈2.99332590942rad/s`.
   A=.01Q and `B=(0+.2*.01)/ω≈.000668153105Q`.
   Omitting the sine term gives initial rate−.002Q/s, violating the stated reset.
6. Product differentiation gives `E'=u v−b v²` for
   `E=.5a v²+.5c q²`. Initially E=.0009J and, for u=0,v=0, E'=0.
   The acceleration is nonzero, so the mass soon moves and dissipates energy.
   Initial zero dissipation is not undamped motion.
7. The two sampled roots have sum`2e^(-αh)cos(ωh)` and product`e^(-2αh)`.
   Moving the product term to the right yields C_d negative.
   At h=.05, A_d≈1.95796391760847, C_d≈−.980198673306755.
8. Samples are`1,0,−1/4,−3/16,−5/64,−3/256`.
   The radius is sqrt(1/4)=1/2. It is not the ratio of two successive values:
   that ratio also depends on oscillatory phase and may be undefined at zero.
9. Derivatives give`Σx(t−Ax−Cy)=0` and`Σy(t−Ax−Cy)=0`.
   With X,Y,Z,P,Q as in the lesson, D=XY−Z²,
   `A=(PY−QZ)/D`, `C=(QX−PZ)/D`. D=0 prevents a unique two-parameter
   solution; a tiny D relative to XY makes finite-precision estimates fragile.
10. Every recurrence row requires`1=A+C`. Any A with C=1−A fits the observed
    sequence; all design rows are the same. Ten copies of one constraint remain
    one independent constraint. More diverse excitation is needed.
11. Dividing either free equation by a yields `q''+.4q'+9q=0`.
    For a common nonzero constant drive1U, equilibrium is1/18 versus1/54Q.
    Balance supplies absolute scale only because drive/reference units are known.
12. Use q0=.01,v0=−.002. Both responses are`.01e^(-.2t)cos(ωt)`.
    At t=.2n, the higher frequency adds2πn to phase, leaving samples unchanged.
    The inverse cosine selects a principal angle in[0,π], not a proof about the
    unobserved continuous frequency. In this pair it reports3rad/s.
13. No: every added sample at another integer grid index still has the same
    alias relation. An independently known upper frequency bound can select a
    branch; a noncommensurate new sampling interval can falsify this particular
    alias. Neither action automatically rules out every possible hidden system.
14. See the actual raw `omitted_offset` result. This run fits inertia≈114.045
    and loss≈29.177 instead of2 and.8; changed-drive holdout error≈.03883Q.
    The offset leaves a constant term in the supposed free coordinates, so the
    homogeneous recurrence fits a false compromise. A residual must be assessed
    alongside instrument premises and intervention transfer.
15. Counts are51,201,2001, including both endpoints. Keep horizon10s and the
    same detector-count noise bound; preserve each seed separately. As h shrinks,
    x and y columns become similar and noise changes both regressors and target.
    Ordinary least squares' noiseless-regressor premise is violated. Increasing
    N does not in general remove that bias; the observed refusals are informative.
16. The supplied test suite exercises these cases. All-zero samples carry no
    pole information; nonfinite/excessive input is outside the numerical contract.
    A fitted radius>1 beyond tolerance violates the non-growing restriction.
    `b²≥4ac` lies outside this reference's strictly underdamped family; refuse
    it rather than taking a square root of a negative frequency argument.
17. The fit visits N samples a fixed number of times, O(N) arithmetic and O(N)
    memory here. A streaming sufficient-sums implementation could reduce working
    memory but would still need input/resource contracts and stable summation.
    Normal equations square conditioning; QR changes the solve's numerical
    behavior, not topology identifiability or the noise-in-regressors premise.
18. `L=2H`, `R=.8Ω`, `C=1/18F`. Magnetic energy`.5L I²` and electric energy
    `.5q²/C` map to the same numeric expression as kinetic/spring energy.
    A matching boundary equation supports equivalent port behavior under the
    stated model, not a unique internal component arrangement or material.
19. A checkable solution accepts only the prompt's inputs, recovers the stated
    clean holdout to≤1e-9Q in all four cases, includes negative gain, rejects
    singular/out-of-contract data and reproduces both scale/alias counterexamples.
    The reference is one solution, not an architecture requirement. An imported
    reference or copied formula without derivation fails the memory condition.
20. A defensible transfer proposal identifies trusted force/voltage and
    displacement/charge references, detector gain/offset/uncertainty, rated
    energy limits, safe accessible ports, a quantitative settling/drift criterion
    and instrument-loading tests. Observe independently evidenced motion or
    fields, or inspect a verified internal interface, to separate physical
    interpretations that are equal at the original port. The proposal remains
    hypothetical until authorized apparatus measurements exist; software
    agreement does not provide ratings, isolation or a safe wiring plan.
