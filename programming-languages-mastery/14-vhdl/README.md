# VHDL

Infrastructure and introductory model; learner NOT STARTED. Required curriculum gate: U02; take exact lesson bridges before an exemplar. Canonical HDL route: [VHDL](../../hardware-description-languages/vhdl/README.md).

Purpose: strongly specified hardware interfaces and event models.

```text
entities/architectures → elaboration → simulation or synthesis → hardware
```

Projects, in increasing scope: gate; adder; ALU; register; counter; FSM; memory interface; processor component. These are plans, not implementations.

[Primary evidence](https://ghdl.github.io/ghdl/about.html); full semantics and version-specific details outside prepared units remain UNVERIFIED — verification required.

| Area | Preparation |
| --- | --- |
| [Language Model](00_LANGUAGE_MODEL.md) | INTRODUCTION |
| [Origin And Purpose](01_ORIGIN_AND_PURPOSE.md) | INTRODUCTION |
| [Execution Model](02_EXECUTION_MODEL.md) | INTRODUCTION |
| [Syntax](03_SYNTAX.md) | SCAFFOLDED |
| [Types](04_TYPES.md) | SCAFFOLDED |
| [Values And Representation](05_VALUES_AND_REPRESENTATION.md) | SCAFFOLDED |
| [Memory Model](06_MEMORY_MODEL.md) | SCAFFOLDED |
| [Control Flow](07_CONTROL_FLOW.md) | SCAFFOLDED |
| [Functions](08_FUNCTIONS.md) | SCAFFOLDED |
| [Data Structures](09_DATA_STRUCTURES.md) | SCAFFOLDED |
| [Module System](10_MODULE_SYSTEM.md) | SCAFFOLDED |
| [Error Model](11_ERROR_MODEL.md) | SCAFFOLDED |
| [Io](12_IO.md) | SCAFFOLDED |
| [Os Interaction](13_OS_INTERACTION.md) | SCAFFOLDED |
| [Concurrency](14_CONCURRENCY.md) | SCAFFOLDED |
| [Compilation Or Runtime](15_COMPILATION_OR_RUNTIME.md) | SCAFFOLDED |
| [Abi And Interoperability](16_ABI_AND_INTEROPERABILITY.md) | SCAFFOLDED |
| [Performance](17_PERFORMANCE.md) | SCAFFOLDED |
| [Debugging](18_DEBUGGING.md) | SCAFFOLDED |
| [Security](19_SECURITY.md) | SCAFFOLDED |
| [Internals](20_INTERNALS.md) | SCAFFOLDED |
| [Machine Level View](21_MACHINE_LEVEL_VIEW.md) | SCAFFOLDED |
| [Examples](22_EXAMPLES.md) | SCAFFOLDED |
| [Exercises](23_EXERCISES.md) | SCAFFOLDED |
| [Experiments](24_EXPERIMENTS.md) | SCAFFOLDED |
| [Projects](25_PROJECTS.md) | SCAFFOLDED |
| [Reference](26_REFERENCE.md) | SCAFFOLDED |
| [Mastery](27_MASTERY.md) | SCAFFOLDED |

## Developed VHDL queue

After logic states and clocked registers, build [the VHDL clocked queue](units/clocked-queue/README.md). The shared contract has original VHDL/SystemVerilog implementations, independent vectors, native testbenches and deliberate semantic mutants.
