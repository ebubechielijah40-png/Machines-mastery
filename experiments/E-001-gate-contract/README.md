# E-001 — Combinational Circuit Truth-Table Check

Project J-01 / P01. Status: PLANNED. Source-ready: false. This is an original proposed protocol, not a performed experiment or a reconstruction of an upstream exercise.

## Question and background

Can an independently specified small combinational component satisfy its complete finite input/output contract, and can our checks detect a deliberately introduced fault?

Background source: R-NAND, identity verified only. Exact component specification and locator: **UNVERIFIED — source required.** Select the component after U02 study. No gate behavior is attributed to an unread source.

## Hypothesis

Under a chosen deterministic finite Boolean model, a correct implementation will match the independently derived contract on every valid input. A selected fault that changes behavior should produce a reproducible mismatch. These are predictions, not observations.

## Variables and controls

Manipulated: valid input tuple; baseline versus deliberately altered implementation. Measured: actual outputs and mismatch count. Controls: same specification, input enumeration, reference table, environment and initial conditions. Prevent oracle leakage by deriving expected outputs before writing the implementation.

## Setup

Not selected: component, input width, simulator/language, tool version and code revision. Record them before execution. Use a local deterministic simulator or program with synthetic inputs; no external targets, private data or hardware purchases are needed.

## Procedure and measurements

1. Inspect and cite the original contract, or explicitly define a local contract without claiming upstream compatibility.
2. Derive the reference table by hand and review it independently.
3. Implement the component only after learner prerequisites are satisfied.
4. Enumerate every input in the specified finite domain and record expected and actual outputs.
5. Introduce one documented change predicted to alter behavior; identify a discriminating input before running it.
6. Repeat the comparison and preserve both successful and failed runs with command, exit status, tool version, source hashes and actual output.

Record each input/output tuple and mismatch; no timing or physical behavior claim follows from this protocol. Add `raw/` only when output exists.

## Expected result

Baseline: no contract mismatches if the model and implementation agree. Altered implementation: at least one mismatch for the chosen distinguishing input. This conditional prediction does not prove the oracle or source interpretation correct.

## Observed result

**NOT YET OBSERVED.**

## Analysis, alternatives and error sources

Analysis awaits execution. Planned alternatives to investigate: incorrect oracle, wrong input ordering, omitted input combinations, mutation that preserves behavior, simulator convention mismatch or correlated mistakes in implementation and test.

## Conclusion and follow-up

No empirical conclusion. After execution, determine whether failures distinguish implementation errors from specification errors. A possible follow-up is composition of two verified components, contingent on the first result and learner explanation.
