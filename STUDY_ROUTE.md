# Connected study route through developed mechanisms

This route names actual lessons and exit tasks. It does not treat a planned topic
or an empty chapter map as prepared instruction. Study the prerequisite first,
make an unaided attempt, predict a run, implement, test, interpret failures and
reconstruct before moving to the dependent build. Author/test evidence is not
learner evidence. Broad subjects still missing depth are named explicitly below.

## Common entry

| Study in order | Exit evidence to produce |
| --- | --- |
| [Counting and units](foundations/mathematics/counting-and-units/README.md) | Convert300 ms to seconds; explain zero versus unmeasured and samples versus intervals |
| [Algebra/functions](foundations/mathematics/core/01_ALGEBRA_FUNCTIONS.md) | Solve a byte constraint and calibration; declare domains and units |
| [Python syntax to tests](02-programming/python-entry/README.md) | Rebuild a valid byte-budget function with loops, exceptions and an independent boundary test |
| [Finite words](foundations/mathematics/finite-representations/README.md) and [state/logic](foundations/mathematics/state-and-logic/README.md) | Derive a word's capacity/wraparound and one state transition |
| [Proofs/discrete models](foundations/mathematics/core/02_PROOFS_DISCRETE.md) | State an invariant, prove termination and distinguish a sequence from a set |

Python is an executable teaching medium, not a prerequisite to count or reason.
Learners may work the first equations by hand before running code. Each prepared
unit has separate hints/solutions so copying the reference is not the first step.

## Mathematical preparation for inference and dynamics

| Next unit | Required earlier concept | Exit task |
| --- | --- | --- |
| [Coordinates/complex arithmetic](foundations/mathematics/core/GEOMETRY_COMPLEX.md) | Fractions, equations, functions | Derive modulus/conjugate/reciprocal and a quarter-turn; explain radians |
| [Vectors, maps and equations](foundations/mathematics/core/03_VECTORS_MAPS.md) | Coordinates and finite sums | Construct basis columns, compose maps, solve a pivoting example and expose sensitivity |
| [Change/error/measurement](foundations/mathematics/change-error-and-evidence/README.md) | Algebra and units | Derive a secant, diagnose cancellation, distinguish sample variation from bias |
| [Calculus/optimization](foundations/mathematics/core/04_CALCULUS_OPTIMIZATION.md) | Local change and maps | Derive a chain derivative, squared-residual gradient, integral and stable Euler/update multiplier |
| [Finite probability/inference](foundations/statistics/probability-inference/README.md) | Sets, counting and algebra | Derive Bayes/binomial masses and interval coverage; break an iid assumption |
| [Initial-value dynamics](foundations/mathematics/initial-value-evidence/README.md) | Rates, integrals, vectors, units and tested Python loops | Derive a cart trajectory and stable update; independently expose energy drift and an unseen smooth pulse |

The least-squares chapter proves its candidate by orthogonality before using
calculus in the next chapter. Complex arithmetic is taught before Hermitian
norms or quantum amplitudes. This avoids requiring the learner to accept an
unwritten mathematical bridge in order to finish the current worked example.

## Machine state, C and operating systems

| Developed build | Prerequisite handoff and evidence |
| --- | --- |
| [Byte CPU](01-computation/toy-cpu/README.md) / [guided build](projects-guided/p01-logic-cpu/README.md) | Finite words/logic → trace fetch/decode/execute, flags, branch offsets and instruction faults |
| [C reading bridge](foundations/programming/c-reading/README.md) → [byte parser](programming-languages-mastery/01-c/units/01-byte-parser/LESSON.md) | Functions/bytes → pointer-length/lifetime contract and valid/rejected parses |
| [Separate compilation/linking](04-computer-systems/compile-link/README.md) | C interfaces → symbols, relocations, a failed link and actual O0/O2 output |
| [Byte arena](projects-guided/p04-memory-allocator/README.md) | C objects/pointers → split/coalesce proof and fragmentation counterexample; byte leases differ from typed malloc storage |
| [OS scheduling/translation/descriptors](05-operating-systems/SELF_CONTAINED_GUIDE.md) / [workbench](projects-guided/p05-mini-kernel-labs/README.md) | Program versus process → service conservation, mapping/protection faults, cached authority and real EOF observations |
| [Synchronization](05-operating-systems/synchronization/README.md) | State transitions and shared objects → lost-update schedules, whole critical section and predicate-based waiting |
| [Shell](projects-guided/p02-shell/README.md) | Descriptor/process lifecycle → quoted argv, live pipeline, timeout/direct-child cleanup and logical cwd |
| [C++ resource lifetime](programming-languages-mastery/02-cpp/units/resource-lifetime/README.md) | C lifetime plus the unit's C++ syntax bridge → unique ownership, independent copy, transfer and exception cleanup |

