# SQLite index and query-plan lab

Goal: make indexing, query planning, measurement, and scaling observable using Python's standard `sqlite3` module.

Workflow: generate data → baseline query → inspect `EXPLAIN QUERY PLAN` → add index → rerun → compare → change selectivity/order → explain when the index helps or does not.

Do not hard-code benchmark results. They depend on machine, SQLite build, data distribution, cache state, and table size.
