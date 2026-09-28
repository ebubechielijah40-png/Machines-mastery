# Experiment Workflow

See [EXPERIMENT_REGISTRY.md](../EXPERIMENT_REGISTRY.md). E-001 is a prepared protocol only. It has not run.

Use [templates/experiment.md](../templates/experiment.md). Assign a stable ID and register the path, project, phase, resources, status, observed result and evidence paths in the catalog. Define the question, hypothesis, variables, controls and stopping conditions before running anything.

`python3 tools/scaffold.py experiment E-002 experiment-slug --project J-01` prepares and registers one new protocol; choose an unused ID and meaningful slug. Review the protocol and rerender the indexes before execution.

Write predictions separately from observations. Until execution, use exactly **NOT YET OBSERVED**. After execution, retain actual raw output, commands, tool versions, inputs, seeds where relevant, timestamps and deviations. A nonzero exit or surprising result is still an observation; do not replace it with an expected result.

Store public/synthetic raw evidence under the experiment's `raw/` directory when needed. Keep private data under ignored `raw-private/`; publish only reviewed non-sensitive summaries if separately authorized. Preserve failed runs. Explain alternatives and measurement error before drawing a conclusion.

Infrastructure tests belong in `research/`, not in learning experiment results. Passing them provides no evidence about gates, CPUs or learner mastery.
