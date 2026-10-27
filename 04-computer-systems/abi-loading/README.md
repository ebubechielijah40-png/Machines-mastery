# Native calling boundaries and a bounded ELF loading model

This is a preserved, executable mechanism checkpoint. The broader systems
domain remains PARTIAL. The original full instructional chapter, source map,
separated assessment and full ABI/runtime breadth were not recovered before
this delivery; passing these programs does not complete that instruction.

Enter after [compilation/linking](../compile-link/README.md), the
[C byte parser](../../programming-languages-mastery/01-c/units/01-byte-parser/README.md)
and [memory/translation foundations](../../05-operating-systems/SELF_CONTAINED_GUIDE.md).
The scripts use only supplied source files and temporary build products. They
do not execute arbitrary ELF inputs or run a guest virtual machine.

`code/boundary.S` and `code/main.c` expose a selected Linux x86-64 integer call
boundary. The native runner checks eight-argument register/stack calls, an
entry-alignment observation, deliberate callee-save corruption, raw versus libc
error returns, structure layout and an8192-byte zero-initialized object. It
builds O0EXEC,O2EXEC and O2PIE with warnings as errors, retains exact compiler
and tool outputs, and compares program-header fields with GNU readelf.

`elf_plan.py` parses a restricted ELF64 input and constructs a load plan from
PT_LOAD segments, file ranges, memory ranges, permissions, alignment and a
declared load bias. Materialization copies each file-backed prefix and fills
the remaining modeled memory with zero bytes. A source section table describes
link/debug organization; this runner also removes that table from its own test
binary and actually runs the modified supplied binary. The result supports
that selected program-header boundary, not a complete dynamic-linker model.

`memory_models.py` contains deterministic cache and nested-translation models.
Its cache observations are modeled hit/miss counts, not hardware-counter or
timing measurements. A nested mapping's permission intersection does not prove
hypervisor isolation. No KVM guest is executed; path presence is not evidence
that a virtual-machine operation is available or authorized.

Run from the repository root:

```sh
python3 -m unittest discover -s 04-computer-systems/abi-loading -v
python3 04-computer-systems/abi-loading/run_native.py
```

The native path needs Linux x86-64, a C compiler and GNU readelf/objdump/nm;
the runner returns BLOCKED if they are absent. The portable suite has ten
methods, including independent cache-history and affine translation checks.
Historical [native output](evidence/native-observed-2026-10-25.json) and
[model tests](evidence/model-tests-2026-10-25.txt) are retained; the delivery
verification additionally records a fresh actual execution.

Primary ABI/specification verification is still an explicit documentation gap
in this recovered unit. Native observations and local model contracts are the
evidence available here. Do not treat a previous author's unpreserved source
inspection report as a current complete source map. Remaining work: explain
the call/return and load derivations step by step, add source locators and
worked transfer exercises, then independently review full systems breadth.
