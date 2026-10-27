# From a material to a controlled electrical path

Start with [quantities/current/voltage](../foundations/physics/electrical-quantities/README.md),
[atomic structure and bonding](../foundations/chemistry-materials/elastic-evidence/README.md),
[algebra](../foundations/mathematics/core/01_ALGEBRA_FUNCTIONS.md) and
[derivatives/integrals](../foundations/mathematics/core/04_CALCULUS_OPTIMIZATION.md).
The worked implementation is [devices.py](device-logic/devices.py); its selected
primary scopes are recorded in [SOURCES](device-logic/SOURCES.md). Every device
parameter below is assumed for a model, not taken from a real part's datasheet.

## Allowed states, occupied states and mobile charge

A bonded solid has many interacting electronic states. Some energies are allowed;
a band gap is an interval with no corresponding bulk states in the band model.
The availability and occupation of states both matter to transport. A partially
filled band or overlapping bands can allow metallic conduction; a statement that
all conductors merely have a small positive gap is too crude. A band diagram is
not a complete conductivity calculation: temperature, scattering and structure
also enter. The earlier two-particle mechanical energy well does not derive this
many-electron electronic structure.

In a semiconductor model, n counts mobile electrons per m³ and p counts mobile
holes per m³. A hole describes an unoccupied electronic state whose motion is
conveniently represented as positive mobile charge; it is not a proton traveling
through the crystal. A donor can leave a fixed positive ion and a mobile electron;
an acceptor can leave a fixed negative ion and a mobile hole. Bulk electrical
neutrality can therefore coexist with very different mobile-carrier populations.

Assume thermal equilibrium, a nondegenerate carrier model and completely ionized
uniform donors ND and acceptors NA. At a fixed temperature, let ni be an assumed
intrinsic concentration. The equations are

\[
 np=n_i^2,\qquad n-p=N_D-N_A=\Delta.
\]

The first is the equilibrium mass-action relation; it is not automatically true
under optical injection, applied nonequilibrium bias or high degeneracy. The
second counts fixed as well as mobile charge. Substituting p=n-Δ gives
n²-Δn-ni²=0. The positive solution is

\[
 n=(\Delta+\sqrt{\Delta^2+4n_i^2})/2,\qquad p=n_i^2/n.
\]

For a large negative Δ, this formula subtracts nearly equal floating numbers.
Instead compute the majority concentration as
M=|Δ|/2+hypot(Δ,2ni)/2, compute the minority as ni(ni/M), and assign M to the
appropriate carrier. This preserves a small positive minority where direct
subtraction would erase it. Extreme unrepresentable minorities are rejected.
Near intrinsic conditions, subtracting the two large returned concentrations to
recover a tiny Δ has unavoidable floating resolution; tests bound that residual
in units of the represented concentrations rather than demanding impossible
relative accuracy in their tiny difference.

With ni=10^16 m^-3 and ND=10^22 m^-3, NA=0, n is almost10^22 m^-3 while p is
about10^10 m^-3. If both dopant densities are10^22 m^-3, their net contribution
cancels in this ideal model and n=p=ni. This compensated case refutes the shortcut
“more total dopant always means more majority carriers.” Real mobility can still
change with impurity scattering, which the fixed-mobility example omits.

## Derive current from charge crossing an area

Under a weak uniform field E_field in V/m, define electron drift velocity
v_n=-μ_n E_field and hole drift velocity v_p=μ_p E_field. In one second a cross
section of area A is crossed by approximately nA|v_n| electrons. Multiplying
charge per carrier by signed flux gives conventional electron current density
J_n=(-q)n v_n=q n μ_n E_field; holes similarly give J_p=q p μ_p E_field.
Thus

\[
 J=\sigma E_{\rm field},\quad \sigma=q(n\mu_n+p\mu_p),\quad
 R=L/(\sigma A).
\]

Mobility units are m²/(V·s), so σ has units C/(V·s·m)=S/m. Be careful with
centimeter-based source conventions:1 cm^-3=10^6 m^-3 and1 cm²/(V·s)=10^-4 m²/(V·s).
Random thermal motion alone is not net drift. Strong fields, spatial gradients,
interfaces and temperature-dependent scattering require more than this ohmic
bulk expression. A p-n junction needs a spatial charge/field/diffusion model;
these uniform equations do not produce its full behavior.

## Gate control and a long-channel current law

A MOSFET has gate, source, drain and body terminals. The gate insulator allows a
gate-to-body electric field to change charge near the surface. Under the declared
strong-inversion conditions an electron channel can connect source and drain.
Gate current is omitted from the static idealization; changing the gate voltage
still charges capacitances and transfers energy. A device is not an energy-free
Boolean switch.

