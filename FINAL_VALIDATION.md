# Final validation record

Validation checks repository structure and reference implementations; it cannot certify learner mastery, factual completeness of every external source, or physical truth.

## Commands

```sh
python3 tools/run_reference_tests.py
python3 -m unittest discover -s tools/tests -v
python3 tools/validate_completion.py
python3 tools/validate_expansion.py
python3 tools/validate.py
```

## Results recorded in this build

- unified reference groups: 12/12 passed;
- arrays released set: 20/20 problem test suites passed;
- infrastructure regression suite: 44/44 passed after updating the obsolete scaffold fixture to use an actually scaffolded topic;
- completion validator: 0 errors;
- expansion validator: 0 errors;
- structural validator: 0 errors, with explicit known source/license warnings retained;
- RISC-V assembler oracle is toolchain-dependent and cannot run without GNU RISC-V binutils;
- SystemVerilog simulation is toolchain-dependent and cannot run without Icarus Verilog or another compatible simulator in the environment.

Warnings are not silently converted to passes. The portable archive intentionally excludes copyrighted book source bytes and retains source/license uncertainty where not verified.