The CPU is an instruction model, not a transistor/HDL construction. Semiconductor
physics, timing/metastability, full HDL implementations, comprehensive ABIs and
kernel/drivers/filesystems remain separate unfinished subjects. Missing optional
HDL/RISC-V tools are recorded as BLOCKED executions rather than invented output.

## Algorithms and language mechanisms

[Arrays](algorithmic-problem-solving/topics/arrays/README.md) lead to
[explicit lookup/heap/rank mechanisms](algorithmic-problem-solving/mechanisms/ordered-state/README.md),
[graphs](algorithmic-problem-solving/topics/graphs/LESSON.md) and
[dynamic programming](algorithmic-problem-solving/topics/dynamic-programming/README.md), then the
[guided library](projects-guided/p03-algorithm-library/README.md). Use the proof
bridge before BFS, relaxation, low links, cuts or augmenting paths. Reconstruct
one implementation plus an independent path/cut oracle; explain the objective,
representation, returned witness, mutation policy and complexity assumptions.

For language consequences, compare [Python aliasing](programming-languages-mastery/08-python/units/objects-and-aliases/README.md),
[C++ ownership](programming-languages-mastery/02-cpp/units/resource-lifetime/README.md),
[Bash argument boundaries](programming-languages-mastery/12-shell-bash/units/argument-boundaries/README.md)
and [SQL unknown/join semantics](programming-languages-mastery/11-sql/units/null-and-joins/README.md).
Then build [the expression language](projects-guided/p10-language/README.md):
characters → tokens → precedence/associativity → syntax tree → exact rational
meaning → diagnostics. These mechanisms do not complete all14 language routes,
compiler backends or every algorithm topic.

## Observation → transmission → storage → claim

| Developed unit | Connection and exit task |
| --- | --- |
| [Incremental framing](06-networking/stream-boundaries/LESSON.md) | Byte state → every split/EOF boundary and bounded-buffer behavior |
| [HTTP subset](projects-guided/p06-http-server/README.md) | Framing/lifecycle → grammar, local socket response, rejection and deadline |
| [Scientific ingestion](projects-guided/p08-scientific-pipeline/README.md) | Units/probability → strict observations, exact transform, metadata and uncertainty assumptions |
| [Transactional WAL](projects-guided/p07-storage-engine/README.md) | Bytes/state → torn tails, corruption, commit acknowledgement and uncertain-outcome reconciliation |
| [Query/isolation](07-databases-data-systems/query-isolation/README.md) | Rows/logic → bag operators, NULLs, indexes and actual SQLite schedules |
| [Finite information](08-information-science/finite-information/LESSON.md) | Probabilities → entropy/conditional information with independent finite sums |
| [Bootstrap evidence](10-data-science/bootstrap-evidence/README.md) | Sampling model → exact resamples and a nominal-interval counterexample |
| [Authenticated provenance](projects-guided/p09-secure-pipeline/README.md) | XOR/hashes/byte contracts → HMAC, replay/access policy, lineage and trusted-tip limits |
| [Count release](13-privacy/count-release/LESSON.md) | Probability/calculus and trust boundary → ideal density proof, utility, composition and finite-sampler limits |
| [Replica reconciliation](projects-guided/p11-distributed-kv/README.md) | Events/sets → convergent keywise state, send clocks, tombstones and counterexamples |

Do not infer truth from authentication, causal effects from a query, confidentiality
from a MAC, durability from memory, or consensus from convergence. The actual
worked counterexamples make those distinctions observable. Routing/congestion,
full databases, modern protocol/PQ implementations and production privacy systems
remain unfinished scope.

## Learning models and bounded tool control

After maps, calculus and probability, derive [squared-loss fitting](foundations/mathematics/core/03_VECTORS_MAPS.md),
then [binary/local/recurrent/generative mechanisms](16-machine-learning/model-families/README.md),
then [autodiff](16-machine-learning/03_AUTODIFF_BACKPROP.md),
[attention/local derivatives/cache](16-machine-learning/labs/DERIVATION.md),
and [the trainable decoder/tokenizer](16-machine-learning/training/README.md).
Use [the neural project](projects-guided/p12-neural-net/README.md) for milestones.
Your exit evidence includes checked gradients, causal/shifted-target reasoning,
actual training, independent evaluation, leakage/shift failures and explicit
checkpoint/tokenizer state. A synthetic pattern fit is not broad language skill.

