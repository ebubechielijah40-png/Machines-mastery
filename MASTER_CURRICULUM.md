# Master Curriculum

<!-- Generated from registries/catalog.json by tools/render.py; edit the catalog. -->

This is a dependency-driven plan, not a processed reading list. All learning remains NOT STARTED. Use [PREREQUISITE_GRAPH.md](PREREQUISITE_GRAPH.md) to select a bounded unit and [RESOURCE_REGISTRY.md](RESOURCE_REGISTRY.md) to check each source before use.

## Study depth

- **MUST STUDY DEEPLY:** each phase’s core mechanism and required entry bridges; explain, derive, apply and test.
- **REFERENCE:** syntax tables, API details, tool flags and catalogs once the mechanism is understood.
- **OPTIONAL DEPTH:** advanced extensions with no current dependency; defer with a reason.
- **HISTORICAL/CONTEXT:** background that contextualizes a mechanism without gating implementation.

These are planning rules, not chapter classifications. Classify actual source units only after inspection. A difficult foundational chapter is still required.

## Dependency corrections

Keep the requested phase progression with small entry bridges: U00 establishes evidence logging at the start; U05 introduces only the process/descriptor concepts needed for the shell; U06 supplies proof/discrete mathematics before algorithms. Probability precedes inference and cryptography; linear algebra/calculus precede advanced regression and gradients. Physical measurement, mechanics and differential equations gate control; chemistry and cell/genetic foundations gate biological interpretation. These are design decisions preventing specific gaps, not additional survey courses. Formal scientific reasoning remains P08, but predictions and raw logs begin with the first experiment. TLS is introduced operationally in P06 and cryptographically in P10. Distributed database sections wait for P13. P15/P16 do not require completion of unrelated earlier applications; follow the graph.

## P01 — Computation and the Machine

**Core scope — MUST STUDY DEEPLY:** computation; information representation; binary and number systems; Boolean logic; gates; digital circuits; CPU; memory; machine language; assembly; hardware/software boundary.

**Resources:** R-CODE, R-ELEMENTS, R-NAND, R-SV, R-DISCRETE, R-ELECTRIC. Verify status before selection.

**Demonstrable outcome:** Trace a small instruction through a designed machine; predict state changes before simulation.

**Project:** J-01 in [PROJECT_REGISTRY.md](PROJECT_REGISTRY.md). **Subject paths:** [01-computation](01-computation/README.md), [hardware-description-languages](hardware-description-languages/README.md), [foundations](foundations/README.md).

**Learning state:** NOT STARTED.

## P02 — Programming

**Core scope — MUST STUDY DEEPLY:** fundamentals; C; Python; data types; functions; recursion; data structures; pointers; memory management; files; debugging; testing; Git.

**Resources:** R-C, R-PYTHON, R-DIVE, R-BYOX, R-C11. Verify status before selection.

**Demonstrable outcome:** Implement and debug programs; account for ownership, lifetime and error paths.

**Project:** J-02 in [PROJECT_REGISTRY.md](PROJECT_REGISTRY.md). **Subject paths:** [02-programming](02-programming/README.md), [programming-languages-mastery](programming-languages-mastery/README.md).

**Learning state:** NOT STARTED.

## P03 — Algorithms

**Core scope — MUST STUDY DEEPLY:** data structures; complexity and Big O; searching; sorting; trees; graphs; dynamic programming; correctness; benchmarking.

**Resources:** R-ALGORITHMS, R-ALGO-PY, R-DISCRETE. Verify status before selection.

**Demonstrable outcome:** Justify correctness and complexity; compare measured behavior with predictions.

**Project:** J-03 in [PROJECT_REGISTRY.md](PROJECT_REGISTRY.md). **Subject paths:** [03-algorithms](03-algorithms/README.md), [algorithmic-problem-solving](algorithmic-problem-solving/README.md).

**Learning state:** NOT STARTED.

## P04 — Computer Systems

**Core scope — MUST STUDY DEEPLY:** compilation; machine code; linking; loading; memory layout; stack; heap; caches; system calls; processes; threads; concurrency; reverse engineering.

