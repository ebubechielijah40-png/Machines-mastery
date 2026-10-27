# Actual integration executions — ZIP window2026-10-23

The initial integrated [replay](verification/results.json) executed27 command
groups, all PASS, with no blocked toolchain and no failure. It includes61
infrastructure tests,56/56 portable reference groups, selected native C/C++/RISC-V,
Rust/Zig/Go/Java and two HDL FIFO builds. These are group counts, not a count of
individual assertions or a curriculum completion score. Final post-integration
checks and extracted-archive replay are recorded separately in the delivery receipt.

| Actual scope | Evidence and interpretation |
| --- | --- |
| Serialized B+ tree and WAL rebuild |16 tests; independent range maps, byte corruption, capacity rollback and every log cut. No durable index publication claim |
| ML families |17 tests; all parameter finite differences, exact correlation/count oracles, recurrence input derivatives, invariance, EM and rejection paths |
| Elastic evidence |10 tests; analytic derivatives, Fraction affine fits/series-parallel laws, identifiability and underflow rejection |
| Device/logic |9 tests; high-precision carrier oracle, load/RC-energy checks,65,536 byte additions and setup/hold counterexamples |
| Explicit hash/heap/tree |6 tests; thousands of independent operation histories, constant collisions, stable unorderable ties and1100-node skew |
| DP |21 suites: one shared15-test independent finite-search suite plus one local suite for each of20 distinct contracts |
| Lexical binding |12 tests; static-depth binding, shadowing, closure shared cells and invalid declarations in a supplied bounded AST |
| Operations |10 tests; transactional identity/original response, concurrent retries, deadlines/admission and exact SLO arithmetic |
| Native binary records |8 tests; native/Python differential cases, every truncation/bit mutation, independent CRC and actual UBSan build |
| Rust2021 |8 tests each debug/optimized, three intended compile failures and actual allocation/move observation |
| Zig0.13.0 |6 tests each Debug/ReleaseSafe, intended leak detection and actual allocator-budget observation |
| Go |9 tests ordinary and race-detector runs, plus go vet; finite channel/alias/cancel/join contracts |
| Java17 |15 checks in ordinary and interpreted execution, actual compiler-module and javap observations |
| FIFO in each HDL |2992 independent deque vectors plus two intended semantic mutants rejected per language |
| Retained RISC-V |9216 assembled ADDI words compared to original encoder, plus model/boundary tests; broad ISA not covered |
| Retained SystemVerilog register |1024 transitions and intended priority mutant rejection |

[Ten expansion experiments](experiments/results.json) actually reran: bond/bar/
compliance, device/timing, page shape, full WAL-cut rebuild, five model families,
explicit structures, DP, lexical binding, threaded operations/process kills and
native binary probes. Their new raw JSON/stdout/stderr are in that directory;
original unit-local observations remain untouched. In the materials case this
new run fingerprints the repaired output-underflow guard.

The exact tool records are [language downloads](language-tool-downloads.json)
and [hardware package records](hardware-tool-packages.json). Compiler binaries,
source PDFs and private inspection text are excluded from the repository.
Package SHA256 values were matched to HTTPS Ubuntu indexes; their Release
signatures were not independently checked. Language archive hashes are recorded
from the tool-fetch workstream and the native command logs retain actual versions.

PASS covers specified executable contracts. It does not certify educational
completeness, universal race freedom, storage power-failure durability, all-state
HDL proof, physical calibration, biological/quantum hardware or live deployment.
Use [the qualitative review](integration-review.md) and root domain audit with
these limitations. Missing tools on another machine must be BLOCKED, not PASS.
A plain ZIP extraction lacks Git metadata, so its two whitespace checks are
BLOCKED; restore the optional bundle to run those in a checkout.

## Strict content gate actually executed

The [strict command record](content-gate.json) returned exit1 with1775 review
findings:282 missing-assessment,384 missing-experiment,373 missing-reference
trails,119 near-empty instruction,6 placeholder instruction,600 repeated-template
occurrences and11 unverified paper dossiers. There were no broken internal links
or Python syntax findings in this final inventory. Counts increased from the
previous1699 as the inventory acquired more separated new files; this is not
evidence of an educational regression or an excellence score. Many findings
remain genuine old shallow pages; heuristics also flag separated new practice
files whose source/experiment context is in neighboring unit files. They need
qualitative adjudication, not automatic suppression or a fabricated passing gate.

## Post-integration replay

[verification-final/results.json](verification-final/results.json) records a
second actual27/27 command-group replay after removing private-tool fallbacks
and integrating the source/catalog/route changes. It again executed56/56
reference groups and61 infrastructure tests, with all selected native tools
passing. No failed or blocked group occurred in this checkout. The packaging
script was subsequently syntax-checked; its real end-to-end validation is the
fresh delivery extraction and bundle/source replay recorded in the receipt.
