# Logical clocks: preserve causality without inventing physical time

Leslie Lamport, *Time, Clocks, and the Ordering of Events in a Distributed
System*, Communications of the ACM21(7),558–565, July1978.
Primary [author-hosted PDF](https://lamport.azurewebsites.net/pubs/time-clocks.pdf).
See [the scoped verification record](../../SOURCE_VERIFICATION_CONTINUATION.json).
Classification: **STRONG bounded logical-clock reconstruction; PARTIAL full-paper
reproduction**. The physical-clock theorem and complete mutual-exclusion protocol
are inspected context, not locally reproduced systems.

## 1. Historical context

[SOURCE L78, pp.558–561] The paper formalizes process/message causality, assigns
logical clocks satisfying a one-way ordering condition, then constructs a total
order. It illustrates synchronization and later studies physical clocks. The
source distinguishes concurrent events from events connected by causality.

## 2. Unresolved problem

[ORIGINAL EXPLANATION] Suppose service A accepts a command and sends work to B.
B records completion. An auditor merges logs and sees completion's local counter
as1 while acceptance's is900. Independent counters are not a consistent causal
timeline. Sorting timestamp-shaped numbers cannot repair missing semantics.

## 3. Why the problem matters

If a downstream effect is shown before its upstream cause, debugging can blame
the wrong operation. More seriously, a resource scheduler could service an
effect-dependent request before the earlier request that enabled it. First define
what must be ordered; a real-time deadline and a causal prerequisite are different
contracts.

## 4. Previous approaches

[SOURCE L78, pp.558,561] A central scheduler receiving requests in arrival order
does not generally preserve the order of remote request events. [ORIGINAL]
Different network delays can reverse arrivals even when one remote request
causally preceded another. Physical timestamps require a synchronization model;
the local integer counters below deliberately do not estimate seconds.

## 5. Their limitations

Arrival order reveals something about one receiver's execution, not every remote
dependency. A single central queue is sufficient only for an appropriately weaker
arrival-order specification or with additional ordering information. Do not
reject it as universally wrong; reject a mismatch between guarantee and need.

## 6. Research question

Which event order can a message-passing system define internally, and how can
local clock rules preserve it? The important distinction is between the relation
defined by observations and a representation chosen to respect that relation.

## 7. Central insight

[SOURCE L78, pp.559–560] Local process order plus send→receive edges and
transitivity generate happened-before. Clock correctness requires
`a→b implies C(a)<C(b)`; the reverse implication is not guaranteed. [ORIGINAL]
This permits a lossy representation: useful numbers can preserve required edges
without encoding every absence of an edge.

## 8. Mathematical mechanism, derived on a complete example

Our synthetic trace has A-local events a,b, then send s of message m to B. B
receives r and performs c. C independently performs u. Generating edges are
`a→b→s→r→c`; u has no edge to that chain.

Use counters initially zero. A local/send event increments its counter. A receive
uses `max(local_counter,message_timestamp)+1`. Values are
`a=1,b=2,s=3,r=4,c=5,u=1`. All ten ordered pairs within the five-event chain have
strictly increasing values. But `C(u)=1<C(c)=5` does not create a path u→c.

Proof of the clock condition: a local edge increases by construction. A message
edge increases because receive exceeds its sent timestamp. Any causal path is
a finite sequence of these edges, and integer `<` is transitive. Checking only
the two generating edge types is enough for the proof. Our independent graph
oracle additionally enumerates all reachable pairs to test the implementation.

## 9. Algorithm and implementation choices

[Runnable original model](../../../projects-guided/p16-research-reproduction/code/logical_clocks.py)
separates trace validation, clock assignment, graph reachability and total-order
construction. Invalid duplicate event/message IDs or mismatched endpoints fail
before stamping. Undelivered sends are legal. The model receives a finite valid
delivery schedule; it does not discover network failures.

Sorting `(clock,process_name)` gives one total order consistent with causality.
It also arbitrarily orders concurrent events. Our final name tie-breaker is
redundant for valid strictly increasing per-process clocks but makes the offline
contract explicit. Sorting complete data does not tell an online process whether
an earlier unseen request is still in flight.

## 10. Experimental design

The inspected logical-clock result is mathematical; the paper does not supply a
modern throughput benchmark for this rule. The local experiment tests a bounded
mechanism claim: preserve all causal pairs while changing only receive handling.
Same trace and independent reachability oracle are controls; the receive rule is
the intervention. No physical-clock drift experiment is performed.

## 11. Baselines and metrics

Baselines are a correct timestamp rule and two deliberate faults: ignore the
message timestamp, or omit strict increment after `max`. Metrics are causal pairs
that violate `<`, not wall-clock latency. A smaller value is not an accuracy
metric unless the clock's intended semantics are specified.

## 12. Actual reported results versus local observations

[SOURCE L78, pp.560–561] Rules IR1/IR2 satisfy the clock condition, and clock order
with a fixed process tie order extends happened-before. These are reported
formal results, not numerical benchmarks. The physical-clock bound later in the
paper is outside this reproduction target.

[EXECUTED HERE] [Raw experiment](../../../projects-guided/p16-research-reproduction/evidence/causal-clocks.json)
records zero violations for the correct trace, while both deliberately broken
rules violate s→r. The ignored-message rule gives r=1<s=3; the non-strict rule
gives r=s=3. These are original synthetic observations, not the paper's data.

## 13. What the evidence supports

The derivation establishes the invariant under the declared event rules. Tests
check representative inputs, all valid interleavings of one small two-process
case and80 seeded random traces using graph reachability. This triangulates the
implementation with a structurally different oracle.

## 14. What it does not establish

Scalar clock comparison cannot establish causality in reverse, elapsed duration,
deadline satisfaction, fair scheduling, atomic broadcast or agreement after
failures. A timestamp does not authenticate an event. A malicious participant can
invent counters, and an unrecorded communication can invalidate the modeled graph.

## 15. Limitations

The original synchronization example assumes ordered eventual delivery and
additional queue/acknowledgment rules [L78,p.561]; clock tagging alone is not that
protocol. Our finite trace omits crash/restart, durable counters, wraparound,
membership changes and Byzantine behavior. Python integers do not wrap, whereas
a fixed-width wire field needs an overflow/epoch policy.

## 16. Subsequent developments

A representation carrying one coordinate per process is a natural next question:
can it distinguish concurrency? This repository does not attribute that later
development to the1978 paper. Detailed original vector-clock papers remain
**UNVERIFIED — verification required** in this dossier; they are a source-specific
research gap, not a license to infer results from their titles.

## 17. Reproduction requirements

Python3.10+ and the standard library suffice for the bounded trace experiment.
Full synchronization requires implementing the request/acknowledgment/release
protocol and specifying failures. Reproducing physical-clock bounds requires a
drift/delay model and correctly transcribed theorem premises; neither follows
from the local counter experiment.

## 18. Implementation exercises

Build the generating graph and compute its transitive closure without consulting
timestamps. Implement the counter rule separately. Remove the receive increment,
then construct a failing trace yourself. See the project's
[exercises and solutions](../../../projects-guided/p16-research-reproduction/EXERCISES.md)
for independent reconstruction and an online-ordering counterexample.

## 19. Connections

The [replication example](../../../15-distributed-systems/code/replication_sim.py)
deduplicates IDs but arrival-order writes can still diverge. Logical tagging adds
ordering metadata; it does not automatically implement a consensus protocol.
The [WAL project](../../../projects-guided/p07-storage-engine/README.md) can retain
an ordered history, but durable bytes alone do not choose a cross-process order.

## 20. Open questions

What evidence lets a process safely deliver a total-order prefix before all
messages arrive? What does a restart do to counter uniqueness? Which external
causal channel must be instrumented for an audit? Implement a bounded answer and
test a violating schedule before claiming a stronger guarantee.
