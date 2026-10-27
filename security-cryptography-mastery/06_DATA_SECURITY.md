# Data security and provenance

Trace data from collection to deletion. Classify sensitivity; minimize collection; protect at rest and in transit; record transformations; separate integrity from truth. Hashes, MACs, signatures, append-only logs, and versioning can make unauthorized modification detectable, but cannot prove the original measurement was correct. Project: build a small provenance ledger where every transformation records input hashes, code version, timestamp, and parent lineage.
