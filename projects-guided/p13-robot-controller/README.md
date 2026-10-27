# Build a sampled sensor–motor feedback loop

Start from conservation of energy and Newton's rotational law. Build a motor
plant, a delayed/noisy sensor and a voltage-bounded controller; then diagnose
integrator windup and calibration bias. All reference parameters/data are
synthetic, and the executable build requires only Python3.10+.

[PREREQUISITES.md](PREREQUISITES.md) connects units, electrical storage and
mechanics. [CHECKPOINTS.md](CHECKPOINTS.md) teaches the architecture in stages:
continuous plant → numerical step → sensed sample → controller memory → actuator
limit → next physical state. The complete [lesson](../../17-embedded-robotics/control-path/README.md)
contains derivations, hand calculations and an original tested reference. Build
your own version before opening the matching reference function. Practice has
separate [exercises](../../17-embedded-robotics/control-path/EXERCISES.md),
[hints](HINTS.md) and [solutions](../../17-embedded-robotics/control-path/SOLUTIONS.md).

The experiment asks a concrete question: why can an unreachable20rad/s command
make recovery to2rad/s slow even when both controllers clip to the same6V?
Controller integral memory differs. A second experiment adds a.5rad/s sensor
bias: measured tracking can improve while true motion remains offset.
[EXPERIMENTS.md](EXPERIMENTS.md) gives controlled variables and actual outputs;
[TESTS.md](TESTS.md) gives mathematical and analytic acceptance tests.

Deliver a unit-annotated block diagram; electrical/mechanical energy derivation;
your plant, sensor and controller; all test output; predictions and raw experimental
records; a failure explanation and a reconstruction from memory. The rubric is
25points for equations/units/boundary,25 for independent tests,20 for causal
experiment interpretation,15 for controller/sensor contracts and15 for
reconstruction/limitations. No passing score is possible with invented hardware
observations, an unexplained sign convention or an incorrect energy identity.

The reference build is complete at the simulation boundary. Firmware deployment,
robot kinematics, current protection and physical validation remain separate
work; see [LIMITS.md](LIMITS.md) and [PRODUCTION.md](PRODUCTION.md).
