# Carrier, device, circuit and timing workbench

Study in this order:

1. [Semiconductors and controlled conduction](../03_SEMICONDUCTORS_TRANSISTORS.md):
   equilibrium carrier counting, drift units, channel integral, load-line root,
   charge/energy dynamics and complementary gates.
2. [Digital timing](../04_DIGITAL_TIMING.md): value ranges, min/max delay,
   register sampling, signed skew, separate setup/hold and metastability limits.
3. [Actual synthetic experiments](EXPERIMENTS.md), then [exercises](EXERCISES.md),
   [hints](HINTS.md) and [solutions](SOLUTIONS.md).

```sh
python3 -m unittest discover -s hardware-electronics-mastery/device-logic -v
python3 hardware-electronics-mastery/device-logic/experiment.py
```

No external Python library or hardware is needed. The assumed low-field,
long-channel and single-clock models have explicit scopes. Sources are mapped
in [SOURCES](SOURCES.md). The finite Boolean ripple model is tested exhaustively
for bytes; it does not supply a physical transistor/FPGA implementation.
