# Contributing to Machines Mastery

Start with [AGENTS](AGENTS.md), [the depth standard](DEPTH_STANDARD.md) and
[the current scorecard](STRONG_PROGRESS_DASHBOARD.md). Preserve developed
instruction, public implementations and actual observations. A passing validator
does not promote a domain, a book reconstruction or a learner's mastery.

For an educational change, teach the mechanism and its prerequisites, include
worked normal/failure cases, provide progressive exercises with separated
solutions, and run the relevant implementation and experiment. Inspect the exact
primary-source scope before attributing a claim. Keep source/version/rights and
limits beside the unit; do not add copyrighted book originals or private datasets.
Do not replace an observed result with a prediction or fabricate benchmark data.

For an implementation change, run the affected public-contract tests and preserve
a failing counterexample when repairing a defect. New execution records use a
new filename or report directory. Curated scientific evidence stays in Git;
local replay output, generated binaries, caches and private files do not.

Before opening a pull request, run from the repository root:

```sh
python3 tools/check_publication.py
python3 tools/validate.py
python3 tools/render.py --check
python3 tools/strong_dashboard.py --check
python3 -m unittest discover -s tools/tests -v
python3 tools/run_reference_tests.py
git diff --check
```

Use `tools/verify_repository.py` for the additional optional native/compiler
contracts listed in [INSTALL_AND_RUN](INSTALL_AND_RUN.md). Record unavailable
dependencies as BLOCKED. Edit generated indexes through `registries/catalog.json`
and `tools/render.py`, not by changing marked generated blocks directly.

The GitHub workflow runs the portable checks on Ubuntu/Python3.12 and inventories
educational gaps without mislabeling them as a content-quality pass. It needs no
repository secrets or external service account. Its hosted execution begins only
after a push; local validation is not a claim that GitHub Actions has already run.

Push a review branch and describe the problem, resulting behavior, actual checks
and remaining limitations. Keep the original STRONG scope fingerprints and six
criterion weights unchanged. No blanket third-party or repository-wide license
is added by a contribution; preserve existing attribution and rights boundaries.
