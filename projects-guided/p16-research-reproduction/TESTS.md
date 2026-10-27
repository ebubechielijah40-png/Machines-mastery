# Executed validation and rerun procedure

Executed on2026-10-23 with Python3.12.14, Linux x86-64; individual experiment records contain the full environment string. Command from the repository root:

```bash
python3 -m unittest discover -s projects-guided/p16-research-reproduction/code -v
```

**Actual result:20 tests passed.** [Unedited unittest output](evidence/test-run.txt) records test names, elapsed suite time and `OK`. Three experiment scripts were also executed to the saved [clock](evidence/causal-clocks.json), [Fourier](evidence/fourier.json) and [publication](evidence/publication.json) JSON files. This is a reference-implementation verification record, not a claim that the learner completed the project.

| Mechanism | Tests | Independent evidence and limits |
|---|---:|---|
| logical clocks | 8 | known graph closure, all valid interleavings of one small schedule,80 seeded generated traces, broken receive rules, invalid identities/endpoints and offline-order extension; finite valid traces only |
| Fourier transform | 7 | hand four-point result, direct defining sums, impulse/constant/tone, Parseval, shift, nested-loop convolution, operation count and invalid shapes/nonfinite values; float arithmetic and radix two only |
| task publication | 5 | sequential original-token oracle,24 attempt permutations,50 generated jobs, crash-before-publication omission, output snapshot/replay contracts and nondeterministic counterexample; single-process memory only |

Check a test's independence before trusting it. Clock reachability must not be inferred from clock values. Forward/inverse round-trip alone cannot establish Fourier sign. Aggregating generated map outputs alone does not independently check the original token count. Inspect the hand examples and alternative oracles, not just the count of tests.

To save a fresh run without replacing historical evidence:

```bash
python3 -m unittest discover -s projects-guided/p16-research-reproduction/code -v > /tmp/p16-tests.txt 2>&1
python3 projects-guided/p16-research-reproduction/code/experiment.py > /tmp/p16-clocks.json
python3 projects-guided/p16-research-reproduction/code/fft_experiment.py > /tmp/p16-fourier.json
python3 projects-guided/p16-research-reproduction/code/publication_experiment.py > /tmp/p16-publication.json
```

Read exit codes and the saved output. A script emitting valid JSON does not by itself prove its conclusion. Tests for actual network recovery, filesystem atomicity, security isolation, historical performance and a production privacy mechanism have **not** been performed.
