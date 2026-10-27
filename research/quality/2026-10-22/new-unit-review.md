# Independent review — numerical foundation and quality auditor

Reviewed 2026-10-22 by the independent audit agent, separate from the implementation author. Actual files were read; focused tests, deterministic experiment replay and adversarial probes were executed. No implementation edits were made by this reviewer. This record describes the pre-remediation versions below; later fixes need their own execution evidence.

## Inspected scope and fingerprints

- `tools/quality_audit.py`: SHA-256 `bacb45b37521110cd233a3e77bae89e3472342f825f23e0256d64c11b0af8ac4`.
- `tools/tests/test_quality_audit.py`: SHA-256 `7d251ea8bb4d62bf9f1c3c6502053abdb1e2404235f74a8d75992a0671ad3c8b`.
- `foundations/mathematics/change-error-and-evidence/numerics.py`: SHA-256 `c797c60336568f8e8a2aa54cb720714f3d70ec3789e9eada8cb89e052f74fff8`.
- `test_numerics.py` in that unit: SHA-256 `f1427aeb752d8c8e2e5a9f928d3071775f1c373a1e2105ae80c4160470f75102`.
- Unit `README.md`: SHA-256 `c79c59c349b9c92a681e3da53ff7237eb5882d1a61a0a820555f5229debf714a`.

Also read the unit experiment, stored observation JSON, exercises, hints, solutions and sources. Primary external sources were not independently reopened in this code/lesson review; source verification claims remain the authoring agent's scoped records. Reviewed arithmetic derivations against the stated models rather than inferring correctness from filenames or test counts.

## Executed checks

From repository root:

```sh
python3 -m unittest discover -s tools/tests -p 'test_quality_audit.py' -v
python3 -m unittest discover -s foundations/mathematics/change-error-and-evidence -v
python3 foundations/mathematics/change-error-and-evidence/experiment.py
```

Actual results: auditor **7 tests passed**, numerical unit **10 tests passed**, experiment **exit 0**. Parsed experiment output matched `observed-2026-10-22.json` exactly, including recorded environment. This establishes reproducibility of that deterministic software experiment in the present environment, not physical measurement or statistical coverage on unseen distributions.

Adversarial probes below were run in a Python subprocess. Temporary auditor fixtures used `TemporaryDirectory`; no arbitrary educational snippets were executed. The tests pass while these previously uncovered defects remain, demonstrating why the fixed suite is insufficient alone.

## Numerical API findings

### F-N1 — avoidable intermediate range failure in uncertainty propagation

Severity: substantive correctness defect for accepted finite inputs. `speed_uncertainty` computes the time contribution as `-d*ut/(t*t)`. Squaring t can underflow/overflow even where speed and uncertainty are representable. This can silently erase uncertainty, not merely raise a clear unsupported-range error.

| Actual probe | Actual output | Independently calculated time contribution magnitude |
| --- | --- | --- |
| `speed_uncertainty(1e-200,1e-200,0,1e-202)` | `ZeroDivisionError: float division by zero` | `(d/t)*(ut/t) = 0.01` |
| `speed_uncertainty(1e200,1e200,0,1e198)` | `ValueError: uncertainty must be finite` | `0.01` |
| `speed_uncertainty(1e160,1e160,0,0.01)` | `(1.0, 0.0)` | `1e-162`, representable in binary64 |

For these examples the equivalent ratio factorization `-(d/t)*(ut/t)` avoids the intermediate squared-time failure. It is not a universal overflow cure: the function should still state accepted numerical range and reject nonrepresentable intermediates clearly. Add these cases and ordinary covariance/unit cases as regression tests. A positive final standard uncertainty must not silently become zero solely because an unnecessary intermediate overflows.

### F-N2 — sum overflow can reject a representable summary

Severity: documented numerical-range limitation that should be explicit at the API. `summarize([1e308,1e308])` raises `OverflowError: intermediate overflow in fsum`, even though mean `1e308`, variance 0 and SEM 0 are representable. `summarize([1e154,-1e154])` also raises intermediate-overflow error; the latter variance is outside binary64 range, so rejection is appropriate, but the exception policy differs from the deliberate `ValueError` checks elsewhere.

