# Project Registry

<!-- Generated from registries/catalog.json by tools/render.py; edit the catalog. -->

Only PREPARED projects have materialized documentation. PLANNED entries are bounded future work, not implementations. All stages start at A; no completion or authorship is implied. See [project workflow](projects/README.md). J-04 groups allocator, compiled-program inspection and systems experiments; J-06 groups TCP server, HTTP server and a small networked system.

| ID / phase | Project | Status / stage | Original resource candidates | Outcome |
| --- | --- | --- | --- | --- |
| J-01 / P01 | [Logic To Cpu](projects/logic-to-cpu/README.md) | PREPARED / A — NOT STARTED | R-NAND, R-ELEMENTS | Trace a small instruction through a designed machine; predict state changes before simulation. |
| J-02 / P02 | Unix Shell | PLANNED / A — NOT STARTED | R-C | Implement and debug programs; account for ownership, lifetime and error paths. |
| J-03 / P03 | Algorithms Library | PLANNED / A — NOT STARTED | R-ALGORITHMS | Justify correctness and complexity; compare measured behavior with predictions. |
| J-04 / P04 | Systems Lab | PLANNED / A — NOT STARTED | R-CSAPP | Trace compiled execution and allocations; distinguish model, source evidence and observation. |
| J-05 / P05 | Xv6 Study | PLANNED / A — NOT STARTED | R-OSTEP | Explain and test a small kernel change in an isolated emulator. |
| J-06 / P06 | Network Servers | PLANNED / A — NOT STARTED | R-NET | Trace a request across interfaces and explain partial I/O and disconnections. |
| J-07 / P07 | Storage Engine | PLANNED / A — NOT STARTED | R-DB | Build persistence and recovery with explicit transactional boundaries. |
| J-08 / P08 | Claim Trace | PLANNED / A — NOT STARTED | R-CRAFT | Trace a claim back to collection and measurement; delimit what the evidence supports. |
| J-09 / P09 | Scientific Pipeline | PLANNED / A — NOT STARTED | R-PYDATA | Produce a reproducible analysis with uncertainty, leakage checks and data provenance. |
| J-10 / P10 | Secure Pipeline | PLANNED / A — NOT STARTED | R-SECURITY | Test security boundaries of a local pipeline against an explicit threat model. |
| J-11 / P11 | Provenance System | PLANNED / A — NOT STARTED | R-PRIVACY | Verify recorded transformations while stating what provenance cannot establish about reality. |
| J-12 / P12 | Interpreter | PLANNED / A — NOT STARTED | R-INTERPRETERS | Implement a language with defined evaluation and error semantics. |
| J-13 / P13 | Replicated Kv | PLANNED / A — NOT STARTED | R-DDIA | State a fault model, inject failures and compare observed histories with promised semantics. |
| J-14 / P14 | Autodiff Engine | PLANNED / A — NOT STARTED | R-HOML | Derive and check gradients; evaluate generalization separately from training performance. |
| J-15 / P15 | Sensor System | PLANNED / A — NOT STARTED | R-EMBEDDED | Measure sensor behavior and timing; explain calibration, control and physical limitations. |
| J-16 / P16 | Biological Analysis | PLANNED / A — NOT STARTED | R-CELL | Analyze public biological data while separating computational output from biological interpretation. |
| J-17 / P17 | Research Reproduction | PLANNED / A — NOT STARTED | R-CRAFT | Reproduce a bounded published result; document discrepancies and limits before proposing extensions. |
| J-CAP01 / P01 | Software for a understood HDL processor | PLANNED / A — NOT STARTED | R-RV32, R-SV | Match a declared ISA subset instruction-by-instruction from C/assembly through HDL CPU. |
| J-CAP02 / P05 | Kernel and process reconstruction | PLANNED / A — NOT STARTED | R-XV6 | Reproduce a bounded kernel mechanism and inspect processes, memory, files and recovery. |
| J-CAP03 / P13 | Networked distributed service | PLANNED / A — NOT STARTED | R-NET, R-SRE | Build a protocol/service then measure concurrency, retries and partition behavior. |
| J-CAP04 / P07 | Storage engine and pipeline | PLANNED / A — NOT STARTED | R-SQLITE-LAB | Connect indexes, transactions, query layer, ingestion and failure recovery. |
| J-CAP05 / P11 | Secure provenance system | PLANNED / A — NOT STARTED | R-OWASP | Specify trust boundaries, integrity/authentication, audit and failure detection. |
| J-CAP06 / P15 | Closed-loop physical machine | PLANNED / A — NOT STARTED | R-ELECTRIC, R-ROBOTICS | Trace sensing/electronics/firmware/control/actuation with verified safe equipment. |
| J-CAP07 / P17 | Unfamiliar-system reconstruction | PLANNED / A — NOT STARTED | R-CRAFT | Characterize, hypothesize, instrument, reproduce and validate an unknown authorized system. |

Original resource candidates must be narrowed and attributed before reproduction. No unverified author or license may be inferred from the registry. Every materialized project carries its own attribution and quality gates.
