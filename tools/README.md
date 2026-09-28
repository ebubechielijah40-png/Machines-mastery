# Local Infrastructure Tools

Requirements: Python 3.10+ standard library and Git. No package installation, network service or database is needed. Python uses four-space indentation; test files use `test_*.py` and the standard `unittest` framework.

## Commands

```sh
python3 tools/render.py
python3 tools/render.py --check
python3 tools/validate.py
python3 tools/validate.py --strict
python3 -m unittest discover -s tools/tests -v
python3 tools/fingerprint.py books/code-petzold/source/YOUR-ACTUAL-FILENAME
python3 tools/scaffold.py project J-02
```

The last two are usage examples, not claims that a source exists or that J-02 has been created. Book intake uses `python3 tools/scaffold.py book RESOURCE_ID book-slug`. Scaffolding refuses existing destinations. It creates meaningful planning prompts, never `src/`, tests, results or mastery evidence.

Prepare a new protocol with `python3 tools/scaffold.py experiment E-002 experiment-slug --project J-01`; replace the ID/slug with unused values. This registers a PLANNED protocol with NOT YET OBSERVED results. It does not execute anything. Observed records must reference non-private raw evidence under the experiment's `raw/` directory; for private data, retain originals in ignored storage and provide a reviewed non-sensitive execution record there.

## What is checked

`validate.py` checks required metadata/types, duplicate IDs, cross-references, prerequisite cycles, project document/quality gates, source fingerprints for inspected books, chapter source gates, experiment result/evidence consistency, mastery evidence requirements, knowledge-edge claim support, inline internal link destinations, whitespace and generated-index drift. It also catches unregistered project/experiment/chapter directories. It reads owned files including untracked files and excludes book originals, external checkouts, secrets/private storage and environment/build directories from general traversal. Registered inspected sources are hashed explicitly.

Normal mode fails on structural errors and reports known source/license warnings. `--strict` also fails on those warnings and is expected to fail while sources/licenses are unresolved. Neither mode proves claim entailment, scientific validity, author identity, lawful availability, license compliance or learner mastery. Markdown fragment anchors, reference-style links and arbitrary prose claims are not automatically verified; use inline links and review anchors manually. The tool is not a secret scanner.

## Maintenance

Edit `registries/catalog.json`, run the renderer and inspect changes. The renderer refuses unmarked nonempty destinations and `--check` writes nothing. Generated Markdown is a view, not another source of truth. A fingerprint records bytes only and never updates the registry automatically. Source inspection and learner assessment remain human-reviewed gates.

Tests exercise rejection paths, not just successful generation. Keep checks small and inspectable. When adding a new record kind, update schema, validation and meaningful failure tests together.

## Expansion validation and readiness

The catalog now includes tracks and prepared lesson records; validation checks their unit/resource/project/experiment links and internal bridges. Mastery vocabulary includes debugging, reconstruction, transfer and applied operational capabilities with specific criteria. Owned text validation includes C, assembly, HDL and shell files. No check awards learner evidence.

```sh
python3 tools/learning_gate.py U-CEX
python3 tools/learning_gate.py U-SVEX
python3 tools/validate_expansion.py
```

The readiness reporter returns nonzero for missing learner evidence (expected now). It follows required graph edges; humans still inspect the seven-discipline bridge and the lesson diagnostic. The expansion validator enforces exemplar artifacts, topic quotas for future completed releases and preserved baseline curriculum requirements. Test and benchmark commands are documented within each executable unit. Temporary assembler/simulator packages are not repository dependencies silently assumed installed.