The lesson already states two-pass/`fsum` range limits, so this is not an unsupported completeness claim. Either improve scaling for finite representable summaries or explicitly document/normalize the failure contract. Do not promise arbitrary finite input support solely because each input passes `isfinite`.

### F-N3 — distinguish target from population mean in sample variance derivation

Severity: explanatory ambiguity requiring a small correction. The model uses `x_i=μ+b+e_i`, where μ is the target and b a common offset. Later the variance derivation expands around μ and says the two expectations are `nσ²` and `σ²`. With b nonzero, they are `nσ²+nb²` and `σ²+nb²`; the bias terms cancel. The final unbiased-variance conclusion is correct, but the displayed justification silently changes μ's meaning.

Use population mean `m=μ+b` in the derivation, or retain μ and explicitly show cancellation. This reinforces the unit's important point that repeatability does not identify common bias.

### Numerical strengths and bounded limits

The unit supplies an actual progression from interval velocity to derivatives, a complete quadratic/cubic expansion, finite-step error, representability rejection, sample variance/SEM, common bias and covariance propagation. The `|x|` counterexample correctly separates stable central quotients from differentiability. Exercises have separated hints/solutions and transfer to RC uncertainty. The code uses actual representable endpoint separation and explains asymmetric endpoints. Tests include exact rational variance, hand-computed uncertainties, units and metamorphic scaling checks.

This is **STRONG as a bounded original unit, pending the defects above**. It does not supply a complete calculus/statistics foundation, a certified numerical library or a confidence interval method. The experiment has one deterministic polynomial and synthetic readings; it cannot establish an error law for arbitrary functions or validate independence in real instruments.

At review time the README's `RESULTS.md` link target was absent; finite-representations prerequisite link existed. The results file may still be in active development; integration must recheck it before publishing.

## Auditor findings

### F-A1 — malformed evidence record crashes instead of producing a finding

Severity: robustness failure in the automated quality check. The completion-evidence parser catches `ValueError` and `TypeError`, but not `AttributeError` or explicit schema violations.

Actual isolated fixtures:

```json
[]
```

as `registries/quality_evidence.json` caused:

```text
AttributeError: 'list' object has no attribute 'get'
```

and:

```json
{"units": [null]}
```

caused:

```text
AttributeError: 'NoneType' object has no attribute 'get'
```

The parser should validate top-level object/list/record/field types and emit `invalid-quality-evidence` rather than crash. Add fixtures for these shapes and for source-verification records. A checker intended to find broken records must itself handle them.

### F-A2 — evidence validation follows symlinks

Severity: evidence-integrity gap. The module promises to never follow symlinks, and `owned_files` skips them. However, excellence evidence checks call `(root/p).is_file()` without containment/symlink checks; source verification does likewise for its evidence path.

Actual fixture: a regular file named `real`, a symlink `link -> real`, and an EXCELLENT unit pointing every required evidence field (`review`, `tests`, `sources`, `experiment`, `assessment`) to `link`. Actual auditor `counts` was `{}`. It emitted no unsupported-excellence or unsafe-evidence finding.

Validate every evidence path as a normalized repository-relative file; reject absolute paths, path traversal and any symlink component. Reuse one safe evidence resolver for both registries. File existence alone still cannot verify evidence truth or independence; the auditor correctly admits that broader limit.

### F-A3 — AST parsing misses Python compilation errors

Severity: incomplete invalid-code detection. A file containing only:

```python
# not runnable — invalid complete module, deliberately not executed
return 3
```

produced auditor `counts: {}` in an isolated root fixture. `ast.parse` constructs this AST, while compiling it as a module rejects `return` outside a function. Similar static context errors can involve `break`, `continue`, `yield` and invalid nonlocal bindings.

Compile the parsed code object without execution, or state that this check only catches grammar errors. The former is safe for this use and better matches the invalid-code-example requirement. Preserve explicit fragment labeling so intentional non-module snippets are not mislabeled. Add a regression fixture whose failure does not depend on executing arbitrary code.

### Parsing and scope limits

The checker explicitly acknowledges that it is not a full CommonMark parser. It removes backtick fences but does not handle the complete fenced-code/inline-code grammar; apparent links in inline code or tilde fences can be false positives. Nested parentheses and some heading/anchor syntax can also be misparsed. Keep those findings reviewable and do not imply exhaustive broken-link detection.

