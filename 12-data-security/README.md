# Data Security

Curriculum phase: P10 — Data Security and Cybersecurity. Learning state: NOT STARTED.

Focus here on data lifecycle protection and verification.

## Scope

principles; threat modeling; authentication; authorization; access control; cryptography; encryption; hashing; MACs; signatures; integrity; authenticity; secure storage and transmission; network, application and database security; vulnerability analysis; monitoring; incident response; forensics.

## Entry and exit

Use the unit-level gates in [PREREQUISITE_GRAPH.md](../PREREQUISITE_GRAPH.md). Target evidence: Test security boundaries of a local pipeline against an explicit threat model.

## Work placement

Keep subject notes here. Link implementations from [PROJECT_REGISTRY.md](../PROJECT_REGISTRY.md), measurements from [EXPERIMENT_REGISTRY.md](../EXPERIMENT_REGISTRY.md), and verified references from [RESOURCE_REGISTRY.md](../RESOURCE_REGISTRY.md). Do not duplicate book reconstructions here.

## Developed build

[Data identity and authenticated history](SELF_CONTAINED_GUIDE.md) lead through
scientific ingestion, typed authentication and uncertain-write recovery. Continue
with [encrypted history, key epochs and a separately remembered head](../security-cryptography-mastery/provenance/PROTECTED_HISTORY.md):
library AEAD, explicit GHASH, transactional writers, original-response retries,
signed configuration-bound receipts and actual crash/rollback investigations.
Protected remote deployment, dynamic policy, real identity/key custody and
production operation remain unfinished. Artifact preparation is not learner mastery.
