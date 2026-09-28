# Install / run locally

After extracting the repository:

```sh
cd machines-mastery
python3 tools/run_reference_tests.py
python3 -m unittest discover -s tools/tests -q
python3 tools/validate_completion.py
python3 tools/validate_expansion.py
python3 tools/validate.py
```

The core prepared materials require only Python 3 for the included reference labs. Some optional language/hardware exercises require their own toolchains (for example a C compiler, RISC-V binutils, or an HDL simulator). Missing optional toolchains should be recorded as blockers rather than treated as evidence that the lesson is wrong.

Start learning at `START_HERE.md`.
