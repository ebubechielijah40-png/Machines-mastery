# Master curriculum — self-contained prepared edition

This is the learner-facing curriculum. `MASTER_CURRICULUM.md` remains the registry-derived historical/core phase index; this edition adds the permanent quantum and cryptography depth tracks and points to self-contained material.

## Phase 0 — learning/research method
Evidence logging, prediction before observation, source/provenance discipline, tests, experiments, reconstruction, and transfer. Start with `SELF_CONTAINED_STUDY.md`.

## Phase 1 — computation and machine foundations
Number representation, Boolean logic, electricity bridge, transistor switching model, gates, state, memory, ALU, datapath, control, CPU, ISA. Use `01-computation/SELF_CONTAINED_GUIDE.md`, `hardware-electronics-mastery/DEEP_GUIDE.md`, and HDL tracks.

## Phase 2 — programming and systems languages
Python/Shell for leverage; C for machine-oriented programming; x86-64/RISC-V/ARM64 for ISA reasoning; C++/Rust/Zig for systems design; Java/Go/SQL when their system contexts arrive. Use `programming-languages-mastery/`.

## Phase 3 — algorithms and complexity
Invariants, correctness, asymptotics, empirical complexity, core data structures, graph/DP/greedy methods, and applied problem sets. Use `03-algorithms/SELF_CONTAINED_GUIDE.md` and `algorithmic-problem-solving/`.

## Phase 4 — computer systems
Compilation, linking/loading, memory layout, caches, syscalls, processes, threads, binary inspection, concurrency. Use `04-computer-systems/SELF_CONTAINED_GUIDE.md`.

## Phase 5 — operating systems
Privilege, scheduling, virtual memory, filesystems, synchronization, IPC, interrupts/drivers. Use `05-operating-systems/SELF_CONTAINED_GUIDE.md`.

## Phase 6 — networking
Signals/links conceptually, IP/routing, UDP/TCP, DNS, HTTP, TLS concepts, sockets, partial failure, backpressure. Use `06-networking/SELF_CONTAINED_GUIDE.md` and code labs.

## Phase 7 — databases and data systems
Relational modeling/SQL, pages/indexes, transactions/isolation, query planning, warehouses/lakes, batch/stream, lineage, provenance, scaling. Use `07-databases-data-systems/SELF_CONTAINED_GUIDE.md` and SQLite lab.

## Phase 8 — information science and scientific reasoning
Data/information/evidence/claim/knowledge distinctions, provenance, metadata, measurement, uncertainty, experiments, causality, reproducibility. Use phases 08/09 and research reconstruction.

## Phase 9 — data science
Probability/statistics, EDA, regression, Bayesian reasoning, data quality, scientific computing, leakage and reproducibility. Use `10-data-science/`.

## Phase 10 — security, cryptography, privacy
Threat models, authn/authz, secure coding, hashes/MACs, AEAD, public-key systems, key management/PKI, storage/data security, privacy engineering, incidents, post-quantum implications. Use `security-cryptography-mastery/` plus phases 11–13.

## Phase 11 — programming languages, compilers and runtimes
Lexing/parsing, ASTs, semantics/types, interpreters, bytecode/VMs, code generation, GC, ABIs. Use phase 14 and language deep guides.

## Phase 12 — distributed and production systems
Failure models, replication, consistency, consensus, transactions, queues, idempotency, scalability, observability, deployment, load/stress testing, recovery/postmortems. Use phase 15 and `production-systems-engineering/`.

## Phase 13 — ML and AI systems
Linear models, trees, neural networks, optimization, evaluation, serving, drift, robustness, security/privacy and production measurement. Use phase 16.

## Phase 14 — embedded systems, control and robotics
Electronics, microcontrollers, firmware, sensors, actuators, timing, feedback/control, robotics integration and physical-machine limits. Use phase 17 plus machine teardown units.

## Phase 15 — computational biology
Chemistry/molecular bridge, sequence algorithms, genomics, evolution, systems biology, structural/computational biology, statistical interpretation and reproducible bioinformatics. Use `18-computational-biology/DEEP_HANDBOOK.md`.

## Phase 16 — quantum computing and quantum machines
Complex vectors/matrices, qubits, phase/interference, entanglement, measurement, circuits, algorithms, noise/error correction, hardware modalities, control stack, cryptographic impact and limits. Use `20-quantum-computing/`.

## Phase 17 — experimental research and unfamiliar-system investigation
Paper reconstruction, reproduction/replication, measurement, uncertainty, source code/binary/protocol/hardware/physical-machine reverse engineering, black-box inference and reconstruction from memory. Use phase 19, `research-paper-reconstruction/`, and `reverse-engineering-systems/`.

## Capstone standard
A capstone should force at least five of: build, explain, test, measure, fail, debug, scale, secure, operate, reproduce, reconstruct, transfer. The final capability is not “know every system”; it is “meet an unfamiliar system and know how to find out how it works.”
