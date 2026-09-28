# Electronics and digital hardware — deep self-contained guide

## 1. Voltage, current, resistance, power

Voltage is an electric potential difference between two points; current is charge flow; resistance relates voltage/current in regimes where Ohm's-law modeling is appropriate; power is energy transfer per unit time. `P=VI` is an accounting relationship, not a complete device model.

### Experiment model
Use a safe low-voltage source and known resistor only when you have appropriate equipment. Predict current from nominal resistance and voltage, then measure. Compare tolerance, meter burden, source resistance, and heating. If equipment is unavailable, use the local simulation exercises and mark the physical result unobserved.

## 2. Kirchhoff reasoning

At a circuit node, charge conservation motivates current balance. Around an ideal lumped loop, potential changes sum to zero. These laws are modeling rules for lumped circuits; high-frequency distributed effects require richer models.

## 3. Capacitance and time

A capacitor stores energy in an electric field. In an RC charge model, voltage approaches its final value exponentially with time constant `τ=RC`. This creates delays, filters, reset timing, debouncing behavior, and analog front ends.

## 4. Inductance and magnetism

An inductor relates changing current to voltage and stores magnetic-field energy. Motors, transformers, switching converters, relays, and signal integrity all depend on inductive effects. Switching inductive loads requires paths for stored energy; ignoring this can produce damaging voltage spikes.

## 5. Diodes and transistors

A diode conducts asymmetrically under an approximate operating model. A MOSFET can act as a voltage-controlled switch within device limits. Digital logic abstracts continuous voltages into regions interpreted as logical 0/1, but the transistor/circuit remains analog underneath.

## 6. From transistor to gate

CMOS logic uses complementary transistor networks so stable logical states draw relatively little static current in idealized conditions, while switching consumes dynamic energy. Gate delay, input capacitance, fan-out, threshold variation, and noise margins make “instant perfect Boolean logic” an abstraction.

## 7. Combinational vs sequential logic

Combinational output is modeled as a function of current inputs. Sequential circuits contain state. Latches/flip-flops capture values under timing conditions; registers group bits; finite-state machines combine state with transition/output logic.

Setup/hold requirements mean data must be stable around the sampling event. Violating them can cause metastability, a physical phenomenon not represented by ordinary Boolean simulation.

## 8. Clocking

A clock coordinates state updates but creates distribution, skew, jitter, power, and timing problems. Maximum frequency is limited by path delays plus setup/skew margins. Faster clock is not automatically faster system if memory/I/O/parallelism dominate.

## 9. Memory

Memory technologies encode state physically in different ways: SRAM-like cells use bistable circuits, DRAM stores charge that must be refreshed, nonvolatile memories use mechanisms that retain information without power. Each has density, latency, endurance, power, and manufacturing tradeoffs.

## 10. ADC/DAC and sensors

Physical sensors produce analog quantities. ADC converts a bounded analog input into discrete codes under sampling/quantization assumptions. Resolution is not the same as accuracy. Noise, offset, gain error, nonlinearity, bandwidth, aliasing, calibration, and reference stability matter.

## 11. Power delivery and heat

Every electronic system must deliver current within voltage tolerance and remove heat. Voltage drop, regulator efficiency, transient response, decoupling, grounding, PCB layout, airflow, and thermal interfaces can determine reliability even when logical design is correct.

## 12. Hardware description languages

HDL describes structure/behavior of hardware. A synthesizable `always_ff`/clocked process is not a software loop; it specifies state updated on clock events. Simulation semantics and synthesis constraints must both be understood.

## 13. Build path

```text
resistor/transistor models
→ inverter
→ logic gates
→ mux/decoder/adder
→ latch/flip-flop
→ register/counter/FSM
→ ALU
→ datapath
→ control
→ memory interface
→ CPU
→ assembler/program
```

At each step test truth tables/state transitions, timing assumptions, invalid states, and integration interfaces.

## 14. Limits

A schematic/RTL simulation does not establish physical reliability. Real hardware adds parasitics, timing, process variation, signal integrity, EMC, thermal limits, power integrity, manufacturing defects, and component tolerances. Never infer safe voltage/current limits without actual datasheets and equipment-specific constraints.