Project implementation/test presence checks are local-file heuristics; a fixture/helper can be mistaken for implementation, and test documentation under a `tests/` path can be mistaken for runnable tests. Source inspection truth and semantic support are not computable from a JSON status plus existing evidence file. Those limitations are acknowledged and remain important even after robustness fixes.

### Auditor strengths

The audit inventories all roots, skips source/private trees, uses explicit report-only mode, distinguishes findings from quality ratings, detects repeated substantive paragraphs rather than headings/file counts, checks reference links and maps paper dossiers to scoped inspection records. Tests deliberately probe false certification, exclusion and syntax nonexecution. This is a useful substantive improvement over the former grep/count script. It remains a **STRONG risk-inventory design with identified implementation defects**, not an automated educational-excellence certificate.

## Required follow-up before accepting this batch

1. Repair and regression-test F-N1 and F-A1–F-A3; clarify F-N3.
2. Document or improve F-N2's finite-range/exception behavior.
3. Supply/check the linked RESULTS artifact.
4. Rerun the focused suites, deterministic experiment and these exact adversarial probes. Preserve this pre-fix review; append a dated resolution record rather than deleting discovered failures.
5. Keep whole-domain mathematics classification PARTIAL and repository-wide excellence incomplete. Passing repaired tests supports only the bounded contracts exercised here.

## Independent resolution check — 2026-10-22

The author repaired the reviewed implementation and asked for the exact failing probes to be rerun. This section preserves the original failures above and records subsequent evidence without rewriting them.

Actual rerun results:

- `python3 -m unittest discover -s tools/tests -p 'test_quality_audit.py' -v`: **10 tests passed**.
- `python3 -m unittest discover -s foundations/mathematics/change-error-and-evidence -v`: **11 tests passed**.
- Numerical experiment: **exit 0**, parsed output still exactly matches the retained observation JSON.
- F-N1 probes now return `(1.0,0.01)`, `(1.0,0.01)` and `(1.0,1e-162)` respectively. The unnecessary squared-duration intermediate was removed. **Resolved for the reviewed scales**, with new regression coverage; general finite-range limitations remain.
- F-N3 now explicitly defines population mean `m=μ+b`, then expands around m. **Resolved by inspected explanation**.
- F-A1's top-level array and null unit record now each emit `invalid-quality-evidence: 1`, without crashing. Additional source-manifest array/null-record probes each emit `invalid-verification-records: 1`. **Resolved for the reviewed malformed shapes**.
- F-A2's five symlink evidence fields now emit `unsupported-excellence-claim: 5`; the new resolver rejects absolute, parent-escape and symlink paths. **Resolved for referenced evidence paths**.
- F-A3's illegal top-level return now emits `invalid-python: 1`. Inspection confirms compilation without execution is used for complete modules/examples. **Resolved for the reviewed compilation-context defect**.

Rechecked fingerprints:

| File | SHA-256 |
| --- | --- |
| `tools/quality_audit.py` | `79468e54647cd252af92849973ca03041f2e40ba5d95f0794f96ad53d9ebe803` |
| `tools/tests/test_quality_audit.py` | `74744d93da2327a43a80658f076491d23b42049fe9b9809fd7f1a4d08124c79f` |
| Unit `numerics.py` | `e8ccf223bf7e565c41f32c34839afd988e89c7a65a4cc34177fd230191c28ff0` |
| Unit `test_numerics.py` | `4ef5506d66dd453d0f16054ac1d88af89b20d887137efed4c1d96d6638be677d` |
| Unit `README.md` | `059ff37c04db1ca02a40c2f49a89da2f41f190e77f4f5989f5c3d98fba39b77c` |

Remaining integration checks: F-N2 remains an intentional documented range/exception limitation; the author will add an explicit `OverflowError` note rather than claim arbitrary finite-input support. `RESULTS.md` was still absent at this rerun. A follow-on inspection notes that manifest files themselves are opened with `.is_file()/read_text`; guard against a symlinked manifest as well as symlinked evidence to fully meet the module's non-following promise. These final documentation/path changes were not falsely reported as already inspected or executed here.

The repaired bounded numerical lesson and auditor remain STRONG within their stated scope. This review supports neither whole-domain mathematics excellence nor a repository-wide completion claim.
