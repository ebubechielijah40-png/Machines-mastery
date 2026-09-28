# Production topic map

Infrastructure plan, not completed concept lessons. Each scope below must acquire code, a controlled failure and measured evidence before release.

## Environments And Releases

development/production separation; configuration; environment variables; secrets; dependency pinning; build systems; release/versioning; deployment; migrations; backward compatibility; rollback; canary; blue/green; CI/CD.

Assign a concrete requirement, implementation, controlled baseline and falsifying test. Tie it to the existing phase rather than waiting for a final production course.

## Observability

structured logs; metrics; timings; traces; request IDs; monitoring; alerting; health checks; profiling; dashboards; production debugging; SLI/SLO/SLA.

Assign a concrete requirement, implementation, controlled baseline and falsifying test. Tie it to the existing phase rather than waiting for a final production course.

## Load And Capacity

load versus stress; throughput; p50/p95/p99; error rate; CPU/memory/connections; bottleneck identification; capacity planning; connection pooling; resource limits.

Assign a concrete requirement, implementation, controlled baseline and falsifying test. Tie it to the existing phase rather than waiting for a final production course.

## Resilience

timeouts; retries; exponential backoff; circuit breakers; rate limiting; queues; caching; graceful degradation; fault tolerance; redundancy; replication; backups; disaster recovery; incident response; postmortems.

Assign a concrete requirement, implementation, controlled baseline and falsifying test. Tie it to the existing phase rather than waiting for a final production course.

## Validation

unit; integration; system; property-style; regression; performance; load; failure; security tests; deployment comparison; recovery verification.

Assign a concrete requirement, implementation, controlled baseline and falsifying test. Tie it to the existing phase rather than waiting for a final production course.

Testing limits: unit tests isolate a component contract; integration tests expose boundary mismatches; system tests exercise a composed workflow; property checks cover families of inputs; regression tests preserve a past failure; performance/load tests characterize a specified workload; failure/security tests challenge declared fault/threat boundaries. None proves correctness for all environments.

An SLI is a defined measurement, an SLO a target for that measurement over a window, and an SLA an external service agreement with specified consequences. Scope and denominator matter. Primary orientation: [Google SRE service-level objectives](https://sre.google/sre-book/service-level-objectives/). No contractual or availability guarantee is assigned to the local lab.
