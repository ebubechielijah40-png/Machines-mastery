# VHDL clocked queue

The [shared queue unit](../../../../hardware-description-languages/fifo-contract/README.md)
contains the language-specific syntax/semantics bridge, original VHDL source,
actual GHDL testbench/negative controls and progressive practice. Code is shared
intentionally with the HDL hardware track. Read signal versus variable scheduling
before modifying occupancy logic; reconstruct the state transition first.

```sh
python3 hardware-description-languages/fifo-contract/run.py --language vhdl
```

Run from the repository root with ghdl on PATH. This bounded implementation does
not make the rest of the generic VHDL topic pages complete.
