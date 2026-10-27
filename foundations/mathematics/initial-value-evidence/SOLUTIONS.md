# Checkable solutions

1. m:kg,b:kg/s,F:kg·m/s²,v:m/s,τ:s,f:m/s². A rate law gives a slope at a
   state; the initial condition selects the starting state/trajectory.
2. v*=F/b,τ=m/b. Withu=v-v*,d(e^(t/τ)u)/dt=0, so
   v=v*+(v0-v*)exp(-t/τ). At.5s the answer is.9481808382m/s.
3. Start slopes3 then1.5 produce.75 then1.125. Acceleration decreases within
   each interval, so a left-endpoint rectangle overestimates its integral.
4. First predictor.75,accepted.5625; second predictor1.03125,accepted.9140625.
   Predicted endpoints are derivative-evaluation inputs; correction is the update.
5. Exact Taylor has h²y''/2+O(h³) beyond Euler's increment. On a fixed interval
   there areT/h steps, and a stable propagation bound gives globalO(h). This is
   conditional on bounded derivatives and propagation, not a universal counting proof.
6. eN≤Mh²/2Σj=0..N-1(1+hL)^j=Mh((1+hL)^N-1)/(2L).
   Bound powers byexp(LT); itsL→0 limit isMTh/2. Add(1+hL)^Ne0. Calibration,
   parameter/model error and finite arithmetic have not been bounded here.
7. k=(-1,-.75,-.8125,-.59375);y+=.6067708333333 versus
   exp(-.5)=.6065306597126. Signed error≈+.0002401736207.
8. k2=λy(1+z/2),k3=λy(1+z/2+z²/4),k4=λy(1+z+z²/2+z³/4).
   Substitution givesR=1+z+z²/2+z³/6+z⁴/24. Nonlinear mixed derivatives are not
   constrained by this one linear test equation.
9. z=-1/4. Euler gives9/16; Heun multiplier25/32 gives75/128; RK4 multiplier
   4785/6144 gives14355/24576. These exact polynomials avoid copying the tested
   stage loop and expose wrong coefficients or signs independently.
10. Multipliers .5,0,-.5,-1,-2: positive shrinking, one-step zero, alternating
    shrinking, alternating constant magnitude, alternating growing. The numerical
    zero is not the exact exponential trajectory. Strict decay excludeshk=2.
11. Solvey+=y-hky+ to obtainy/(1+hk). Multiplier1/101≈.00990099 differs greatly
    fromexp(-100)≈3.72008e-44. Stable positivity does not resolve the fast transient.
12. Ath=.02 the fast multiplier is-19, so50 steps amplify by19⁵⁰. A reduced
    slow model needs a justified transient/observability or scale-separation
    argument. Removing an apparently tiny mode that drives a constraint or sensor
    can remove the failure mechanism under investigation.
13. (v-hω²x)²+ω²(x+hv)²=(1+h²ω²)(v²+ω²x²). Iterate the multiplier:
    EN=E0(1+h²ω²)^N. A closed energy formula is independent of the state loop.
14. A=[[1-h²ω²,h],[-hω²,1]],detA=1. Let
    M=[[ω²,-hω²/2],[-hω²/2,1]]. MultiplyingAᵀMA returns the same four entries,
    so the quadratic is invariant in exact arithmetic for every input state.
15. Q=(v-hω²x/2)²+ω²(1-h²ω²/4)x². Athω=2 it ceases to bound both coordinates.
    Within0<hω<2,eigenvaluesexp(±iθ) satisfycosθ=1-h²ω²/2;θ/h generally differs
    fromω. A time-of-peak or phase error can accumulate while energy remains bounded.
16. Coarse errorCh⁵,fine error2C(h/2)⁵=Ch⁵/16; their difference is15Ch⁵/16.
    Fine error is approximately difference/15 when the same leading smooth local
    error model applies. Entirely unsampled structure defeats that inference.
17. x_mm=1000x_m,f_mm=1000f_m,a_mm=1000a_m;r unchanged. Normalized ratios match
    in exact arithmetic, so decisions match; roundoff can perturb a near-threshold
    decision. Rescaling only state, without its tolerance, changes the procedure.
18. 12(44+3)=564calls. With budget11, the twelfth evaluation raisesContractError;
    the solve returns no successful trajectory or relaxed tolerance.
19. Σj=0..6(-1)^j choose(6,j)/(7+j)=1/12012. Distinct stage times are
    {0,.25,.5,.75,1}. All miss(.1,.15), so the accepted output is0 even though
    the normalized exact integral is1.
20. Supply[.1,.15]and hold method/tolerance fixed; outside it the derivative is
    known0. The actual informed result is near1. This tests supplied localization,
    not a general detector or certified global error policy.
21. Afterc,y=(t-c)² has derivative2(t-c)=2√y; beforec both sides0. Atc the
    derivatives agree. sqrt(y)/y=1/sqrt(y) diverges near0, so no local
    state-Lipschitz bound holds there. Infinitely many waiting times are valid.
22. Integratingdy/y²=dt gives-1/y=t-1, hencey=1/(1-t) for0≤t<1. At1 the
    classical solution becomes unbounded. A finite extrapolated output beyond
    that point supplies neither continuation nor correctness evidence.
23. RC stateV hasV'=(Vin-V)/(RC),withRC seconds. Spring states(x,v) have
    derivatives(v,-kx/m),withω²=k/m. Consistent millisecond/second conversion
    preservesh/(RC) and physical outputs. Varying onlyh across a derived
    stability threshold tests the integrator; inconsistent units test another bug.
24. A valid submission uses fresh code and a polynomial/exponential/rational
    oracle, includes ordinary and adversarial cases, and explains each outcome.
    At1e16 adjacent float times are separated by2; four requested intervals
    beforet+2 cannot advance every mesh point. The reference rejects this.
    One pulse test cannot certify all input detection, global accuracy, real
    sensor calibration or the model's correspondence with physical reality.
