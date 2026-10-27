# From a simulation to an embedded controller

A device loop must timestamp each sensor sample, reject stale/invalid readings,
use a documented unit conversion, and bound both voltage and current. A watchdog
needs an independently specified safe actuator state; continuing the last high
command after a software crash is a design decision with physical consequences.
Command limits in the controller must match what the driver actually applies,
or the anti-windup model tracks the wrong actuator input.

Separate the fast control task from blocking logging or communication. Measure
worst-case execution/jitter on the actual target; a Python average runtime is not
a deadline guarantee. Log setpoint, measurement timestamp, command before/after
limiting, integrator and fault code so an incident can be reconstructed. Store
calibration version and units beside measurements, not just raw encoder counts.

A bounded local simulation is the deployable artifact here. Hardware deployment
requires a motor/driver datasheet, current-limited supply, guarded mechanism,
independent emergency stop, sensor calibration and incremental low-energy tests.
These are concrete engineering dependencies, not actions performed by this build.
A useful simulation extension first adds actuator-current limiting and sensor
staleness faults, then tests a defined recovery state before any hardware port.
