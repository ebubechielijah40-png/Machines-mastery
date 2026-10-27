# Carrier, load-line and timing interventions

**Questions.** How does compensation change a uniform equilibrium carrier model?
How does a transistor's current law become a circuit output? Does a slower clock
repair a hold violation?

**Predictions.** Net dopant imbalance determines the ideal majority/minority
solution; a series resistor prevents an exact zero low output and dissipates
static power; Euler delay estimates converge as step is reduced; setup and hold
respond differently to signed skew and period.

**Controls/procedure.** Keep ni=10^16 m^-3 and assumed mobilities.1/.05 m²/(V·s)
fixed while varying donor/acceptor concentrations. Sweep Vin from0 to5 V in.1 V
increments with VDD=5 V,R=10 kΩ,β=.001 A/V²,VT=1 V. Add C=10 pF and integrate
one gate-input transition for300 ns with steps.2,.1,.05 ns. Retain interpolated
half-supply crossing times, sampled trajectory and complete accumulated energy
terms. Independently vary only capture skew or only period in the timing model.
Run experiment.py; the raw JSON records environment, code hashes, assumptions and
actual synthetic observations. No physical electronics was operated.

**Actual observations.** [observed.json](evidence/observed.json) retains the run.
At Vin=5 V, modeled DC Vout=.1238209296 V, supply current=.487617907 mA and power
=2.438089535 mW. Those are computed circuit values, not measured component ratings.

| Euler step | Rising half-supply crossing | Falling half-supply crossing |
| --- | --- | --- |
|.2 ns |66.740333 ns |3.258891 ns |
|.1 ns |66.773721 ns |3.267503 ns |
|.05 ns |66.790419 ns |3.272012 ns |

The two transitions use different current paths. Smaller step changes the values;
the finite table does not prove the continuous-time solution exactly. The energy
balance residual matches the independently derived Euler quadratic term. A1 µs
step is explicitly rejected for leaving the rails; no trajectory clipping masks
that failure.

For the stated clock/path example, zero skew yields setup slack3 ns and hold
slack.1 ns. Adding.2 ns positive capture skew gives3.2 ns setup slack and-.1 ns
hold slack. Changing the period from10 to100 ns leaves hold slack at-.1 ns.
This is a counterexample to the proposed universal “slow the clock” repair.

**Interpretation/alternatives.** The laws and observation equations explain these
interventions within their assumed regimes. Physical carrier populations,
mobilities, thermal effects, body bias, loads, interconnect and clock uncertainties
can invalidate them. An ideal zero-cutoff current is not evidence of no real
leakage. An abstract timing inequality is not a metastability measurement.

**Follow-ups.** Double C and compare crossing times at equal normalized step;
change R and compare static-power/speed tradeoffs; replace fixed mobility with a
separately sourced model; sweep path minimum delays while checking both timing
slacks; design a future calibrated waveform protocol with explicit probe loading,
threshold definition and device conditions. Treat a requested physical protocol
as prepared until actual apparatus/evidence exists.