**Resources:** R-CSAPP, R-DIVE, R-XV6. Verify status before selection.

**Demonstrable outcome:** Trace compiled execution and allocations; distinguish model, source evidence and observation.

**Project:** J-04 in [PROJECT_REGISTRY.md](PROJECT_REGISTRY.md). **Subject paths:** [04-computer-systems](04-computer-systems/README.md).

**Learning state:** NOT STARTED.

## P05 — Operating Systems

**Core scope — MUST STUDY DEEPLY:** architecture; scheduling; virtual memory; filesystems; interrupts; system calls; synchronization; kernel/user boundary.

**Resources:** R-OSTEP, R-XV6, R-OSTEP-HW. Verify status before selection.

**Demonstrable outcome:** Explain and test a small kernel change in an isolated emulator.

**Project:** J-05 in [PROJECT_REGISTRY.md](PROJECT_REGISTRY.md). **Subject paths:** [05-operating-systems](05-operating-systems/README.md).

**Learning state:** NOT STARTED.

## P06 — Networking

**Core scope — MUST STUDY DEEPLY:** fundamentals; TCP/IP; addressing; routing; TCP; UDP; DNS; HTTP; TLS; sockets; network programming; distributed communication.

**Resources:** R-NET, R-BEEJ, R-BEEJ-REPO. Verify status before selection.

**Demonstrable outcome:** Trace a request across interfaces and explain partial I/O and disconnections.

**Project:** J-06 in [PROJECT_REGISTRY.md](PROJECT_REGISTRY.md). **Subject paths:** [06-networking](06-networking/README.md).

**Learning state:** NOT STARTED.

## P07 — Databases and Data Systems

**Core scope — MUST STUDY DEEPLY:** data models; relational modeling; SQL; indexes; transactions; concurrency; query execution; storage engines; B-trees; warehouses; lakes; pipelines; lineage; metadata; quality.

**Resources:** R-DB, R-DDIA, R-SQLITE, R-TOYDB. Verify status before selection.

**Demonstrable outcome:** Build persistence and recovery with explicit transactional boundaries.

**Project:** J-07 in [PROJECT_REGISTRY.md](PROJECT_REGISTRY.md). **Subject paths:** [07-databases-data-systems](07-databases-data-systems/README.md).

**Learning state:** NOT STARTED.

## P08 — Information Science and Scientific Reasoning

**Core scope — MUST STUDY DEEPLY:** data, information and knowledge; fact and claim; evidence; context; metadata; provenance; measurement; uncertainty; source criticism; scientific method; experimental design; sampling; correlation and causation; reproducibility and replication.

**Resources:** R-CRAFT, R-STATS, R-STATS-REPO, R-DATA8, R-CODE. Verify status before selection.

**Demonstrable outcome:** Trace a claim back to collection and measurement; delimit what the evidence supports.

**Project:** J-08 in [PROJECT_REGISTRY.md](PROJECT_REGISTRY.md). **Subject paths:** [08-information-science](08-information-science/README.md), [09-scientific-reasoning](09-scientific-reasoning/README.md), [reverse-engineering-systems](reverse-engineering-systems/README.md).

**Learning state:** NOT STARTED.

## P09 — Data Science

**Core scope — MUST STUDY DEEPLY:** probability; statistics; inference; regression; Bayesian reasoning; acquisition; cleaning; validation; EDA; visualization; feature engineering; experimental analysis; scientific computing.

**Resources:** R-PYDATA, R-PYDATA-REPO, R-STATS, R-DATA8, R-LINEAR, R-CALCULUS. Verify status before selection.

**Demonstrable outcome:** Produce a reproducible analysis with uncertainty, leakage checks and data provenance.

**Project:** J-09 in [PROJECT_REGISTRY.md](PROJECT_REGISTRY.md). **Subject paths:** [10-data-science](10-data-science/README.md).

**Learning state:** NOT STARTED.

## P10 — Data Security and Cybersecurity

