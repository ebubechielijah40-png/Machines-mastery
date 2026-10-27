# Dean and Ghemawat (2004): a task can execute twice while its output counts once

Jeffrey Dean and Sanjay Ghemawat, **MapReduce: Simplified Data Processing on Large Clusters**, OSDI 2004. The inspected [author-institution PDF](https://research.google.com/archive/mapreduce-osdi04.pdf) is labeled “To appear in OSDI 2004.” Source **DG04** in the [inspection record](../../SOURCE_VERIFICATION_CONTINUATION.json) records its hash, access and exact sections. This unit writes original explanations and code; it does not distribute the paper or Google's implementation.

**Scope: STRONG for the bounded programming/fault-semantics unit; PARTIAL for the full paper and data-systems research domain.** The terabyte experiments are reported findings, not local reproductions. The in-memory reconstruction isolates task-output acceptance and cannot make claims about a real cluster.

## 1. Historical context

The paper describes large data transformations across unreliable worker machines. DG04 sections 1–2 motivate an interface that lets programmers express record processing while a runtime handles partitioning, scheduling and failures. The historical achievement combines an interface with an operational system; implementing a pair of higher-order functions alone does not reconstruct the system.

## 2. Unresolved problem

How can a job recover from a slow or failed worker without requiring each application programmer to implement distributed coordination? A retry repeats work. If the runtime blindly adds every completed attempt to a result, a correct deterministic map function can still produce an incorrect final answer.

## 3. Why the problem matters

In the original miniature dataset, shard s0 contains `red red`; shard s1 contains `blue`. The sequential result is `{red: 2, blue: 1}`. A backup of s0 computes the same output again. Summing all three completions gives `{red: 4, blue: 1}`. The error is an identity mistake: the system counted execution attempts as logical input shards.

## 4. Previous approaches

Application-specific distributed programs can arrange transfers and retries directly, but must repeatedly solve the same failure problems. DG04 draws on map/reduce programming idioms while exposing intermediate key/value records and a cluster runtime. Its discussion of prior systems does not establish that the interface invented functional mapping or all forms of parallel reduction. Their original papers have not been independently reconstructed here.

## 5. Limitations of manual handling

An application may work on a clean run and fail when one message is retried. It may assume a map output remains available after its worker dies, or publish a partly written reduce file. These failures concern ownership, publication and storage lifetime. They cannot be repaired by adding more arithmetic tests to the map function.

## 6. Research question

Can a restricted dataflow make task retries, distributed grouping and deterministic outputs manageable, while retaining useful cluster throughput? Separate the correctness question from the throughput question: a single-process oracle can investigate the former for a bounded model, whereas the latter needs matching storage, network, placement and scheduling conditions.

## 7. Central insight

The input is divided into logical map tasks. Each map emits intermediate key/value pairs; the runtime groups values by key for reduce tasks. Execution attempts may be duplicated, but publication has task identity. In DG04 section 3.3, the master accepts one map completion, while reduce attempts use temporary files and atomic output rename. The complete failure semantics depend on those mechanisms and deterministic user functions.

## 8. Mathematical mechanism

For a shard \(S_i\), let \(m_i(w)\) count occurrences of word w. The desired result is

\[
C(w)=\sum_{i=0}^{M-1}m_i(w).
\]

If \(A_i\) attempts complete for task i, naive summation computes \(\sum_i A_i m_i(w)\). An acceptance indicator \(I_{i,a}\in\{0,1\}\), with exactly one accepted attempt per completed task, gives

\[
\widehat C(w)=\sum_i\sum_a I_{i,a}m_{i,a}(w)=C(w)
\]

**only if** every accepted attempt of task i computes the same \(m_i\). This algebra explains why retry handling and determinism are separate assumptions. If attempts generate different results, different winners can yield different answers.

## 9. Architecture and worked trace

| Completion | Logical task | Output | Publication decision | Accepted map state |
|---|---|---|---|---|
| `first` | s0 | red→2 | accept | s0→{red:2} |
| `second` | s1 | blue→1 | accept | s0→{red:2}, s1→{blue:1} |
| `backup` | s0 | red→2 | ignore duplicate task completion | unchanged |

The [local implementation](../../../projects-guided/p16-research-reproduction/code/task_publication.py) validates and snapshots each output, rejects an attempt ID that changes identity or payload, accepts the first completion per logical task, and reduces only after every task is represented. Snapshotting matters: mutating a caller's dictionary after publication must not retroactively change the committed contribution.

This model's accepted outputs remain in coordinator memory. DG04's intermediate map output lives on worker disks and must be regenerated if unavailable; the local model does **not** implement that lifecycle. In the real system, publication also depends on storage operations with defined atomicity, not a Python dictionary assignment shared across machines.

## 10. Experimental design

Question: can deterministic duplicate completions change the reduced word count? Hypothesis: aggregating attempts duplicates counts, while aggregating one accepted output per task matches a sequential oracle for any completion ordering. Hold records and tokenizer fixed; vary completion ordering, number of attempts, skipped attempts and deterministic versus nondeterministic outputs. Instrument every attempt's publication decision and both final counts. No real worker is killed: omitting a completion models a crash before publication only.

## 11. Baselines and metrics

Use an independently constructed sequential `Counter` over all original tokens as the reference. Compare exact key/count equality, number of accepted task outputs, detection of incomplete jobs, and behavior under reordered completions. Timing this small model would mostly measure Python overhead and would not test DG04's cluster throughput. The naive “sum every attempt” baseline is deliberately wrong but useful as a negative control.

## 12. Reported results versus local observations

**Reported in DG04 sections 5.1–5.5:** approximately 1800 machines; a roughly 1 TB grep workload completed in about 150 seconds. Sorting completed in 891 seconds normally, 1283 with backup tasks disabled, and 933 in a run killing 200 of 1746 worker processes. The sort used 10-billion 100-byte records, 15,000 map tasks, 4,000 reduce tasks and two output replicas. These are source-reported results under that configuration, not new measurements.

**Observed locally:** [raw publication JSON](../../../projects-guided/p16-research-reproduction/evidence/publication.json) records the original three-completion trace. The naive result is red→4, blue→1; accepted output gives red→2, blue→1. External synthetic notifications still occur twice for s0. The [tests](../../../projects-guided/p16-research-reproduction/code/test_task_publication.py) enumerate all 24 orderings of two tasks with two attempts, compare 50 seeded generated jobs against the sequential oracle, and probe invalid data and incomplete publication. See the [execution record](../../../projects-guided/p16-research-reproduction/TESTS.md) for commands and actual run evidence.

## 13. What the evidence supports

For finite deterministic word-count outputs with validated task identities, the model's accepted-output invariant makes the reduced result independent of completion order. The historical experiment demonstrates the behavior of the reported system on the reported workloads. The local model explains one mechanism behind retry semantics; it does not validate the entire historical implementation.

## 14. What it does not establish

Output acceptance does not guarantee exactly-once execution or exactly-once arbitrary side effects. If an attempt sends email before its completion loses a race, ignoring its map output cannot retract the email. Nor does this experiment establish availability, crash durability, secure isolation, performance scaling, network partition behavior or an entire distributed transaction protocol.

## 15. Limits and failure modes

A hot key can concentrate reduce work. Input partitioning does not automatically balance intermediate data. A combiner must preserve the reduction's meaning: summing partial counts works, while averaging partial averages fails when partitions have unequal sizes. Carry `(sum,count)` instead. A nondeterministic map makes winner independence fail; a dead master or lost intermediate file requires mechanisms absent from the toy model. DG04's deterministic and nondeterministic semantics in section 3.3 must not be conflated.

## 16. Subsequent developments

General dataflow engines, interactive SQL systems, streaming and modern schedulers change the computation model. Their performance or semantics cannot be inferred from DG04. Additional original papers remain **UNVERIFIED in this dossier**. A follow-up reconstruction should select one such system and state which MapReduce constraints it relaxes and what new recovery problem follows.

## 17. Reproduction requirements

The bounded model needs Python 3.10+ and no network or dependencies. Repeating the historical benchmark would require the original data-generation specification, equivalent hardware/storage/replication, load and scheduler controls, precise software versions, failure timing and repeated trials. The historical master/worker implementation is not supplied here, so the cluster result is not independently reproduced.

## 18. Implementation exercises

Implement the publication state machine before opening the reference code. Prove the one-accepted-output invariant by induction over completions. Add a shard with an empty output and explain why “published empty” differs from “not published.” Produce the unequal-size average counterexample and repair it with sufficient statistics. Then design a generation/fencing rule for a regenerated map output after worker loss; state which reducer views must be invalidated. See M1–M4 in the separated [assessment](../../../projects-guided/p16-research-reproduction/EXERCISES.md), [hints](../../../projects-guided/p16-research-reproduction/HINTS.md) and [solutions](../../../projects-guided/p16-research-reproduction/SOLUTIONS.md).

## 19. Connections

Logical task IDs resemble idempotency keys at an application boundary, but persistence and transaction scope determine their real guarantees. [Causal ordering](../distributed-systems/01_lamport_clocks_1978.md) explains why message arrival order differs from logical dependency; it does not select one authoritative task winner. The storage, transactions and distributed-systems domains teach the additional mechanisms needed to move beyond this local state machine.

## 20. Open questions

What if an accepted output becomes inaccessible? What if a task reads changing input or external time? Where does a notification join the same atomic boundary as output publication? Which key distribution makes a reducer the bottleneck? Turn each question into a new bounded model and failure injection before proposing production guarantees.
