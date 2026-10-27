# Identify a concealed dynamic port

Investigate four supplied software oracles named amber, slate, glass and copper.
They emulate detector readings of a physical-style dynamic system. No hardware
is connected. The names reveal no topology; the source is concealed only by a
study convention. Do not open `reveal/` or the reference reconstruction until
you have written hypotheses, a measurement plan and holdout predictions.

Each query resets the target. A response contains numeric readings in detector
counts and, for release, a sampling interval in seconds. A coordinate reference
has unit Q and an applied drive has unit U; do not silently treat counts as Q
or infer mechanical versus electrical units from the shape of a trace.

| Mode | Intervention | Observations |
| --- | --- | --- |
| calibrate | 2–32 known coordinates, each in[-1,1] Q | detector readings at those references |
| balance | 2–32 constant drives, each in[-10,10] U | settled detector readings; no finite settling process is simulated |
| release | coordinate q0 in[-1,1] Q, velocity v0 in[-10,10] Q/s, constant drive in[-10,10] U | 2–4096 uniformly sampled readings, h in[1e-5,1]s and total horizon≤60s |

The added `noise_bound` is in detector counts, from0 to1. For a fixed uint32
seed the software adds reproducible bounded pseudo-noise. That distribution is
a chosen test instrument model, not a measured physical detector law.

```sh
python3 reverse-engineering-systems/exercises/03-hidden-plant/oracle.py --case amber --mode calibrate --values -.02 .02
python3 reverse-engineering-systems/exercises/03-hidden-plant/oracle.py --case amber --mode balance --values -.3 .6
python3 reverse-engineering-systems/exercises/03-hidden-plant/oracle.py --case amber --dt .05 --samples 201
```

Your deliverable is an original executable predictor, calibrated units, a
bounded domain of validity, a notebook of distinguishing experiments, a table
of surviving model classes, and successful predictions for a changed initial
state and constant drive. Choose those holdout conditions before fitting.
Reproducing one observed decay trace is insufficient. Prove at least one thing
that the available observations cannot identify.

Observable exit criteria: calibrate both signs of detector gain; reconstruct
the restricted free-response dynamics; predict the clean101-sample holdout at
h=.037s,q0=-.013Q,v0=.027Q/s,u=.31U within1e-9Q; explain the residual under
noise; exhibit scale and topology ambiguity and an alias pair. The numerical
tolerance is a deterministic software contract, not a measurement uncertainty.

Begin with [the prerequisite and derivation bridge](README.md). Hints, solutions
and reveal are separate so predictions can be recorded before answers are read.
