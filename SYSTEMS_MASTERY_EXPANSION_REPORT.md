# Systems Mastery Expansion Report

Date: 2026-09-27. This document records the systems mastery expansion, distinguishing fully realized executable exemplars from scaffolded tracks, and documenting local validation limits.

## 1. Expansion Architecture and Purpose

The machines-mastery environment expanded from its initial single-chapter intake (*Code*, Chapter 1) into a multi-track technical research and learning environment. The architecture is organized around two foundational models:
1. `REALITY → observation → measurement → raw data → representation → collection → transmission → storage → transformation → analysis → information → interpretation → knowledge/conclusion → decision`
2. `DATA → representation → transmission → computation → storage → protection → verification`

To prevent superficial coverage and avoid jumping across unearned prerequisites, nine connected tracks were added with machine-checkable prerequisite gates and evidence discipline:
- **Foundations (`foundations/`):** Just-in-time mathematics, physics, materials, statistics, and programming bridges.
- **Programming Languages Mastery (`programming-languages-mastery/`):** Fourteen dependency-timed language tracks (C, C++, Rust, Zig, x86-64, ARM64, RISC-V, Python, Go, Java, SQL, Bash, SystemVerilog, VHDL), each with a 28-file scope curriculum (`00_*.md` to `27_*.md`).
- **Hardware Description Languages (`hardware-description-languages/`):** SystemVerilog/Verilog and VHDL hardware descriptions, testbenches, and hardware boundaries.
- **Hardware and Electronics Mastery (`hardware-electronics-mastery/`):** Physical quantities, circuit laws, semiconductor devices, logic gates, and digital abstraction.
- **Reverse Engineering Systems (`reverse-engineering-systems/`):** 29 methodological guides (`00_*.md` to `28_*.md`) from observation and black-box analysis to decomposition, binary analysis, and independent reconstruction.
- **General Machine Systems (`general-machine-systems/`):** Physical machines, energy, sensors, actuators, and control loops.
- **Algorithmic Problem Solving (`algorithmic-problem-solving/`):** 31 distinct algorithmic topic areas with rigorous release quotas (at least 20 problems per topic with separate prompts, hints, solutions, and tests) and complexity experiments.
- **Research Paper Reconstruction (`research-paper-reconstruction/`):** 18 scientific domains with a 10-paper domain quota, paper reconstruction methodology, and reading plans.
- **Production Systems Engineering (`production-systems-engineering/`):** Cross-cutting operational discipline covering architecture, benchmarks, failures, observability, scalability, security, ADRs, postmortems, and load testing.

## 2. Distinction: Executable Exemplars vs. Scaffolded Scope

A foundational policy of this repository is that **infrastructure generation is not learning**, and **scaffolding is not implementation**. The expansion explicitly distinguishes between:

### A. Fully Implemented Executable Exemplars

**Post-expansion continuation:** the algorithmic track now also includes an **Arrays 20-problem release** under `algorithmic-problem-solving/topics/arrays/`. It is a learner-facing problem set with separate prompts/hints/solutions and executable tests, not a mastery claim.

Five initial exemplars were fully constructed, compiled/simulated, and tested locally:
1. **`U-CEX` (Bounded C Byte Parser):**
   - Path: `programming-languages-mastery/01-c/units/01-byte-parser/`
   - Complete C implementation (`solutions/parser.c`), lesson, proofs, hints, problem statement, and test suite (`tests/run.py`).
   - Exhaustively tested across 65,536 16-bit values, boundary conditions, null inputs, and short buffers under `-O0`, `-O2`, and `-fsanitize=undefined`.
2. **`U-RVEX` (RV32I ADDI Encoding & Transition):**
   - Path: `programming-languages-mastery/07-riscv-assembly/units/01-addi/`
   - Machine instruction bit-field encoder and register transition model (`solutions/model.py`), assembly test program (`solutions/program.s`), and test suite (`tests/run.py`).
   - Exhaustively verifies all 4,096 12-bit signed immediate values, sign extension, zero-register invariant (`x0 == 0`), and cross-checks against GNU as/objdump.
3. **`U-SVEX` (Synchronous Enabled Register):**
   - Path: `hardware-description-languages/systemverilog/units/01-enabled-register/`
   - RTL implementation (`solutions/register.sv`), intentionally broken priority mutant (`solutions/broken_priority.sv`), testbench (`tests/tb.sv`), and test runner (`tests/run.py`).
   - Simulated with Icarus Verilog (`iverilog`), testing 1,024 clock cycles with random inputs, synchronous reset priority, hold stability, and mutant rejection.
4. **`U-REEX` (Hidden-State Oracle & Black-Box Reconstruction):**
   - Path: `reverse-engineering-systems/exercises/01-hidden-state/`
   - Unknown black-box oracle (`oracle.py`), hints, problem prompt, verified replica (`reveal/replica.py`), and test suite (`tests/test_oracle.py`).
   - Tests hypothesis generation, state discovery, transition table derivation, and exact behavior replication without inspecting source code.
5. **`U-PROD` (Production Event Ledger):**
   - Path: `production-systems-engineering/labs/event-ledger/`
   - Production SQLite ledger with query indexing, in-memory caching, idempotency checks, and failure injection (`service.py`).
   - Full evidence suite: `DESIGN.md`, `ARCHITECTURE.md`, `ASSUMPTIONS.md`, `BENCHMARKS.md`, `FAILURES.md`, `EXPERIMENTS.md`, `SECURITY.md`, `OBSERVABILITY.md`, `SCALABILITY.md`, `POSTMORTEMS.md`, `ADR-001.md`, `RESULTS.md`.
   - Executable benchmark (`benchmark.py`) run across 1,000, 100,000, and 1,000,000 synthetic events, capturing latency percentiles (p50/p95/p99), memory RSS, and query execution plans.

### B. Scaffolded Tracks and Release Quotas
All other units, languages, algorithms, and paper domains are structured curriculum blueprints and scaffolds:
- The 14 language curricula establish standard 28-topic scope breakdowns for future deep reconstruction.
- The 31 algorithmic topics establish release gates requiring 20 fully specified, test-backed problems before any topic is marked complete.
- The 18 research domains establish release gates requiring 10 verified primary-source papers with full reconstructions before any domain is marked complete.
- Scaffolds do not satisfy prerequisites. No scaffolded topic is marked studied, completed, or mastered.

## 3. Validation Limits and Environment

- **Tools and Dependencies:** Core repository validation (`tools/validate.py`, `tools/validate_expansion.py`, `tools/render.py`, `tools/learning_gate.py`) uses standard Python 3.10+ with zero external packages.
- **Local Compilers and Simulators:** Exemplars rely on local binaries (`gcc`, `iverilog`, `riscv64-unknown-elf-as`/`objdump`). Where toolchains are absent or sandboxed, tests report exact environmental requirements rather than faking success.
- **Validation Modes:**
  - `python3 tools/validate.py` checks structural integrity, file formatting (final newline, no trailing whitespace), link validity, catalog consistency, and gate conditions. It reports 0 errors and documents known source/license warnings.
  - Strict mode (`--strict`) intentionally returns nonzero exit status because 66 primary resources remain unverified or source-restricted pending direct inspection.
  - `python3 tools/validate_expansion.py` checks expansion artifacts, file quotas, and exemplar completeness.
- **Learner Status:** All learner states remain **NOT STARTED**. No automated test, agent measurement, benchmark execution, or scaffold generation counts as learner understanding or mastery.
