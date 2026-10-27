# Project experiments

Use the [complete protocol](../../18-computational-biology/alignment/EXPERIMENTS.md), including controls, predictions, instrumentation, actual observations, alternatives, limitations, and follow-ups. Four agent-run synthetic investigations are preserved: gap sensitivity, objective/interval choice, exact finite permutation null, and time/allocation scaling.

Learner task: make your own predictions before opening the raw results; record exact commands/environment, outputs and deviations. Compare full-output and two-row score-only memory only after independently checking equal scores. An apparent speedup with incorrect output fails the experiment. Runtime and traced allocations are machine-specific; the deterministic scores and cell counts are the portable checks.

Project failure injection: in your copy, initialize global boundaries to zero, then compare unequal-length strings. Separately remove traceback reversal and explain why score-only tests can miss the error. Preserve those failed outputs with your repair. Neither failure injection nor agent observations automatically become learner evidence.
