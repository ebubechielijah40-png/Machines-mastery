# Bash source and evidence scope

Inspection attempts and local execution: 2026-10-23. The explanations, temporary
fixture, helper, code and assertions are original repository work. The retained
runtime is GNU Bash5.2.21, GPLv3+ as reported by `bash --version`.

- Inspected **local GNU Bash builtin documentation** using
  `bash --noprofile --norc -c 'help set'`: option flags and pipefail status rule.
  This is primary documentation supplied by the actual installed program. Its
  help text is not copied into the repository.
- Identified GNU's [Word Splitting](https://www.gnu.org/software/bash/manual/html_node/Word-Splitting.html),
  [Special Parameters](https://www.gnu.org/software/bash/manual/html_node/Special-Parameters.html)
  and [Double Quotes](https://www.gnu.org/software/bash/manual/html_node/Double-Quotes.html)
  manual pages, but repeated retrieval timed out. GNU Guix/manual and source-mirror
  fallbacks were inaccessible. **These full pages were not inspected**; do not
  interpret the links as verified source coverage. Completion of that documentary
  review is BLOCKED by retrieval in this execution window.
- Exact argument/splitting/globbing/substitution behavior and pipeline status were
  independently executed on the controlled local runtime; observed.json records
  values and environment, tests.txt records seven passing methods. Explanations
  of those observations are scoped to this declared experiment, not a formal proof
  of every Bash/POSIX expansion rule or all shell versions.

No GNU manual passages or third-party source code are bundled. NUL/process-option
limitations are stated as engineering boundaries, not newly measured results.
Add a pinned inspected manual source before assigning complete documentary
source verification to this unit or extending its claims to another shell.
