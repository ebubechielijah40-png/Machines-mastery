# Reference reasoning and checkable results

1. Atomic number fixes proton count; an ion has nonzero net charge. Molecules
are bonded groups; a crystal has ordered structure; a sample has geometry,
processing history and defects. None of those labels alone specifies a modulus.
2. A=π(.002)²/4=π×10^-6 m²≈3.14159 mm²;2 mm² would be2×10^-6 m².
3–4. U(r0)=-D. Taking d(r^-m)/dr=-mr^(-m-1) gives the lesson's force and
curvature. Required force is negative for compression and positive for tension
near r0; internal force has opposite sign.
5. U(x)=-x² has U'(0)=0 but U''(0)=-2. A positive perturbation lowers energy
by moving farther from0.
6. Set (m+1)q^(m+2)=2q³, cancel q³>0, then invert q to obtain the peak ratio.
The locally stable force-controlled branch needs U''>0. A prescribed displacement
constrains the coordinate, so this one-coordinate instability criterion does not
assert that the clamp cannot hold the descending branch.
7. k=Dm/r0²=40 N/m; ideal-chain E=k/r0=200 GPa. Both follow from assumed values.
8. Doubling n doubles length and compliance, halving structural stiffness. Doubling
p doubles area and stiffness. In either case E=k/r0 stays fixed in the ideal model.
9. σ=50 MPa, ε=.00025, δ=25 micrometers, stored energy=.000625 J. Ideal unloading
returns the stored energy with no permanent set; it supplies no fatigue or fracture
prediction. A real material can violate these assumptions.
10. Series C=5 micrometers/N. Parallel1/C=1/2+1/3 in reciprocal units, so
C=6/5=1.2 micrometers/N. Derive the first from common F and the second from common δ.
11. A cut through the bar reveals internal axial force50 N across its section.
The balancing end forces prevent center-of-mass acceleration; they do not remove
that transmitted force.
12. C_f=s-L/(AE). Requiring C_f≥0 gives E≥L/(As), with strict positivity of E
and s. Arbitrarily large E remains possible as C_f approaches s from below.
13. At .1 m and10^-6 m², E=200 GPa,C_f=10^-7 m/N and E=250 GPa,C_f=2×10^-7 m/N
both give s=6×10^-7 m/N. More loads identify the same slope more precisely but do
not create a second independent equation for E and C_f.
14. ΔL=.1 m and Δs=5×10^-7 m/N. E=.1/[(10^-6)(5×10^-7)]=2×10^11 Pa.
C_f=6×10^-7-.1/[(10^-6)(2×10^11)]=10^-7 m/N.
15. For fixed s the best b sets the residual mean to zero. Centering then gives
S_yy-2sS_Fy+s²S_FF=S_FF(s-S_Fy/S_FF)²+constant. At that minimizer both Σr and ΣFr
are zero in exact arithmetic. Floating versions should use a scale-aware tolerance.
16. Insert y=b+sF into s0=ΣFy/ΣF². The bias is bΣF/ΣF², positive for b>0 and
nonnegative nonzero loads. An independently validated zero offset or an unconstrained
intercept removes this particular bias. It does not remove frame compliance.
17. Partial derivatives are E/L, -E/A and -E/C_s. Independent variance propagation
gives the displayed relative sum. For A=πd²/4, dA/dd=πd/2 and u_A/A≈2u_d/d.
A shared ruler scale error in L1 and L2 introduces covariance; a shared frame or
load calibration error can correlate slopes.
18. When Δs scales down by100 at the same absolute noise, relative modulus error
from slope differencing scales up by roughly100 under first-order propagation.
Once noise competes with Δs, inversion can become strongly asymmetric or invalid;
a linear uncertainty approximation may fail.
19. Curved mean residuals versus load indicate that the linear frame/specimen
observation equation is inadequate. A small overall residual sum is guaranteed
by the fit and does not rule out that curvature. Preserve the raw data and report
both the changed generating equation and fitted model.
20. Negative frame estimates can arise from random slope error, length/area errors,
changed gripping, load-dependent frame compliance or an invalid constant-modulus
assumption. Catastrophic cancellation for almost equal slopes is another candidate.
Check exact/noiseless examples and vary the design before attributing the sign.
21. The test suite supplies100 Fraction-generated comparisons and a constant-load
rejection. A learner solution is independently checkable if it computes means,
centered sums and the rational result before comparing floating output.
22. A satisfactory reconstruction identifies all parameters/units, produces the
noiseless hand result, retains a one-length counterexample, implements residual
checks, and distinguishes synthetic observations from physical calibration.

Rubric: correct mechanism/units4 points; derivation and assumption boundaries4;
independent tests/failure cases4; experiment interpretation4; unaided rebuild and
transfer4. Scores are learner assessment only after reviewing an actual attempt.
No author-generated score is assigned to the learner.
