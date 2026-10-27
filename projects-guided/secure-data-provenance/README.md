# Secure data provenance: connected capstone

The runnable build now lives in the [secure-pipeline project](../p09-secure-pipeline/README.md), using the shared [authenticated provenance mechanism](../../security-cryptography-mastery/provenance/LESSON.md). Reusing one inspected implementation avoids two incompatible ledger formats. This capstone extends its scientific interpretation rather than duplicating the code.

Work in this order: [scientific ingestion and uncertainty](../p08-scientific-pipeline/README.md) → [framed message transport](../../06-networking/stream-boundaries/LESSON.md) → [authenticated transformation/history](../p09-secure-pipeline/README.md) → [privacy count release](../../13-privacy/count-release/LESSON.md). Each linked unit has an entry gate, implementation, worked example, independent tests, an executed experiment and separated exercises/solutions. Explain each gate before proceeding; reading the previous file alone is not evidence of readiness.

Capstone deliverables:

1. Identify raw-data bytes and code/configuration digests, then show why these unkeyed identifiers cannot authenticate an attacker-replaceable manifest.
2. Build the producer-MAC/processor-MAC history, explain exact rational unit conversion, and retain an externally trusted final tip.
3. Perform the mutation/replay/substitution/rollback probes in the shared experiment. Distinguish expected results from saved actual observations.
4. Sign a deliberately false synthetic measurement claim. Explain why authentication does not validate the instrument, specimen, collection method or inference.
5. Design recovery for an append with unknown outcome and a missing checkpoint. Give competing histories that available evidence cannot distinguish.
6. Reconstruct the design from memory, including what remains unsupported.

This implementation deliberately omits timestamps: an unsigned local wall-clock value would not establish trusted event time, and nondeterministic timestamps are not needed for the current exact replay invariant. Trusted time, full artifact DAGs with multiple parent hashes, key rotation, protected backup/restore and deployment are unfinished extensions. The present sequence is a linear authenticated transformation history, not a complete scientific provenance standard or confidential data service.

Assess each deliverable by another learner's independent counterexample: a replacement manifest, valid but forbidden write, copied sequence, deleted suffix, shared correction averaged incorrectly, or public fixed-seed noise. The result is STRONG as a bounded capstone path and PARTIAL against the full original provenance/security scope.
