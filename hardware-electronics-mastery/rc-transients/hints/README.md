# RC exercise hints

1. Prefix factors are `k=10^3`, `μ=10^-6`, `m=10^-3`. Divide quantities with
   the same units before exponentiating.
2. Use `Δq=CΔv` and average current `Δq/Δt`. Averages do not reveal a waveform.
3. Start with the initial error `v_0-V_s`; do not use the zero-initial formula.
4. Set source voltage to zero, solve a decreasing exponential for its time.
5. Solve symbolically for a fraction before evaluating any particular fraction.
6. Solve `t=RC ln 2` for `R`. Under stated controls, delay is linear in `C`.
7. At equilibrium the capacitor current is zero. The meter current is still
   nonzero. With the ideal source set to zero, the two resistors are parallel.
8. Integrate charge delivery for source work and integrate `v dq` for stored energy.
9. Multiplication and division associate left-to-right. Compare dimensions
   and double both `C` and the observation time.
10. Subtract `V_s` from the update equation. Vary the integration method and
    halve the step while leaving the physical parameters unchanged.
11. A voltage trajectory determines the product. Use `I(0)=V_s/R` and
    `E=C V_s²/2` to find information the voltage trace lacks.
12. Use `h=τ/N`, so `Nh=τ`. Compare errors relative to the same exact endpoint.
13. Equate energy storage rate and negative heat outflow. Map `T` to `v`,
    `T_env` to `V_s`, and compare `H/G` with `RC`.
