# Engineering investigations, not buzzword exams

All scenarios below are synthetic assignments, not observed incidents. An assessor must provide internally consistent code/log/metric/query fixtures before claiming an executable exam; only the ledger's cache scenario currently has runnable evidence.

1. API latency changes from 80 ms to 2 s. Require traffic/window/percentile definitions, request correlation, query plan, pool wait and dependency latency. Propose competing explanations and a test that distinguishes them; do not jump immediately to caching.
2. Pipeline duplicates events. Use the ledger lab to separate retry delivery from effect application; show why a durable event identity and payload conflict check matter. Test retry after an uncertain response, not just duplicate arrival in one function.
3. Memory grows over 24 hours. Require retained-object/allocation evidence and bounded reproduction; a rising RSS alone does not establish a leak. Contrast caching, allocator retention and genuine unreachable resource loss.

Architecture variants: URL shortener, chat, file storage, notifications, analytics pipeline, payment ledger, search, logging, streaming, authentication, AI inference and IoT sensor service. Each submission needs requirements, constraints, traffic assumptions, data model, interfaces, security, failure/recovery, scaling, observability, deployment, tradeoffs and a tested prototype. A box diagram alone fails.

Capacity exercise: 10 million users * 20 requests/day = 200 million requests/day; dividing by 86400 seconds gives about 2315 requests/second on average. With decimal 4 KB payload, payload-only volume is 800 GB/day, about 9.26 MB/s average; a 30-day month is 24 TB before retention/compression/replication/protocol overhead. Peak multiplier is an explicit unknown, not a guessed capacity. Measure service demand on a representative workload before estimating hosts.

For any optimization, state which consistency promises survive, the expected bottleneck, what was measured, how failure is detected and how a rollback preserves data compatibility. A faster stale answer is not automatically a successful design.
