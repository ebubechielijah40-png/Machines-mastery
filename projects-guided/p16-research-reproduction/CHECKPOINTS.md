# Milestones and assessment rubric

Complete one track end to end, then transfer the method to a second. Keep predictions and failed attempts; they distinguish reasoning from copying a final output.

| Milestone | Learner work | Observable pass condition | Typical failure |
|---|---|---|---|
| A0: claim and source | identify primary version, locator, assumptions and a narrower local target | someone finds the claim and explains what the model omits | title metadata is called full verification |
| A1: hand construction | clock: six-event graph; FFT: four-point sum; publication: duplicate-attempt table | intermediate states agree with definitions before execution | clocks are used to define their own causal oracle |
| A2: first mechanism | clock: receive update; FFT: even/odd stage; publication: logical winner | one end-to-end example works using the underlying mechanism | a library or expected-answer table replaces the mechanism |
| A3: independent oracle | graph reachability, direct complex sum or original-record count | reference differs structurally from tested algorithm | forward and inverse share a sign error |
| A4: negative controls | bad receive rule; nonpower length; missing completion | invalid contracts reject and deliberate faults yield a specific counterexample | errors are swallowed and relabeled success |
| A5: controlled experiment | vary rule/size/attempt schedule; retain raw output and environment | another learner reruns and compares invariant outcomes | Python time is called a historical hardware reproduction |
| A6: discrepancy analysis | distinguish specification, implementation, source, arithmetic and environment | each discrepancy has a discriminating next test | tolerance is tuned to force the desired conclusion |
| A7: memory reconstruction | close notes, derive invariant, rewrite transition | explain why it works and one failing assumption | recall function names without a proof |
| A8: unfamiliar transfer | online delivery, linear convolution or external side effect | name the added mechanism and construct a violating case | a local property becomes a deployment guarantee |

Clock milestones continue from [proofs and relations](../../foundations/mathematics/core/02_PROOFS_DISCRETE.md) to [Lamport](../../research-paper-reconstruction/domains/distributed-systems/01_lamport_clocks_1978.md), then logging/replication. FFT milestones continue from complex roots to [factorization](../../research-paper-reconstruction/domains/scientific-computing/01_cooley_tukey_1965.md), then convolution. Publication milestones continue from logical identity to [MapReduce semantics](../../research-paper-reconstruction/domains/data-systems/01_mapreduce_2004.md), then transaction/storage boundaries.

## Rubric

| Evidence | Points | Full-credit meaning |
|---|---:|---|
| source integrity and scope | 15 | original inspected, version/locator given, unavailable evidence stated |
| derivation and hand example | 20 | intermediate steps correct; assumptions, converse and units handled |
| implementation and debugging | 20 | mechanism works; invalid inputs and a failed approach explained |
| independent verification | 20 | definition oracle and negative control; finite testing distinguished from proof |
| experiment and interpretation | 15 | predictions, controls, raw results, alternatives and limits |
| reconstruction and transfer | 10 | rebuild from memory and solve a new surface case |

Passing requires 80/100 and no missing source, derivation, oracle or evidence boundary. Fabricated observations or unsupported deployment claims require correction before any pass. This assesses the bounded project, not an entire research domain.
