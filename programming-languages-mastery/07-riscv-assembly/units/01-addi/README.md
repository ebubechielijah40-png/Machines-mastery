# Assembly exemplar: one instruction from text to state

PREPARED; learner NOT STARTED. Study [bridge](PREREQUISITE_BRIDGE.md) → [lesson](LESSON.md) → [problems](problems/README.md) → hints/retry → implementation → [experiment](EXPERIMENT.md) → [mastery](MASTERY.md). The reference stays in solutions. No external reading required.

Scope: RV32I ADDI only, fixed 32-bit instruction encoding and architectural arithmetic. The Python interpreter is a restricted teaching model, not a complete CPU/emulator. There is no Linux syscall, ABI, pipeline or physical timing claim.

Python 3.10+ and GNU RISC-V binutils are required for full validation. From repository root:

```sh
python3 programming-languages-mastery/07-riscv-assembly/units/01-addi/tests/run.py
```

The runner uses installed `riscv64-linux-gnu-as/objcopy`, or the audited temporary tools under `/tmp/machines-tools/usr/bin`. If neither exists it fails explicitly, rather than claiming assembler validation. No installation is needed for the explanatory paper path. The GNU assembler is configured `-march=rv32i -mabi=ilp32`; its executable name does not select RV64 in this command. Temporary objects are deleted by the test harness. Python uses four-space indentation; tests use unittest.