**Core scope — MUST STUDY DEEPLY:** principles; threat modeling; authentication; authorization; access control; cryptography; encryption; hashing; MACs; signatures; integrity; authenticity; secure storage and transmission; network, application and database security; vulnerability analysis; monitoring; incident response; forensics.

**Resources:** R-SECURITY, R-CRYPTO, R-OWASP, R-CRYPTOPALS. Verify status before selection.

**Demonstrable outcome:** Test security boundaries of a local pipeline against an explicit threat model.

**Project:** J-10 in [PROJECT_REGISTRY.md](PROJECT_REGISTRY.md). **Subject paths:** [11-cybersecurity](11-cybersecurity/README.md), [12-data-security](12-data-security/README.md).

**Learning state:** NOT STARTED.

## P11 — Privacy and Trusted Information

**Core scope — MUST STUDY DEEPLY:** classification; minimization; anonymization; pseudonymization; differential privacy; privacy-preserving analytics; auditability; traceability; integrity verification; secure sharing; retention; secure deletion.

**Resources:** R-PRIVACY, R-SECURITY, R-OWASP. Verify status before selection.

**Demonstrable outcome:** Verify recorded transformations while stating what provenance cannot establish about reality.

**Project:** J-11 in [PROJECT_REGISTRY.md](PROJECT_REGISTRY.md). **Subject paths:** [13-privacy](13-privacy/README.md).

**Learning state:** NOT STARTED.

## P12 — Programming Languages and Compilers

**Core scope — MUST STUDY DEEPLY:** language design; lexing; parsing; AST; semantic analysis; types; interpreters; bytecode; virtual machines; code generation; runtimes; garbage collection.

**Resources:** R-INTERPRETERS, R-INTERPRETERS-REPO. Verify status before selection.

**Demonstrable outcome:** Implement a language with defined evaluation and error semantics.

**Project:** J-12 in [PROJECT_REGISTRY.md](PROJECT_REGISTRY.md). **Subject paths:** [14-programming-languages](14-programming-languages/README.md).

**Learning state:** NOT STARTED.

## P13 — Distributed Systems

**Core scope — MUST STUDY DEEPLY:** distributed computation; replication; consistency; consensus; fault tolerance; distributed transactions; scalability; distributed storage.

**Resources:** R-DDIA, R-TOYDB, R-SRE, R-SQLITE-LAB. Verify status before selection.

**Demonstrable outcome:** State a fault model, inject failures and compare observed histories with promised semantics.

**Project:** J-13 in [PROJECT_REGISTRY.md](PROJECT_REGISTRY.md). **Subject paths:** [15-distributed-systems](15-distributed-systems/README.md), [production-systems-engineering](production-systems-engineering/README.md).

**Learning state:** NOT STARTED.

## P14 — Machine Learning and AI

**Core scope — MUST STUDY DEEPLY:** regression; classification; clustering; evaluation; optimization; neural networks; deep learning; representation learning; ML systems; model security and reliability.

**Resources:** R-HOML, R-HOML-REPO, R-MICROGRAD, R-LINEAR, R-CALCULUS. Verify status before selection.

**Demonstrable outcome:** Derive and check gradients; evaluate generalization separately from training performance.

**Project:** J-14 in [PROJECT_REGISTRY.md](PROJECT_REGISTRY.md). **Subject paths:** [16-machine-learning](16-machine-learning/README.md).

**Learning state:** NOT STARTED.

## P15 — Embedded Systems and Robotics

**Core scope — MUST STUDY DEEPLY:** electronics; microcontrollers; embedded C; sensors; actuators; firmware; real-time systems; control; robotics; autonomous systems; hardware/software integration.

**Resources:** R-EMBEDDED, R-ROBOTICS, R-PHYSICS, R-ELECTRIC. Verify status before selection.

**Demonstrable outcome:** Measure sensor behavior and timing; explain calibration, control and physical limitations.

**Project:** J-15 in [PROJECT_REGISTRY.md](PROJECT_REGISTRY.md). **Subject paths:** [17-embedded-robotics](17-embedded-robotics/README.md), [hardware-electronics-mastery](hardware-electronics-mastery/README.md), [general-machine-systems](general-machine-systems/README.md).

