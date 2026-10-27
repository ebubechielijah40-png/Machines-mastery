# Reconstruct a research mechanism and delimit its evidence

Build a small mechanism from a primary paper, test it against an independent specification, deliberately break one assumption, and write a result another learner can check. The completed reference build includes three mechanisms. It does not claim to reproduce a historical cluster or hardware benchmark.

**Repository content: STRONG bounded project. Learner state: NOT ASSESSED.** Reading a paper or running reference tests does not complete the learner's reconstruction. Each track starts with prerequisites, develops a hand trace, builds code, measures an intervention, then transfers the invariant to an unfamiliar case.

| Track | Prerequisite | Taught mechanism | Independent check | Handoff |
|---|---|---|---|---|
| A: causal clocks | relations, graphs, induction | local counters preserve message dependencies | graph reachability without timestamps | distributed logging and online order |
| B: Fourier factorization | complex numbers, finite sums | even/odd decomposition and butterflies | direct sum, Parseval, nested convolution | signal analysis and numerical performance |
| C: task publication | maps, sums, state invariants | one logical output despite duplicate attempts | sequential count over original records | retries, idempotency and storage boundaries |
| D: analytical privacy extension | densities, triangle inequality | sensitivity-calibrated noise | symbolic likelihood ratio | contribution accounting and implementation limits |

Start with A, then C: both use identities and event traces but solve different problems. Complete the complex-number bridge before B. D is an analytical extension; there is no production privacy sampler in this project. The [research coursebook](../../coursebooks/11-research.md) connects their evidence methods.

## Problem and architecture

An experiment can agree with a paper for the wrong reason. A timestamp sorter may silently invent causal edges; a forward/inverse FFT pair may share a sign error; a retried map job may double-count records. Construct a reference whose structure differs from the tested algorithm. Keep validation, mechanism, oracle, experiment and interpretation separable enough that each can be questioned.

| Component | Files | Responsibility |
|---|---|---|
| runnable learner entry | [starter.py](code/starter.py) | expose a deliberately broken counter rule and an independent causal oracle |
| clock mechanism | [logical_clocks.py](code/logical_clocks.py) | validate events, stamp clocks, check causality and construct offline order |
| transform mechanism | [fourier.py](code/fourier.py) | positive-sign DFT, radix-two FFT, inverse, circular convolution and counts |
| publication mechanism | [task_publication.py](code/task_publication.py) | snapshot outputs and accept one attempt per task |
| tests | `code/test_*.py` | worked examples, contracts, independent oracles and generated cases |
| experiments | [clock](code/experiment.py), [Fourier](code/fft_experiment.py), [publication](code/publication_experiment.py) | emit raw JSON, controlled interventions and environment details |
| evidence | [experiments](EXPERIMENTS.md), [tests](TESTS.md) | executed results with limitations and rerun commands |

## Tools and first run

Python 3.10+ and its standard library suffice. Run from the repository root; no package installation, external dataset, GPU, account, credential or network is needed for the models. Original papers are verification references, while local worked derivations remain usable offline.

```bash
python3 projects-guided/p16-research-reproduction/code/starter.py
python3 -m unittest discover -s projects-guided/p16-research-reproduction/code -v
python3 projects-guided/p16-research-reproduction/code/experiment.py
python3 projects-guided/p16-research-reproduction/code/fft_experiment.py
python3 projects-guided/p16-research-reproduction/code/publication_experiment.py
```

The starter intentionally reports causal violations. The reference suite has 20 tests. Clock JSON records zero correct-rule violations and broken-rule counterexamples. Fourier JSON includes each timing sample and error against the direct sum. Publication JSON shows a wrong naive duplicate total and an unchanged accepted total. Timing varies between runs; causal relations, integer counts and operation counts do not.

## Build rather than copy

Work through [milestones](CHECKPOINTS.md). Copy the starter into your own working area, draw the graph and write a receive rule before opening the reference implementation. Retain your prediction before executing a trial. For the FFT, derive and hand-calculate four points before reading `fft_counted`. For publication, write an invariant and completion table before implementing a dictionary of winners.

Attempt [exercises](EXERCISES.md), then [hints](HINTS.md); [solutions](SOLUTIONS.md) are separate. Each track includes an incorrect approach, a boundary case and a transfer problem. Tests expose errors; a written argument explains why a mechanism should work beyond those inputs.

## Deliverables and evaluation

Deliver a source record with version and claim locators, an original hand trace, your implementation, independent tests, raw JSON, a discrepancy analysis, and a reconstruction written without code or notes. Separate source-reported findings from executed observations. [CHECKPOINTS](CHECKPOINTS.md) contains the rubric and observable exit gates.

For research operation, security and deployment, study [PRODUCTION](PRODUCTION.md). For constraints and unperformed work, see [LIMITS](LIMITS.md). A local mechanism result cannot be promoted to an entire-domain or historical-benchmark reproduction.
