# Establish the quantities before controlling them

Read [counting and units](../../foundations/mathematics/counting-and-units/README.md),
[change/error/evidence](../../foundations/mathematics/change-error-and-evidence/README.md),
[electrical quantities](../../foundations/physics/electrical-quantities/README.md),
[RC transients](../../hardware-electronics-mastery/02_RC_TRANSIENTS.md) and
[motion/energy](../../foundations/physics/MOTION_ENERGY.md), in that order.
The model uses a derivative as instantaneous change, an integral as accumulated
error, and vectors as lists of current/speed/angle. No matrix-control theory or
hardware purchase is required.

Entry checks: 6V times2A is12W; a.2m perpendicular lever under10N produces2N·m;
a.5kg·m² rotor under2N·m accelerates at4rad/s². Inductor storage is Li²/2 and
rotational storage is Jω²/2. A zero-speed motor can draw current and heat while
performing zero shaft work. Correct these before tuning gains.

Use Python3.10+ standard library. Reproducible commands and recorded environment
are local. [SOURCES.md](../../17-embedded-robotics/control-path/SOURCES.md) records
exact inspected CTM/MIT/MathWorks sections and unavailable-source attempts.
