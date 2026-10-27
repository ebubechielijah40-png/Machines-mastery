# RC exercise solutions and checks

These are original solutions to the local exercises. Read them after saving an
attempt. Numerical values are calculated model answers; they are not observations.

1. `R=4700 Ω`, `C=22×10^-6 F`, `t=0.015 s`.
   `τ=0.1034 s`, `t/τ≈0.145068`. The ratio is dimensionless and can be an
   exponential argument. `t` or `τ` with units cannot individually be that argument.
2. `Δv=(2×10^-6)/(10×10^-6)=0.2 V`.
   `I_average=2×10^-6/10^-3=0.002 A=2 mA`. Many different current waveforms
   have this integral, so instantaneous current is not identified.
3. `τ=2000×2×10^-6=0.004 s`.
   `v(t)=5-4 exp(-t/0.004)` volts. At `τ`, `v≈3.528482 V`.
   Initially `i=(5-1)/2000=2 mA`, positive into the output-node plate.
4. `v(t)=5 exp(-t/0.004)`. Setting `v=1` gives
   `t=0.004 ln 5≈0.00643775 s`. Initially `i=-5/2000=-2.5 mA` under
   the charging convention: charge leaves the output-node plate.
5. Times are `RC ln 2`, `RC ln 10`, no finite time (asymptotic), and
   unreachable, respectively. Domain analysis must precede numerical log evaluation.
6. `R=t/(C ln 2)≈28,853.90 Ω`. At fixed exact `R` and fraction,
   ±20% `C` makes delay lie in `[0.16,0.24] s`. This interval does not
   include resistor, threshold, loading or temperature uncertainties; those
   were excluded by the question rather than proved negligible.
7. Node balance is `C dv/dt=(4-v)/100000-v/100000`.
   Equilibrium is `2 V`. Coefficient of `v` gives `R_eff=50 kΩ`, so
   `τ=0.05 s`. From zero, `v(t)=2(1-exp(-t/0.05))`. The `3 V` target
   exceeds the endpoint and is unreachable. Using `4 V` as the capacitor's
   asymptote incorrectly discards continuous current through the meter.
8. Source work `CV_s²=550 μJ`; capacitor energy and resistor loss each
   `275 μJ`. Doubling `R` leaves all three limiting integrated energies
   unchanged in the stated ideal model, doubles the time scale, halves
   initial current and quarters initial resistor power divided by? Check:
   `P(0)=V_s²/R`, so it **halves**, not quarters. At an arbitrary fixed time,
   current and power also contain the changed exponential time constant;
   they are not simply halved over the entire trajectory.
9. `-t/R*C` is `-(t/R)C`, not `-t/(RC)`. Its dimensions are `s·F/Ω`
   rather than one. An RC scaling oracle is
   `v(t;R,C)=v(2t;R,2C)`; the wrong formula violates it. The dimensional
   check catches the defect before any simulation is trusted.
10. `e_(n+1)=(1-h/τ)e_n`; at `h/τ=2` its multiplier is `-1`, so it never
    damps an initial error. The ideal continuous multiplier is `exp(-h/τ)`,
    always positive and smaller than one. Control A: halve `h` at the same
    end time and observe the artifact change/disappear. Control B: use exact
    constant-input stepping or backward Euler without changing the circuit.
    If measuring a real circuit, also inspect source waveform and probe
    loading; numerical controls alone do not rule out omitted inductance or
    time-dependent drive in the physical circuit.
11. Both products equal `0.1 s`, so the exact voltage functions coincide.
    Initial current ratio A/B is ten (`3 mA` versus `0.3 mA`). Stored energy
    ratio is ten (`450 μJ` versus `45 μJ`). At the same time,
    `P_R=V_s² exp(-2t/τ)/R`, so power ratio is ten. Voltage alone identifies
    `τ`, not both parameters: multiplying `R` by `k>0` and dividing `C` by
    `k` leaves the waveform unchanged. Measure initial current to identify
    `R=V_s/I(0)`; then infer `C=τ/R`, with that measurement's uncertainty.
12. Forward Euler after `N` equal steps to `τ` gives
    `v_N=V_s[1-(1-1/N)^N]`; exact value is `V_s(1-exp(-1))`. This
    overestimates the rising voltage. Backward Euler gives
    `V_s[1-(1+1/N)^(-N)]`, an underestimate. Adjacent absolute-error ratios
    approach two as `N` doubles in the tested regime. Consult
    [executed evidence](../evidence/rc-experiment.json) for actual run values.
    The exponent `N` and ratio `h/τ` both matter: fixing ten steps while
    changing `h` changes the final time, so differences would mix numerical
    error with physically different endpoints.
13. Storage rate `H dT/dt=-G(T-T_env)`. Thus
    `dT/dt=-(T-T_env)/(H/G)` and `τ=H/G`, whose units are
    `(J/K)/(W/K)=J/W=s`. Solution:
    `T(t)=T_env+[T(0)-T_env]exp(-t/τ)`.
    Euler deviation multiplier is `1-h/τ`; asymptotic stability requires
    `0<h<2τ`. Assume uniform object temperature (internal equilibration
    sufficiently fast) and constant environmental temperature/conductance.
    Two sensors showing persistent internal temperature gradients would
    challenge the single-state lumped assumption. Radiative nonlinearities,
    changing airflow or temperature-dependent heat capacity may also require
    a richer model. Matching curve shape alone cannot prove the model.
