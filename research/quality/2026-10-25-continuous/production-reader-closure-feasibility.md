# Production closure feasibility under the frozen scope

This is a concrete gap audit following implementation/review, not a replacement
curriculum. The scope fingerprint and original domain remain unchanged. Current
review recommends90.00 readiness but PARTIAL because numeric readiness and a
STRONG gate are distinct. The newly reviewed bounded operational unit is useful
and can remain independently STRONG while the domain's breadth is developed.

The frozen card names live deployment, broad observability, backup operations
and service-scale reliability as unfinished. Actual progress now includes local
process lifecycle/loopback compatibility, offline backup/restore and bounded
histogram/alert mechanisms. The following exact gaps remain feasible to develop.

| Remaining closure | Concrete locally executable build and falsifier | Honest evidence boundary | Active development/review estimate |
| --- | --- | --- | --- |
| Coherent release/environment/migration path | Pin runtime/config/schema/artifact hashes; execute old/new clients across an additive migration and rollback; reject a destructive migration with a retained old-client probe. Rehearse staged candidate promotion with a failed candidate never receiving accepted traffic. | Current mutant shares schema and tests response compatibility; it is not a schema migration or canary implementation. Local staging is feasible without a hosted product. |1–3hours,low confidence|
| Broad operational observability | Emit bounded structured stage logs, correlate request/span identities, account for dropped diagnostics, export compatible aggregate snapshots and enforce declared event-window membership. Add per-stage dependency timing and profile CPU/memory separately. A missing event or overlapping-window negative control must fail its conservation check. | Four timestamp records and histograms already work. No hosted collector, cross-host clock authority, trace exporter or complete pipeline currently exists. Standard-library local processes can teach the mechanisms. |2–4hours,low confidence|
| Service-scale operation/capacity/failure recovery | Run a separately scheduled client process against bounded multi-process service/admission with finite connections, workers and diagnostic retention. Vary demand/worker/dependency capacity and kill one direct worker while identity/receipt invariants survive. Include all eligible failures, generator lag, CPU/RSS and queue/connection populations; compare a declared correction under fixed demand. | Existing40-request thread experiment and small serial loopback drill are bounded foundations. More rows/requests alone do not close this: the composed boundary, operating decision and fault/recovery evidence must be taught. One host still cannot certify datacentre or general distributed reliability. |3–7hours,low confidence|
| Backup lifecycle and recovery-point evidence | Kill a new-generation publisher at explicit file/manifest/sync boundaries; retain incomplete generations and prove refusal. Execute a concurrent-writer snapshot schedule, verify known complete receipt sets and collect repeated restore component intervals on fixed/varied disposable datasets. | Current engine backup/restore and stale/forged-artifact refusals are implemented. No process-kill publisher matrix, independent retention policy or repeated recovery distribution has been executed. Actual power-cut/controller claims remain unverified. |1–3hours,low confidence|
| Operator reconstruction/incident transfer | Add a bounded concealed failure scenario over the composed service with a learner-owned prediction/instrumentation sheet. Grade distinguishing generator lag, dependency saturation, admission, unknown reply and stale backup using observed invariants and retained evidence. | Existing guided milestones and20 new tasks are substantive. A broader operator investigation should require new diagnosis rather than copying the reference or checking a health endpoint. |1–2hours,low confidence|

These ranges overlap: one composed service can supply release, telemetry, load
and recovery cases. They must not be added mechanically or presented as delivery
guarantees. The reader has not executed these proposed builds, so they are not
new results or completed requirements. The highest-value next operation is to
extend the already tested service boundary with bounded structured stage events
and a separately scheduled multi-process client, then use its evidence for a
capacity/failure/migration investigation. Do not replace the working core or
duplicate it merely to create another project directory.

## Available versus external prerequisites

Actual tool presence is retained in `production-reader-legacy-corrections.json`.
The active environment has Python/POSIX process and socket facilities, SQLite,
selectors, threading/executors, cProfile,tracemalloc and resource-based local
instrumentation. The reader used subprocesses,SQLite and sockets in actual tests;
presence of the other modules is not a claim that their proposed experiments ran.
Docker/Podman/strace/lsof presence or absence is recorded separately, never
assumed and never required to proceed with the standard-library builds above.

No new external permission, secret, real customer dataset or remote host is
needed for those local educational closures. There is no reason to block all
production work or unrelated feasible domains while waiting for a commercial
monitoring stack. Protected remote deployment itself needs an authorized target,
network/identity policy and credentials if such an operation is to be executed.
Those were not supplied for this repository delivery. A public deployment should
not be invented to turn a local lab into an apparent hosted-service result.

Physical host/power/controller failures need suitable independent apparatus or
an explicitly stated emulator. They can be taught analytically and modelled with
honest limitations locally; they cannot be reported as physical observations.
Whether the fixed STRONG gate ultimately requires actual external operation must
be resolved from its unchanged declared scope and evidence, not by narrowing it
after the implementation. This reader has not certified that broad gate and
does not recommend promotion on the strength of the bounded loopback batch alone.
