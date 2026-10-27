# Operating Systems

Curriculum phase: P05 — Operating Systems. Learning state: NOT STARTED.

Artifact quality: **PARTIAL** for the domain. The learner-state label above is
not an artifact-completion claim. Start the developed
[mechanism lesson](SELF_CONTAINED_GUIDE.md), then reconstruct its
[guided workbench](../projects-guided/p05-mini-kernel-labs/README.md).
Scheduling and address translation have deterministic implementations and
independent tests; file/pipe/process sections include actual host observations.
The larger bootable-kernel, driver, synchronization and filesystem work remains
incomplete.

Use [experiments](EXPERIMENTS.md), [exercises](EXERCISES.md),
[hints](HINTS.md), [solutions](SOLUTIONS.md) and [inspected sources](SOURCES.md)
in that order. Run the connected reference checks with
`python 05-operating-systems/run_checks.py` from the repository root.


## Scope

architecture; scheduling; virtual memory; filesystems; interrupts; system calls; synchronization; kernel/user boundary.

## Entry and exit

Use the unit-level gates in [PREREQUISITE_GRAPH.md](../PREREQUISITE_GRAPH.md). Target evidence: Explain and test a small kernel change in an isolated emulator.

## Work placement

Keep subject notes here. Link implementations from [PROJECT_REGISTRY.md](../PROJECT_REGISTRY.md), measurements from [EXPERIMENT_REGISTRY.md](../EXPERIMENT_REGISTRY.md), and verified references from [RESOURCE_REGISTRY.md](../RESOURCE_REGISTRY.md). Do not duplicate book reconstructions here.
