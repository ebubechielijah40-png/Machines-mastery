# Observability

Record query latency samples, workload size, cache hits, read/write/error/duplicate counts, query plans, database bytes and process CPU/RSS. Associate run ID, revision/hash and configuration with results. Never infer bottleneck solely from a slow average; compare time distribution and changed work. Future request IDs/traces, queue delay, connection saturation and health checks require an actual service boundary. Query-plan text is human diagnostic evidence and may change by SQLite release.
