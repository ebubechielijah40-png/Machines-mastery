# Integration review — scope and limits

The integrating agent inspected the new implementations, worked lessons,
contracts, tests and source records in the six developed areas. This is an
integration review, not an independent specialist assessment of every domain.
Independent baseline and numerical/auditor reviews are separate files.

## Findings addressed

- Numerical standard-uncertainty propagation formed t², causing overflow,
  underflow and a silent zero even with representable final answers. Reordered
  via speed×relative-time-uncertainty; independent review reran extreme-scale
  probes and new regression tests. Two-pass summary range overflow is explicitly
  documented, not claimed repaired universally.
- The variance derivation now distinguishes target μ from observed population
  mean μ+b. A synthetic offset is not removed by averaging.
- The auditor previously accepted symlink evidence, crashed on malformed record
  shapes and missed compile-invalid Python. Safe evidence-path checks, shape
  checks, compile-only validation and regression fixtures address those cases.
  Manifest files themselves are guarded against symlinks. No arbitrary example
  is executed by the auditor.
- Two arrays used input-sized slices inconsistent with stated auxiliary-space
  claims. Indexed iteration and no-slicing regressions now match the register
  model. Arbitrary-precision numeric storage remains a stated qualification.
- Deterministic final-pivot quickselect now states its quadratic worst case and
  the assumptions needed for expected-linear analysis. A counted-comparison
  test verifies n(n−1)/2 for sorted/equal adversarial inputs.
- Same-key reverse-order replication now deliberately produces different final
  values in the test. This is the deduplication model's boundary, not consensus.
- Source-availability contradictions and unsupported serving incident outcomes
  were corrected. Historical source intake/test records remain historical.
- Three RC links referred to unfinished companion files after a worker limit
  interrupted writing. The integrating agent completed its sources/experiment
  companion from inspected sources and actual stored results; no physical
  experiment was invented.

## Mechanism-level review

| Unit | Reviewed positive evidence | Remaining boundary |
| --- | --- | --- |
| Numerical reasoning | Exact polynomial/Fraction oracles, covariance/unit transformations, nondifferentiability counterexample, independent review/recheck | No arbitrary-range arithmetic, automatic differentiation or confidence-coverage engine |
| RC dynamics | Initial-condition/ODE/exponential trace, invariant/energy/convergence tests, instrument-loading and finite-step failures | Ideal first-order model; no real component/instrument validation |
| WAL recovery | Checksummed bounded frames, atomic batch application, every-byte truncation, failed-sync unknown outcome, corruption fail-closed | Single writer, no locking/parent-directory fsync/checkpointing/authentication; local controlled inputs |
| Attention | Decimal/hand oracle, all local-coordinate finite differences, causal leakage counterexample, cache/full-prefix agreement and failed-step state | Fixed untrained single head; cache context/resource isolation not implemented; no translation reproduction |
| Alignment | Derivation/traceback/tie conventions, independent exhaustive path and local-interval oracles, validated CLI/provenance and synthetic null investigation | Restricted integer linear-gap model; no calibrated homology inference, real-data benchmark or biological conclusion |
| Quantum | Dense independent action oracle, all basis CNOT directions, norm/phase/measurement tests, product/entangled and mixture distinction | Ideal pure-state postulates, exponential resources; no noise/QEC/device claim |

These findings support STRONG classifications for the bounded units after
corrections. Whole mathematics/hardware/databases/AI/biology/quantum domains
remain PARTIAL. Existing production/reverse prototypes retain their scoped
ratings; a passing mechanism test cannot validate broader operation.

## Verification interpretation

The first integrated replay passed implementation tests but found an extra blank
line in a README. Its failed whitespace output is preserved in
`verification-initial/`. The line was removed; final replay has its own
`verification/` record. A zero-test run is an explicit failure in the replay
runner. Missing optional assembler/HDL tools are BLOCKED. Content-risk findings
remain intentionally separate from executable correctness.

No member of this development process performed a full independent specialist
review of all new domain content, all remaining files, or every possible failure
schedule. Further review and implementation remain in the remediation backlog.
