# Executed test report — 2026-10-22

Authoritative exact commands, environment, exit codes and per-suite raw logs are
in [verification/results.json](verification/results.json). Final replay: **12
command groups PASS, 2 BLOCKED, zero FAIL**. Several command groups invoke
multiple suites; these totals are not a count of independent test assertions.

| Executed check | Actual result |
| --- | --- |
| Infrastructure + new audit regressions | 57 unittest tests passed |
| Unified reference runner | 18/18 groups passed, including all original 12 groups |
| Arrays release | 20/20 problem suites passed, including new storage/complexity regressions |
| Attention | 18 tests passed, including Decimal oracle and all local-coordinate gradients |
| Numerical foundations | 11 tests passed, including independently discovered extreme scales |
| RC circuit model | 12 tests passed, including energy/invariant/step-convergence checks |
| Transactional WAL | 10 tests passed, including every byte cut, corruption and unknown sync outcome |
| Global/local alignment | 9 tests passed with independent short-path/interval oracles |
| Guided bio CLI | 4 integration tests passed |
| Quantum simulator | 18 tests passed, including independent dense action and conditional measurement |
| C parser |Compiled/executed at O0/O2 and O1 with undefined-behavior sanitizer |
| RISC-V model | 3 named model suites passed; independent assembler comparison separate |
| Hidden-state reconstruction |Test suite passed |
| Existing production ledger/cluster/serving |All three suites passed; scope remains local prototypes |
| Structural validator, renderer, expansion, Git whitespace |Passed their stated contracts |
| RISC-V assembler comparison |BLOCKED: riscv64-linux-gnu-as absent |
| SystemVerilog simulation |BLOCKED: iverilog absent |

Core Python tests use Python 3.12.14. Historical/domain-specific logs and the final
replay may execute some same reference helpers more than once; no grand unique
test total is manufactured. Assertions in legacy script-style tests are not
misrepresented as unittest-discovered cases.

The initial integrated replay passed code tests but failed Git whitespace on one
extra README blank line. [Initial results](verification-initial/results.json)
are retained; the line was removed and final replay passed. The baseline ML
unittest discovery executed zero tests; this was never accepted as a pass, and
its assert-style autodiff tests are now explicitly invoked by script.

The [content inventory](content-audit.json) still records unfinished instruction,
references, assessments and project/paper gaps. A strict content-risk command
returns nonzero; report-only exit0 writes a report. Neither source/path checks
nor tests certify conceptual completeness, physical truth or learner capability.
