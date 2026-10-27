# Inspected sources and claim scope — 2026-10-22

Original lesson, code, hypothetical parameters, proofs and numerical experiments
are independently written. No source chapters, figures or implementation are
bundled or relicensed. Public readability does not grant redistribution rights.

| ID | Inspected primary/authoritative source | Exact scope | Limits |
| --- | --- | --- | --- |
| C-MOTOR | [CTM DC Motor Speed Modeling, university-hosted original tutorial](https://www.ece.ualberta.ca/~tchen/ctm/examples/motor/motor.html), dated1997 on page | Physical setup/model assumptions, current–torque/back-EMF relations; state-space matrices in printed MATLAB listing | Historical tutorial, not a new hardware datasheet. Its listed inertia unit includes an erroneous /s²; the local lesson derives kg·m² dimensionally. Its motor parameters/claimed measurements are not our data |
| C-PID | MathWorks, R2026b, [Anti-Windup Control Using PID Controller Block](https://www.mathworks.com/help/simulink/slref/anti-windup-control-using-a-pid-controller.html) | “Performance Without Using Anti-Windup,” “Integrator Clamping,” and stated conditions for built-in schemes | Supports saturation/windup/conditional-integration context; our code and parameter experiment are original, not a Simulink reproduction |
| C-ROT | Peter Dourmashkin/MIT8.01SC, textbook updated2022, [Chapter17 PDF](https://ocw.mit.edu/courses/8-01sc-classical-mechanics-fall-2016/mit8_01scs22_chapter17.pdf) | §17.3 torque; §17.4 fixed-axis dynamics; §17.5 work/energy/power, printed17-9 onward and17-25–27 | Fixed-axis/rigid-body assumptions; no proof that the hypothetical plant describes real hardware |
| C-WORK | Same course, [Chapter13 PDF](https://ocw.mit.edu/courses/8-01sc-classical-mechanics-fall-2016/mit8_01scs22_chapter13.pdf) | §13.4, equations13.4.1–13.4.5, work units and sign | Original examples here differ; no source experiment reproduced |

The current Michigan CTMS page returned403; Caltech's FBS PDF timed out and the
wiki returned502. No unseen source contents support this unit. Named books in
those pages' bibliographies were not thereby inspected. The local gear-reflection,
controller state transition, numerical RK4 step and sensor examples are derived
from the explicitly declared model, rather than attributed as new source results.