**Learning state:** NOT STARTED.

## P16 — Computational Biology

**Core scope — MUST STUDY DEEPLY:** biology; chemistry; genetics; molecular biology; biochemistry; evolution; bioinformatics; genomics; systems biology; mathematical biology; synthetic biology.

**Resources:** R-CELL, R-CHEM, R-BIOPYTHON. Verify status before selection.

**Demonstrable outcome:** Analyze public biological data while separating computational output from biological interpretation.

**Project:** J-16 in [PROJECT_REGISTRY.md](PROJECT_REGISTRY.md). **Subject paths:** [18-computational-biology](18-computational-biology/README.md).

**Learning state:** NOT STARTED.

## P17 — Experimental Research

**Core scope — MUST STUDY DEEPLY:** research questions; literature; evidence evaluation; measurement; design; collection; analysis; reproduction; replication; reproducibility; documentation; scientific writing.

**Resources:** R-CRAFT, R-STATS. Verify status before selection.

**Demonstrable outcome:** Reproduce a bounded published result; document discrepancies and limits before proposing extensions.

**Project:** J-17 in [PROJECT_REGISTRY.md](PROJECT_REGISTRY.md). **Subject paths:** [19-experimental-research](19-experimental-research/README.md), [research-paper-reconstruction](research-paper-reconstruction/README.md).

**Learning state:** NOT STARTED.

## Advanced-source selection gates

Before consensus reproduction, select and inspect an original paper with its fault model; before research reproduction, select one original paper and the relevant domain prerequisites. No paper, dataset, hardware board or benchmark result has been selected by guesswork. Rust/Java and mathematical or physical bridges are learned only if the chosen implementation requires them. Chemistry/physics candidate sources need readable primary verification before study.

## Permanent connected tracks

Prepared exemplars and scaffolded scope are distinct. Learner progress requires actual evidence. Use internal prerequisite bridges; original sources are the verification layer, not mandatory learner reading.

| Track | Entry gates | Integrated units | Preparation |
| --- | --- | --- | --- |
| [Programming languages mastery](programming-languages-mastery/README.md) | U04 | L01, L02, L03, L04, L05, L06, L07, L08, L09, L10, L11, L12, L13, L14 | INFRASTRUCTURE |
| [Hardware description languages](hardware-description-languages/README.md) | U02 | U-SVEX, L13, L14 | INFRASTRUCTURE |
| [Hardware and electronics](hardware-electronics-mastery/README.md) | F-COUNT, F-ELECTRIC | F-ELECTRIC, U02, U19 | INFRASTRUCTURE |
| [Reverse engineering systems](reverse-engineering-systems/README.md) | U00 | U-REEX, U12 | INFRASTRUCTURE |
| [Algorithmic problem solving](algorithmic-problem-solving/README.md) | U04, U06 | U07 | INFRASTRUCTURE |
| [Research paper reconstruction](research-paper-reconstruction/README.md) | U12, U13 | U21 | INFRASTRUCTURE |
| [General machine systems](general-machine-systems/README.md) | F-COUNT, F-ELECTRIC | U19 | INFRASTRUCTURE |
| [Production systems engineering](production-systems-engineering/README.md) | U04, U12 | U-PROD, U09, U10, U11, U17, U18, U19 | INFRASTRUCTURE |
| [Just-in-time foundations](foundations/README.md) | None | F-COUNT, F-BITS, F-STATE, F-ELECTRIC, F-CENTRY | INFRASTRUCTURE |

Early language use is Shell/Python/C; x86-64 and basic RISC-V follow representation/state; C++/Rust/Zig enter systems projects; SQL joins databases, Go networking, Java runtimes, ARM64 embedded systems and SystemVerilog/VHDL digital hardware. Do not finish fourteen courses sequentially.

Prepared foundation bridges descend only as far as needed. Unprepared prerequisite topics block learner progression rather than silently assuming mathematics, physics, materials or statistics.

Production thinking enters every phase through code, tests, measurements, failure/recovery, observability and reviewed design decisions. See [production laboratory](production-systems-engineering/README.md).
