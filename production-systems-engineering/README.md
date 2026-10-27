# Production systems engineering

Permanent cross-cutting track, not a final course. Prepared runnable labs: [event ledger and query service](labs/event-ledger/README.md), [distributed cluster and quorum consensus](labs/distributed-cluster/README.md), and [resilient model serving and drift guard](labs/model-serving/README.md). Broader concepts are planned in [the topic map](TOPIC_MAP.md) and [domain labs](DOMAIN_LABS.md); they are not completed courses or deployed services.

Use concept → simple example → real scenario → implementation → test → measurement → failure → debugging → scaling → production design → experiment → explanation. Every serious project needs correctness, profiling, benchmark baseline, load generation, bottleneck hypothesis, measured change, failure injection, recovery and instrumentation. No optimization earns credit without a defensible comparison.

Evidence documents: DESIGN, ARCHITECTURE, ASSUMPTIONS, BENCHMARKS, FAILURES, EXPERIMENTS, SECURITY, OBSERVABILITY, SCALABILITY, POSTMORTEMS and RESULTS. Add [ADRs](templates/adr.md) for consequential choices. Agent-run benchmark evidence is separate from learner mastery. [Engineering exams](EXAMS.md) use labeled synthetic scenarios; no invented incident is presented as an observed production failure.

[Mastery](../MASTERY.md) adds production applicability, scalability tests, failure tests and operational understanding only with actual scoped evidence. Apply gradually to languages, algorithms, OS, networks, databases, distributed systems, security/privacy, AI, hardware and embedded robotics. A Boolean simulation's operating evidence differs from that of a deployed network service; justify applicability explicitly.

## Developed operations build

After transactions and threads, build [idempotent effects/responses, finite admission, deadlines and SLO evidence](labs/operation-workbench/README.md). Use retained load/process-kill observations to derive an incident analysis and a throughput tradeoff.

Continue with [consistent backup, external receipt reconciliation, pooled histograms and a local release rehearsal](labs/operation-workbench/RECOVERY_AND_OBSERVABILITY.md). The independent review rates this bounded build STRONG while the wider frozen production domain remains PARTIAL.
