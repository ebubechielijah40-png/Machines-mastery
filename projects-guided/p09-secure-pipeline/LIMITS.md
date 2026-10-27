# Security boundary and known gaps

Single-writer local caller ownership, configured secret keys, trusted reader-principal argument and an optional independently retained latest tip are assumptions. The experiment deliberately uses public demo keys and synthetic data. No confidentiality, remote identity, signature/nonrepudiation, protected clock or physical measurement truth is provided.

Current keys/policy verify all historical records, so rotation or policy change may prevent reopening. No historical configuration versions, multi-writer lock, hostile-path hardening, parent-directory fsync, external checkpoint transaction, backup/restore or deployment is implemented. A complete valid prefix can conceal deletion without a trusted tip. Injected fsync failure models an uncertain outcome; it is not a physical power-loss test. The bounded mechanism is STRONG; the full secure-pipeline project scope remains PARTIAL.
