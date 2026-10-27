# Quality baseline audit — 2026-10-22

## Source of truth and preservation

Primary input: `machines-mastery-quality-upgrade-ml-v3.tar.gz`, SHA256
`ba21317dcd487d953cc7929fc378d96241a711768fdd6100335d79abf6c5ee99`.
It contains 1,638 archive members and 1,336 files, no Git metadata. The inspected
stable repository was7936e4344021f78f93a9e568c839da719cf2b35f on main, with 1,237
files. Byte comparison found 99 additions, 67 modifications and zero stable files
missing from the archive. The exact preservation inventory is
[archive-comparison.json](research/quality/2026-10-22/archive-comparison.json).

Archive content was committed unchanged, apart from the added comparison record,
as 6e4402b on local branch `development/excellence-2026-10-22` before improvements.
The GitHub integration reported push access but branch creation returned 403
Resource not accessible by integration; command-line Git had no credentials.
No remote branch/PR was created and main was not modified.

## Baseline checks actually executed

[Machine-readable results](research/quality/2026-10-22/baseline/results.json)
and [environment](research/quality/2026-10-22/baseline/environment.json) preserve
commands, exit codes, logs and tool availability.

| Check | Observed baseline outcome | What it establishes |
| --- | --- | --- |
| Structural validator | exit 0 | Declared structural/evidence contracts; known warnings remain |
| Tooling unit suite | 44 tests passed | Infrastructure regression behavior |
| Renderer drift | exit 0 | Generated index consistency |
| Expansion validator | exit 0 | Required artifact/quota declarations, not depth |
| Existing reference runner | 12/12 groups passed | Existing bounded implementations; some groups contain nested tests |
| Old depth audit | exit 1;73 pattern matches | Weak scaffold-risk signal, including false positives in status docs |
| ML code unittest discovery | exit 5, zero tests | Function-style assert tests were not discoverable by unittest; not a pass |
| Attention discovery | existing suite passed | Causal attention properties in the archive |

The autodiff script was subsequently added explicitly to the unified runner;
no zero-test execution is accepted as validation.

## Content inspection and severity

[Independent baseline review](research/quality/2026-10-22/qualitative-review.md)
inspected every major domain, smaller tracks, all 23 book entries, all 12 coursebook
wrappers and all 14 language routes. It records representative exact paths and
concrete technical defects. The per-book/coursebook record is
[book-coursebook-audit.json](research/quality/2026-10-22/book-coursebook-audit.json).

The initial new risk inventory was run against a separate snapshot of 6e4402b,
not a concurrently edited tree. Its [JSON](research/quality/2026-10-22/baseline/content-audit.json)
has 2,048 heuristic findings: 728 files sharing repeated paragraphs, 248 near-empty
instruction signals, 20 project directories without local implementations/tests,
and 12 paper dossiers lacking scoped inspection records. Categories overlap.
These are review indicators, not 2,048 proven conceptual errors or a quality score.

Severe qualitative findings:

- Nineteen phase guides ask for mechanisms/examples rather than supplying them.
- The twelve coursebooks share one generic instructional-method body.
- All fourteen language routes repeat one example across 28 topic pages.
- Only arrays has a released executable problem collection.
- Two arrays use O(n) list slices while claiming O(1) auxiliary storage;
  quickselect omits the assumption needed for an expected-linear claim.
- Opposite arrival order for same-key writes makes the tiny replica diverge;
  its independent-key test did not expose that boundary.
- Code source availability contradicts its current registry; a serving incident
  has numerical outcome claims without matching execution evidence.

## Baseline judgment and immediate work

No baseline domain was EXCELLENT. Most are PARTIAL or SCAFFOLDED; source-specific
book verification is BLOCKED by absent originals. Existing production and
reverse-engineering prototypes are STRONG within their declared local scope.
Passing structure masked substantive unfinished teaching.

The first implementation batch therefore supplies numerical/measurement
prerequisites plus five bounded mechanism/project upgrades and corrects observed
analysis/provenance defects. Final ratings remain separate from this baseline;
see [FINAL_EXCELLENCE_AUDIT](FINAL_EXCELLENCE_AUDIT.md).
