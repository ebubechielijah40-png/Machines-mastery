# Separate-reader production review —2026-10-25

Reviewer: production_reader_recovery, separate from the author of the new recovery,
telemetry, local service, release drill and instruction. This is a team review,
not an external specialist audit, user study or production certification.
No implementation or scoring registry was edited by this reviewer.

## Inspected scope

Read AGENTS.md, DEPTH_STANDARD.md, STRONG_SCOPE_POLICY.md, the unchanged production
card in registries/strong_progress.json, the prior baseline qualitative review,
the operation workbench mechanism/tests/instruction/assessment/incident record,
and the new recovery/telemetry/service/drill mechanisms, source map,20 exercises,
hints, explained solutions and experiment protocol. Also inspected representative
event-ledger, distributed-cluster and model-serving designs, assumptions, source
code, observability/scalability statements and recorded results. Selected primary
source inspection is attributed to the integrating author in RECOVERY_SOURCES.md;
this reader did not independently re-inspect each original web page.

## Actual independent probes and repairs

Run from the repository root:

```sh
python3 research/quality/2026-10-25-continuous/production-reader-probe.py
python3 -m unittest discover -s production-systems-engineering/labs/operation-workbench -v
python3 -m unittest discover -s production-systems-engineering/labs/event-ledger/tests -v
python3 -m unittest discover -s production-systems-engineering/labs/distributed-cluster/tests -v
python3 -m unittest discover -s production-systems-engineering/labs/model-serving/tests -v
```

The saved before/after JSON retains exact mechanism hashes and Python/SQLite
versions. Reader-selected operations Q(-7),R(+11),S(-4) return−7,4,0. A zero final
counter retains three identities; after restoration R's retry still returns4.
An actual direct child exits17 inside an after-commit hook before returning its
reply; a new store recovers uncertain(+6) as an identical duplicate result6.
Its newer receipt rejects the older zero-total snapshot.

The independently sorted population `[2,5,6,10,11]` yields exact selected values
2,6,11. With buckets5/10, reported bounds5/10/overflow are correct. Three unequal
disjoint shards pool to counts2/4, overflow1 and latency sum34. A ten-event window
with two bad events burns4, while a forty-event window with two bad events burns1;
the two-window rule correctly does not alert. Four bad events in the long window
give burn2 and do alert under the stated policy.

The reader found three real corruption/composition defects missed by the initial
author tests. A summary could claim good10 despite ten overload statuses; an empty
summary could retain latency sum1; aggregate could return a deadline value outside
its own validator's bounds. The author added the semantic restrictions and result
validation. `production-reader-before.json` records acceptance and
`production-reader-after.json` records rejection. These files are historical
observations, not overwritten repetitions. Root added a regression covering all
three findings. Final reader-run tests passed:25 operation-workbench,7 event-ledger,
5 cluster and5 serving tests. Those42 executions establish their stated finite
contracts; they do not establish general consensus safety, service reliability
or completeness of the production curriculum.

## Instruction and assessment judgment

The new bounded unit is substantial and technically useful. It derives cumulative
histogram pooling from indicator sums, distinguishes rank bounds from interpolation,
works through response/effect identity, exposes the main-file/WAL boundary, and
separates consistency, authenticity and freshness through an executed false-history
counterexample. The loopback mutant is a meaningful compatibility negative control:
health and final state can pass while an original response fails. Recovery-time
boundaries include startup/HTTP/shutdown explicitly, rather than presenting one
host interval as an RTO guarantee.

The20 assessments require numerical work, counterexamples, competing schedules,
migration reasoning, memory reconstruction and transfer to external job effects.
Hints and solutions are separated and provide intermediate reasons. The measured
backup, identity and histogram limits are taught rather than hidden. The code
assumes trusted immutable generations and exclusive offline destinations; it
does not solve hostile-path races or protected remote custody. The chapter says
so. Reproduction commands and original primary-source scopes are explicit.

The bounded recovery/observability/release teaching unit merits STRONG after
integration checks. This does not automatically promote the entire domain.

