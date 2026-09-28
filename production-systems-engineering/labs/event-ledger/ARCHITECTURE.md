# Architecture

Caller → validation → SQLite transaction/query → durable event table → total response. An optional OrderedDict cache sits before the query, with least-recently-used eviction. Durable rows and volatile cached totals are separate states. Metrics count reads/hits/writes/duplicates/errors. There is no HTTP server, worker pool, network replication or authentication implementation here. Two independent database connections are used only in controlled failure tests.
