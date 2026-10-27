# Engineering extension boundary

The current artifact computes a deterministic bounded synthetic batch. For actual scientific ingestion, establish instrument/calibration authority, sampling metadata and consent/access rules before selecting infrastructure. Preserve raw bytes with unit/schema version and separately managed code/configuration identity. The [next project](../p09-secure-pipeline/README.md) authenticates a bounded claim and transformation but still does not establish instrument truth.

Further engineering tasks are atomic output publication, authenticated artifact manifests, resumable streaming ingestion, retention/backup verification and repeatable environment capture. Each needs a failure/recovery experiment. Scaling beyond10000 rows calls for an analysis of streaming sufficient statistics and merge invariants; the existing in-memory Fraction implementation is not a performance benchmark or production storage engine.
