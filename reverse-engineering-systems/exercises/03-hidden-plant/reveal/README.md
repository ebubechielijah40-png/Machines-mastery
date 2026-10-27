# Reveal after predictions

The supplied fixtures use these ideal coefficients; they are authored synthetic
numbers, not measurements or published experimental results.

| Case | a | b | c | Gain | Offset | Assigned physical interpretation |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| amber | 2 | .8 | 18 | 1000 | 25 | mass/spring/viscous damper; q in m,u in N |
| slate | .75 | .3 | 6.75 | 700 | −12 | mass/spring/viscous damper; q in m,u in N |
| glass | 2 | .8 | 18 | 1000 | 25 | ideal series RLC; q in C,u in V |
| copper | 1.25 | 1 | 5 | −400 | 10 | ideal series RLC; q in C,u in V |

For an electrical interpretation L=a,R=b,C=1/c; gain has units counts/C.
For a mechanical interpretation m=a,viscous coefficient=b,k=c; gain is counts/m.
The different interpretations are information supplied by this reveal. They
cannot be inferred from amber/glass's identical supported numeric observations.

The oracle evaluates the exact underdamped constant-drive formula plus optional
bounded pseudo-noise. It does not implement a circuit solver, detailed material,
actuator saturation, finite settling process or physical measurement apparatus.
Balance returns ideal settled coordinates directly. Inspect
[plant.py](plant.py) only after comparing your holdout predictions and limits.
