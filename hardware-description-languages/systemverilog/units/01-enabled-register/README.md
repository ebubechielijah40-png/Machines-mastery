# SystemVerilog exemplar: a clocked register with priority

PREPARED; learner NOT STARTED. Begin [bridge](PREREQUISITE_BRIDGE.md) → [lesson](LESSON.md) → [problems](problems/README.md) → hints/retry → write RTL/testbench → [experiment](EXPERIMENT.md) → [mastery](MASTERY.md). Source and finished RTL remain optional verification/reference after an attempt.

Python 3.10+, Icarus Verilog 12 or compatible `iverilog`/`vvp` are required for executable checks. From repository root:

```sh
python3 hardware-description-languages/systemverilog/units/01-enabled-register/tests/run.py
```

The runner uses installed tools or the temporary `/tmp/machines-tools` extraction, creates temporary simulator files, exhaustively checks transitions, and requires a reset-priority mutant to fail. Missing tools cause an explicit error. No synthesis, timing closure, FPGA programming or physical measurement is claimed. SystemVerilog uses four-space indentation and an explicit `timescale`; the testbench samples after nonblocking updates settle.
