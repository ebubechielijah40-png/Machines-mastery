# Checkable reference reasoning

1. A hole represents missing occupancy in a band. A donor leaves fixed positive
charge when an electron becomes mobile; charge counting includes both.
2.10^16 cm^-3=10^22 m^-3;1000 cm²/(V·s)=.1 m²/(V·s).
3–4. Substitute p=n-Δ into np=ni² to obtain n²-Δn-ni²=0. For Δ<0 the direct
positive root cancels. Use M=(|Δ|+sqrt(Δ²+4ni²))/2 and minority ni²/M, computing
products/ratios in a stable order and rejecting unrepresentable results.
5. n≈10^20 m^-3 and p≈10^12 m^-3; np≈10^32 m^-6. The approximation n=ND is not
the exact simultaneous solution, so a tiny neutrality residual is expected.
6. ND=NA=10^22 m^-3 gives n=p=ni in the model. Impurity scattering can still
change mobilities and invalidate the “same conductivity” conclusion.
7. v_n=-μ_nE, charge=-q, so J_n=(-q)n(-μ_nE)>0 along a positive field. Holes
also contribute along the field. qnμ has units C·m^-3·m²/(V·s)=S/m.
8–9. Integrating β(VGS-VT-V)dV yields β[(VGS-VT)VDS-VDS²/2]. Nonnegative
channel charge requires VDS≤VGS-VT. For the stated inputs, cutoff gives0,
VDS=1 gives1.5 mA and VDS≥2 gives2 mA in the ideal saturation model.
10. Saturation approximates drain-current independence from drain voltage at
fixed overdrive. It does not set VDS=0 or eliminate dissipated power I_D VDS.
11. At Vout=0, resistor current is positive and device current is0; at Vout=VDD,
resistor current is0 and device current is nonnegative. Resistor current strictly
decreases while the modeled device current is nondecreasing, giving one root.
For Vin=5 the root is the smaller positive root of .0005V²-.0041V+.0005=0,
namely.1238209296 V. Use the rationalized quadratic to avoid cancellation.
12–13. Multiply KCL by Vout and replace VDD-Vout by I_R R. Then expand the Euler
capacitor change: ΔE_C=C VΔV+C(ΔV)²/2. Old-state power accounts for only C VΔV,
so supply minus both heats minus ΔE_C equals -C(ΔV)²/2 per step.
14. In C dV/dt=f(V), doubling C doubles the time for the same trajectory in this
fixed circuit model. A proportionally controlled time step compares like numerical
accuracy. Supply/interconnect/driver changes would be additional interventions.
15. NAND pull-down is a AND b; pull-up is NOT a OR NOT b. NOR uses a OR b and
NOT a AND NOT b. Two parallel n devices paired with two parallel p devices would
connect both rails for input01, a wrong complementary construction.
16. The cell emits the parity of a+b+carry and forwards whether that sum≥2.
Inductively, the low w bits plus2^w times the forwarded carry equal the input sum.
The test exhausts unsigned-byte pairs through independently computed integer sums.
17. Minimum delay bounds the earliest disturbance, maximum bounds latest settling;
setup/hold surround capture; clock-to-Q bounds launch-state output change.
18. Latest new arrival≤T+s-u-t_setup; earliest disturbance≥s+u+t_hold. Rearrange
to obtain the displayed slacks. Positive skew helps the first and hurts the second.
19. With s=.2 ns, hold is short by.1 ns regardless of period. Adding.15 ns to
minimum path delay repairs that bound by.05 ns; if it also adds.15 ns to maximum
path delay, setup slack drops by.15 ns and must remain nonnegative at every corner.
20. An external pin can change arbitrarily close to a sampling edge. Functional
simulation assigns a scheduled0/1 without resolving physical gain/noise/time
constants. No failure-rate estimate follows from seeing only valid sampled bits.
21. Different bit synchronizers can settle in different cycles, creating a word
that never existed at the source. A handshake that holds data until an acknowledged
transfer, or a correctly designed asynchronous FIFO, supplies a coherent protocol.
Neither is supplied merely by our single-clock queue test.
22. A complete attempt derives all three mechanisms, records units/assumptions,
checks at least one independent arithmetic path, retains a failure and explains
which physical claims remain unperformed. The source/experiment files provide
reference checks, never automatic learner mastery.