## Domain breadth and remaining conceptual claims

The frozen production STRONG and full-mandate scope strings are identical and
explicitly retain live deployment, broad observability and service-scale reliability
as gaps. The new actual loopback lifecycle, backup and histogram work materially
close local operational gaps. They do not reproduce protected remote deployment,
host/storage failure, sustained service-scale operation, distributed recovery or
an agreed external SLO. The old event-ledger scalability route still correctly
marks multiple deployment/worker/queue/multi-instance stages as planned. Those
remaining stages cannot become implemented because a local release drill passed.

Representative review also found legacy model-serving claims needing correction:

- `service.py::predict_batch` is a serial loop over predict. `max_batch_size` is
  stored but unused; no timed queue dispatch implements dynamic micro-batching.
- The successful-call latency list grows without a retention bound. Calling its
  percentiles rolling and claiming constant overall memory are inaccurate.
- The single-thread token bucket has no lock or fair admission queue. It does
  not establish concurrency safety or freedom from starvation.

These were reported to the author. Correcting the claims or implementing the
mechanisms is necessary before promoting the wider production domain. Existing
tests passing does not validate those untested claims. The new teaching unit is
not the source of these legacy issues.

## Criterion recommendations and gate boundary

On the current substantial instructional evidence, recommended reviewed marks are:

| Criterion | Four marks | Percentage | Reason |
| --- | --- | ---: | --- |
| Instruction |2,2,2,1|87.5|Mechanisms, worked failures and assumptions are clear; full frozen breadth remains unresolved.|
| Implementation |2,2,2,1|87.5|Real state/recovery/runtime boundaries; broader deployment builds remain unfinished.|
| Reproduction |2,2,2,2|100|Executed bounded experiments, separate oracles and meaningful negative controls, including actual repairs.|
| Assessment |2,2,2,1|87.5|Specific explained assessment and reconstruction; whole-domain progression remains incomplete.|
| Prerequisites |2,2,2,1|87.5|Named/taught links and coherent new build, with wider route still partial.|
| References |2,2,2,1|87.5|Exact selected source scopes, runtime/hash evidence and limits; broader operations source work remains.|

The mandated weighted readiness is90.00. That score is not a rating decision.
Core tests and separate-author review have passed for the inspected contracts.
This reader does **not** certify the complete frozen domain breadth from this
bounded batch. Until the legacy false mechanism claims and the fixed scope's
remaining deployment/service-scale requirements are resolved, conservative
domain classification is PARTIAL despite the improved numeric readiness.
Do not narrow the frozen scope, alter the denominator or use this unit's
STRONG recommendation as automatic domain promotion. No external permission
blocker is invented: additional original instruction/local investigation can
continue in this domain and in other feasible domains.

## Follow-up: legacy claim corrections inspected

The integrating author corrected model-serving README,DESIGN,ARCHITECTURE,ADR001,
OBSERVABILITY,SCALABILITY,BENCHMARKS,RESULTS,SECURITY and source/test descriptions.
The reader inspected their actual diff and relevant source. The documentation
now identifies serial chunking, an unused maximum-batch setting, no dispatch queue,
unbounded successful-call latency retention, success-only percentile population,
the historical empty0 convention and a global single-thread/no-fairness limiter.
The ADR labels size-or-deadline batching as proposed, not implemented. Historical
raw measurements were retained and their scope corrected rather than invented.

A fresh model-serving test execution passes all5 tests, including the renamed
serial-helper contract. The distinct log is
`production-reader-serving-reviewed-tests.txt`; exact reviewed hashes and tool
availability are in `production-reader-legacy-corrections.json`. One remaining
README navigation label still said clamping/DoS mitigation when inspected; the
reader reported it for correction to match the actual rejection/single-thread
limits. This small label does not establish any additional missing mechanism.

The substantive legacy false-completion findings have therefore been addressed
by truthful scope correction, not implementation of the former claims. The
unchanged full-domain breadth recommendation remains PARTIAL90.00. The fixed
deployment/service-scale gaps have not been waived by this correction.
