# Hardware, electronics and digital logic

Permanent track; learner NOT STARTED. The [electrical quantities bridge](../foundations/physics/electrical-quantities/README.md) is prepared. The broader topic map is scaffolded; it does not claim a full electronics course or a measured circuit.

Start from a problem requiring physical state: a receiver must distinguish two voltage ranges despite variation. Descend through energy/charge flow and switching before treating a logical symbol as reliable. Return upward through [HDL](../hardware-description-languages/README.md) only after the abstraction limits are understood. Physical construction waits for verified supply, component and instrument limits.

| Sequence | Required scope | Observable assignment |
| --- | --- | --- |
| Quantities | charge, voltage, current, resistance, power, energy, Kirchhoff laws | Predict a low-voltage resistor circuit after verified equipment selection; compare port energy accounting |
| Dynamics | capacitance, inductance, RC, RL, RLC, oscillators | Predict a transient, identify time scale, measure versus model after calculus/ODE bridge |
| Devices | diodes, BJTs, MOSFETs, switching | Trace controlled conduction from verified curves; separate schematic intent from device limits |
| Signals | logic levels, noise, signal integrity, clocking, power delivery | Identify threshold/timing uncertainty; no universal logic voltage |
| Conversion | ADC, DAC, sensors, amplification | Model input range, quantization, sampling and clipping after ratios/waves prerequisites |
| Integration | digital electronics, memory technologies, buses, PCB fundamentals, microcontrollers, processors, interfaces | Trace one sensor-to-output operation and all power/signal boundaries |

See [digital logic](DIGITAL_LOGIC.md), [device prerequisite bridge](PREREQUISITE_BRIDGE.md), [general machines](../general-machine-systems/README.md) and [reverse engineering](../reverse-engineering-systems/README.md). Every future topic must include realistic code/model work, prediction, measurement and failure analysis where feasible; no results are prefilled.