For an n-channel model with body tied to source, define local channel potential
V(x), source at0 and drain at VDS≥0. Write the assumed sheet charge magnitude as
Cox(VGS-VT-V(x)), and use a low-field mobility μ. Current continuity gives

\[
 I_D=\mu C_{ox}W(V_{GS}-V_T-V)\frac{dV}{dx}.
\]

Integrate x from0 to L and V from0 to VDS. With β=μCoxW/L,

\[
 I_D=\beta[(V_{GS}-V_T)V_{DS}-V_{DS}^2/2]
 \quad(0\le V_{DS}\le V_{GS}-V_T).
\]

The charge expression must remain nonnegative along the channel. At the drain it
reaches zero when VDS=VGS-VT. Extending the parabola beyond that boundary would
predict decreasing or negative current for an invalid charge model. The ideal
saturation approximation instead holds I_D=β(VGS-VT)²/2. For VGS≤VT our simplified
cutoff law sets I_D=0. Real subthreshold leakage, channel-length modulation,
velocity saturation, body effect and temperature dependence are omitted.

For β=.001 A/V², VT=1 V and VGS=3 V: I_D=1.5 mA at VDS=1 V; at VDS=2 V the
branches meet at2 mA. In this model VDS=5 V still gives2 mA. “Saturation” here does
not mean a zero-resistance closed switch; it describes the current-law region.
The implementation tests branch continuity, derivative β(VGS-VT-VDS), cutoff,
nonnegative current and boundary rejection.

## A circuit chooses the operating point

Connect a resistor R from VDD to the drain, the source to ground, and drive the
gate with Vin. At DC, Kirchhoff's current law requires

\[
 (V_{DD}-V_{out})/R=I_D(V_{in},V_{out}).
\]

The left side decreases with Vout; the modeled drain current is nondecreasing.
The difference brackets a unique root between the rails, including the cutoff
endpoint. Bisection retains this bracket without guessing a derivative near a
region change. A numerical solver is only solving the declared circuit/model.

For VDD=5 V,R=10 kΩ,β=.001 A/V²,VT=1 V: Vin=0 gives Vout=5 V. For Vin=5, Vout is
about.124 V, with a nonzero static supply current. The low output is determined
by a resistor/device balance; assigning it exactly zero would hide both the
voltage error and power consumption. The test also solves its triode quadratic
by a separate formula. If the output drives another stage, its input ranges,
load and fanout must be checked rather than assuming any positive voltage is1.

Add a load capacitor C. Charge conservation gives

\[
 C\frac{dV_{out}}{dt}=(V_{DD}-V_{out})/R-I_D.
\]

Euler stepping makes an explicit approximation. With Vin=0, the MOSFET is off,
so the exact limit is Vout=VDD+(V0-VDD)e^(-t/RC). The tests verify convergence
against this independent closed form. An oversized step can leave the rails;
our code reports that failure rather than clipping a bad numerical trajectory.

Power accounting supplies another oracle. With I_R=(VDD-Vout)/R,
VDD·I_R=I_R²R+Vout·I_D+C Vout dVout/dt. Summing old-state power in Euler while
using the exact quadratic capacitor energy creates a known residual
-Σ C(ΔV)²/2. The experiment retains it. A small step shrinks that numerical
residual; deleting it would falsely suggest exact energy conservation.

## Complementary gates and the next abstraction

A complementary ideal-switch inverter uses a p-channel pull-up controlled by
VSG and an n-channel pull-down controlled by VGS. At stable rail inputs, one
network is off in the ideal static model. Real leakage and transition current
are not zero merely because that ideal model omits them.

For a two-input NAND, the n pull-down devices are in series: both inputs must
be1 to conduct. Its complementary p pull-up devices are in parallel: at least
one input0 creates a pull-up path. For NOR, exchange series/parallel roles. The
truth table follows from connectivity, not from naming the gate:

| A | B | NAND | NOR |
| --- | --- | --- | --- |
|0 |0 |1 |1 |
|0 |1 |1 |0 |
|1 |0 |1 |0 |
|1 |1 |0 |0 |

The model rejects networks that simultaneously connect both rails or neither.
A full adder then derives sum=a XOR b XOR carry and carry_out=ab+a·carry+b·carry.
A ripple chain passes that carry into the next bit. The executable cell model
matches integer addition for all65,536 pairs of unsigned bytes. That checks its
finite function; it does not measure transistor delay or prove an analog noise
margin. Continue with [timing and state](04_DIGITAL_TIMING.md).

Run the [controlled experiment](device-logic/EXPERIMENTS.md), then attempt
[practice](device-logic/EXERCISES.md) before [hints](device-logic/HINTS.md) and
[solutions](device-logic/SOLUTIONS.md). Reconstruct the carrier solver, channel
integral, load-line root and one gate network without copying reference code.
