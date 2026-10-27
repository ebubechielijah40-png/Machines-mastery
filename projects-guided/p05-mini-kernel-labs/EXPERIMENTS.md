# Protocols, observed output and limits

## K1: Quantum overhead under a declared workload

Question: how does quantum affect useful-work fraction when switching costs one
tick? Hypothesis: on three equal jobs arriving at zero, shorter q increases
switch intervals. Fix three service-8 jobs, FCFS/RR tie rules and switch cost 1;
vary q across 1,2,4,8. Record timeline, elapsed ticks and useful ticks.
The [phase experiment](../../05-operating-systems/code/experiment.py) actually
executes this deterministic model: useful service remains 24 while elapsed is
47,35,29,26 in those q cases. Fractions are 24/47, 24/35, 24/29 and 24/26.
Those values follow from this model's discrete switch rule; they are not measured
host context-switch overheads. A different arrival pattern can change the trend
for a particular metric, so do not generalize one workload to all scheduling.

## K2: Cached translation and access authority

Fix mapping VPN 2 → PFN 7, permissions r. Access 45 twice, then write 45, then
read 64. Predict miss/125, hit/125, PROTECTION, NOT_PRESENT. Run the CLI through
`code/experiment.py`; [evidence/observed.json](evidence/observed.json) contains
exact input bytes, SHA-256, command, stdout, stderr and exit code. An actual
Python process executed the model, but no hardware page fault was reproduced.

Alternative explanations for an unexpected PA include a wrong offset split,
wrong PFN, stale cache or an invalid oracle. Inspect those state elements
separately. Follow up in your learner model by remapping VPN 2 to PFN 9 after
warming: address 45 must become 157 on a miss. Remove invalidation intentionally
and preserve the stale-result counterexample in a separate record.

## K3: Model/host evidence boundary

Run `python 05-operating-systems/code/experiment.py` and identify which record
uses real descriptors and which is a model. The host runs compare duplicated
versus separately opened file offsets, pipe EOF with an extra writer, and child
cwd/status. Its [protocol](../../05-operating-systems/EXPERIMENTS.md) contains
controls, actual results, alternative explanations and limitations. A real file
observation supports the descriptor semantics on that host; it does not verify
the model's scheduler or your host's page-table walk.

A lab report must retain expected and actual results separately, include the
environment and exact inputs, explain a counterexample, and state what was not
measured. Repeated deterministic outputs verify reproducibility of the stated
model; they are not independent physical observations.