Continue to [retrieval and typed tools](16-machine-learning/retrieval-agents/README.md).
Hand-score a query, freeze relevance labels, reproduce a retrieval miss, deny an
unauthorized tool and demonstrate budget termination. This is a deterministic
controller baseline, not a learned planner. Gated recurrence, modern latent/adversarial/diffusion families,
distributed training, quantization, alignment and production learned agents still
need full units; they are not treated as implicitly completed steps.

## Physical machines, life and quantum states

| Route | Developed order and observable handoff | Remaining broad scope |
| --- | --- | --- |
| Physical/control | [Electrical quantities](foundations/physics/electrical-quantities/README.md) and [motion/energy](foundations/physics/MOTION_ENERGY.md) → [RC](hardware-electronics-mastery/02_RC_TRANSIENTS.md) → [motor/sensor/control](17-embedded-robotics/control-path/README.md) → [guided controller](projects-guided/p13-robot-controller/README.md). Derive power balance, stable stepping, saturation and bias limits | Thermodynamics, broad materials/failure, kinematics/estimation/planning, real apparatus and safe physical validation |
| Computational biology | [Molecular bridge](18-computational-biology/01_MOLECULAR_FOUNDATIONS.md) → [alignment](18-computational-biology/02_SEQUENCE_ALGORITHMS.md) → [population/phylogeny](18-computational-biology/population-phylogeny/README.md) → [integrated synthetic stack](projects-guided/computational-biology-stack/README.md). Explain biological versus model assumptions and reproduce exact finite comparisons | Broad omics, systems/structural biology, real dataset versioning and experimental validation |
| Quantum | Complex/maps/probability → [statevector measurement](20-quantum-computing/10_STATEVECTOR_MEASUREMENT.md) → [density/noise/recovery](20-quantum-computing/noise-correction/README.md) → [integrated stack](projects-guided/quantum-machine-stack/README.md). Derive tensor order, phase, projection, channel balance and a code's uncorrected error | General algorithms/QEC/compilation, hardware modalities, calibrated controls and actual quantum experiments |

## Investigation and operation

Use [hidden-state reconstruction](reverse-engineering-systems/exercises/01-hidden-state/README.md)
to distinguish observation, hypothesis, discriminating experiment and a minimal
model. Then use [the research practicum](projects-guided/p16-research-reproduction/README.md)
for causal clocks, positive-sign FFT and duplicate-task publication. Reported
paper results remain separate from these new bounded executions. Most18-domain
paper quotas and full historical benchmark reproductions remain incomplete.

[Production labs](production-systems-engineering/README.md) extend state/API
contracts into retries, faults, instrumentation and recovery. Reconstruct one
failure analysis using retained observations. A diagram, passing test or local
benchmark does not certify a deployment or a learner. Use the
[current audit](FINAL_EXCELLENCE_AUDIT.md) for precise unfinished work rather
than treating this connected route as a completion claim.

## Further connected builds

[Atoms/bonds → elastic response → instrument compliance](foundations/chemistry-materials/elastic-evidence/README.md)
requires force/energy and derivatives; its exit task separates specimen modulus
from frame compliance rather than fitting one ambiguous line.
[Carriers → transistor load line → transient → setup/hold](hardware-electronics-mastery/device-logic/README.md)
then leads to [clocked queues](hardware-description-languages/fifo-contract/README.md).
Derive which accepted push/pop changes state before translating the same contract
into either HDL. Physical timing remains a separate measurement problem.

After the expression language, [lexical binding/closures](books/crafting-interpreters/README.md)
connect static resolution to retained environments. Compare
[Rust ownership](programming-languages-mastery/03-rust/units/ownership-transfer/README.md),
[Zig allocation](programming-languages-mastery/04-zig/units/allocator-errors/README.md),
[Go cancellation](programming-languages-mastery/09-go/units/channels-cancellation/README.md)
and [Java resources/threads](programming-languages-mastery/10-java/units/objects-resources-threads/README.md)
through their actual compiler/runtime consequences, not generic syntax summaries.

After WAL/query work, [serialized page indexes](07-databases-data-systems/page-index/README.md)
connect ordering to bytes and recovery authority. After threads/transactions,
[the operations build](production-systems-engineering/labs/operation-workbench/README.md)
connects identity, queues, deadlines, metrics and controlled process failures.
After the hidden-state case, [binary-record reconstruction](reverse-engineering-systems/exercises/02-binary-records/README.md)
requires a saved hypothesis ledger and a held probe set. These are dependency
handoffs with observable exit tasks, not claims that the broader domains are finished.
