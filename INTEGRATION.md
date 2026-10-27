# Verify and integrate the publication ZIP

The GitHub-ready ZIP is a source-only archive with repository files at its root.
Checksums, recovery history and release metadata are separate downloads or
delivery records. Nothing needs to be removed from the extracted source tree.
Earlier development ZIPs used an outer source folder plus recovery sidecars;
their historical receipts describe that older layout, not this publication ZIP.

Verify the ZIP's SHA256 against the separately supplied checksum. On PowerShell:

```powershell
Get-FileHash .\Machines-mastery-development-2026-10-25.zip -Algorithm SHA256
```

On a system with `sha256sum`:

```sh
sha256sum -c Machines-mastery-2026-10-25-zip-SHA256SUMS.txt
```

Follow [PUSH_INSTRUCTIONS](PUSH_INSTRUCTIONS.md) to extract into an existing clone
and push a review branch. The optional complete Git bundle is kept outside that
clone. Both routes preserve all instructional implementations and curated evidence.
No remote push is performed by validation or packaging tools.

From the resulting repository root:

```sh
python3 tools/check_publication.py
python3 tools/verify_repository.py --report-dir research/quality/local-replay
python3 tools/quality_audit.py --report-only --json research/quality/local-content-audit.json
```

`local-*` report directories are ignored, so ordinary verification does not add
files to your next commit. Curated historical reports and scientific observations
remain intentionally versioned. Read [INSTALL_AND_RUN](INSTALL_AND_RUN.md) for
portable versus native/optional dependencies. A source folder alone has no Git
history; use a clone or the separate bundle for Git-specific checks.

The strict educational auditor, without `--report-only`, still returns nonzero
for unresolved risks. That is distinct from publication hygiene and executable
contract tests. Neither a clean file tree nor green CI certifies all33 domains,
source licensing, physical experiments or learner mastery. Current readiness and
remaining work are in [the dashboard](STRONG_PROGRESS_DASHBOARD.md).

The original archive comparison and all preserved improvements remain documented
in [QUALITY_BASELINE_AUDIT](QUALITY_BASELINE_AUDIT.md). The publication receipt
records exact source hashes, fresh extraction, Git staging and bundle checks.
