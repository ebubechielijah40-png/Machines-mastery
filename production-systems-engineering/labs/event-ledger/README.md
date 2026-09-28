# Build, measure, cache, break: a local event ledger

Runnable teaching prototype, not a production payment system. Learner NOT STARTED. A record has an event identity, account and integer amount. Repeated identical events should have one effect; the same identity with a different payload must be rejected. Queries total amounts by account. This realistic pattern exposes retry, persistence, query cost and stale-cache problems without external services or real data.

First study [prerequisite bridge](PREREQUISITE_BRIDGE.md), [design](DESIGN.md), then predict baseline behavior. Implement an independent variant before relying on `service.py`. Requirements: Python 3.10+ with standard sqlite3, Linux for recorded RSS units. No package installation, network or credentials. Run from repository root:

```sh
python3 -m unittest discover -s production-systems-engineering/labs/event-ledger/tests -v
python3 production-systems-engineering/labs/event-ledger/benchmark.py --rows 1000 100000 1000000 --output /tmp/my-ledger-benchmark.json
```

The output path must be new; existing measurements are never overwritten. Dataset files are temporary and bounded; a million synthetic rows is a local workload, not a million users. The run emits raw timing samples, query plans, insertion/index cost, storage and process high-water RSS. Code style is four spaces, tests use unittest. Inspect [benchmarks](BENCHMARKS.md), [failures](FAILURES.md), [scaling stages](SCALABILITY.md), [observability](OBSERVABILITY.md) and [security](SECURITY.md).

Practice: compute an account total by hand; predict retry and conflict outcomes; explain zero-row totals; identify the cache key; distinguish durable state from cache state (five basic). Design invalidation, a rollback test and a two-instance stale-read reproducer (three intermediate). Hard: propose an atomic cross-instance cache/version contract without claiming this prototype implements it. Experiment: measure scan → index → cache, inject stale state, restore correctness and explain where caching is wrong. Solutions are demonstrated by source/tests only after your attempt; no learner results exist.
