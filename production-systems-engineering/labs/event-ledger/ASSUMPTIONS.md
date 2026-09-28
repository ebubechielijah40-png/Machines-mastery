# Assumptions

Local Linux process; standard SQLite; known finite synthetic workload; integer event IDs; one writer for cache coherence; no real money or private records. Raw load uses bulk insertion to establish a dataset before timing queries; it bypasses the service ingestion API and must not be described as per-event API throughput. Benchmark hot keys repeat ten accounts; random/cold/write-heavy workloads need separate trials. Tests enforce input domains but do not validate arbitrary storage corruption.
