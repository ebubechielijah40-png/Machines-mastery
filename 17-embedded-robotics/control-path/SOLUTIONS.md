# Checkable solutions

1. Ri, L di/dt, kω are V. Ji acceleration has N·m because kg·m²/s² is N·m;
   bi speed and ki current are N·m. Stored energies have J, their rates W.
2. Electrical derivative remains185 A/s. Mechanical derivative becomes0 rad/s²;
   storage rate3.70 W. Input6 minus copper2, viscous.18 and load.12 is3.70 W.
3. With v=load=0, dE/dt=−Ri²−bω²≤0 under nonnegative R,b. Numerical
   integrators are not automatically constrained by this continuous inequality.
4. ω=k v/(Rb+k²). Required v=20*.05/.1=10 V, above the six-volt limit.
5. ω=(.1*6−2*.05)/.05=10 rad/s. Linear viscous friction does not represent
   stiction, thermal current limits or rigid-tooth failure.
6. Reflected inertia=.5/25=.02 kg·m². Output speed2; energy.5*.5*4=1 J.
   Motor-side equivalent energy.5*.02*100=1 J.
7. d(error)/dt=dr/dt−dy/dt. If target jumps while y is constant, dr/dt appears
   only in derivative-on-error. The reference deliberately differentiates y.
8. Integrals [0,0,.1,0,0]; commands [2,2,1.1,−1,−2]. At final step a negative
   increment would drive a below−2 request farther outward, so it is rejected.
9. True speed2.6 rad/s. Repeat noise can average down under assumptions; the
   common calibration offset remains.
10. At constant positive infeasible error, z grows linearly although output is
    fixed at its bound. On a lower target, that stored positive term can maintain
    positive voltage until enough negative error is integrated. See raw experiment.
11. No universal numeric answer: require exact command/input/raw record and a
    comparison of the chosen metric plus limitations. Failure to worsen is data.
12. For a translating damped mass, m dv/dt=F−cv−Fload and dx/dt=v. A force
    controller can retain the saturation/measurement logic. Current, inductance
    and back EMF require an actual actuator model; they cannot be renamed away.
