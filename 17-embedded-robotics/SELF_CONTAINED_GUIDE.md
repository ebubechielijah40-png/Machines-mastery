# Embedded robotics: quantities to a closed feedback loop

Begin with the [connected coursebook](../coursebooks/08-embedded-robotics.md).
Read units → electrical quantities → RC dynamics → motion/energy →
[the motor/control unit](control-path/README.md) in its stated prerequisite order.
Each step adds a required mechanism; full robot planning/kinematics and hardware
firmware remain outside this bounded path.

A controller commands voltage, not speed. Inductance stores Li²/2 and a rotating
inertia stores Jω²/2. Electrical back EMF and mechanical torque are opposite sides
of the same energy conversion. The derived model is L di/dt=v−Ri−kω,
J dω/dt=ki−bω−load, dθ/dt=ω. Multiplication by i andω cancels conversion power and
gives dE/dt=vi−Ri²−bω²−load·ω. Check that identity before tuning any loop.

For the hypothetical reference plant under6V, no-load steady speed is12rad/s.
Demanding20rad/s creates sustained saturation. A clipped controller can continue
accumulating integral state even while output stays at6V; this state delays
recovery after the target falls. Conditional integration blocks increments that
push farther into saturation and permits unwinding. Derivative on measurement
avoids a derivative kick from target steps but needs filtering against noise.

A sensor reports a biased/noisy/quantized history of speed. With y=ω+c, near-zero
measured error implies true speed r−c; feedback cannot identify its own unknown
calibration offset. A hundred delayed samples at.002s means.2s latency. The sample
pipeline has an explicit first-sample prehistory rather than invented old data.

Build the plant, RK4 step, sensor, controller and failure experiments through
[the guided project](../projects-guided/p13-robot-controller/README.md). The unit
contains original worked cases, independent hand/energy/analytic tests, separate
exercises/hints/solutions, inspected-source records and actual synthetic JSON.

```sh
python3 -m unittest discover -s 17-embedded-robotics/control-path -p 'test_*.py' -v
python3 17-embedded-robotics/control-path/experiment.py
```

The executed windup experiment supports a bounded claim for the recorded gains,
plant, horizon and metric. A delay case improved one metric; do not turn a single
trajectory into a universal rule. All outputs are simulations; no physical
robot, driver, sensor, real-time deadline, collision model or safety system was
validated. Reconstruct equations and update order without notes, then add a
load/current limit and explain which prior assumptions must change.
