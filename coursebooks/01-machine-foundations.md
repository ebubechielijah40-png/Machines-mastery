# Machine Foundations — original self-contained coursebook

This is an original teaching text for **representation, electricity, digital logic, CPU state, memory, ISA and hardware/software boundaries**. It is not a reproduction of any copyrighted textbook. Use it as the narrative entry point, then follow the linked deep guides/labs for implementations and tests.

## How to read this coursebook

For each topic: identify the problem that forced the concept to exist; build the simplest model; trace state and interfaces; predict behavior; run an experiment; then reconstruct from memory. Definitions without mechanisms do not count as understanding.

## Core questions

1. What state exists, and where?
2. What transforms that state?
3. What information enters and leaves?
4. What resources are consumed?
5. What invariants must remain true?
6. What assumptions make the model valid?
7. What breaks first under scale, noise, concurrency, or adversarial input?
8. What experiment would distinguish two competing explanations?
9. What can be implemented as a minimal model?
10. What remains impossible or unknowable from the available evidence?

## Learning architecture

Start with an observable phenomenon. Descend abstractions until you can explain the mechanism, then rise again to application. The same pattern applies whether the system is a CPU, database, protein sequence pipeline, robot, or quantum circuit.

### Worked-method example
Suppose a system becomes slow. “It is slow” is an observation, not a diagnosis. Measure latency distribution and throughput; inspect CPU, memory, I/O, queueing, lock contention, cache behavior, and dependency latency; form a hypothesis; change one variable; measure again. The result is evidence for or against the model, not proof of every causal story.

## Required practice

- at least one hand-worked state trace;
- at least one executable model;
- at least one failure injection or counterexample;
- at least one scaling/complexity measurement where meaningful;
- one reconstruction without notes;
- one transfer problem with unfamiliar surface details.

## Deep material
- `foundations/mathematics/DEEP_GUIDE.md`
- `foundations/physics/DEEP_GUIDE.md`
- `hardware-electronics-mastery/README.md`
- `01-computation/README.md`

## Exit standard

Do not exit because you have read the file. Exit when you can explain the mechanism, implement a bounded version, test it, state limitations, and transfer the model to a new case.
