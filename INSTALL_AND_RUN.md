# Install, run and inspect quality

Extract the source archive or open the included complete Git bundle as described in
[INTEGRATION](INTEGRATION.md). Start at the repository root. Core Python teaching
mechanisms use Python3.10+ standard library, including SQLite; no pip install,
external service, account or dataset download is needed for the reference replay.
Controlled tests use temporary local files, child processes and local sockets.
Review locally trusted code before executing it.

```sh
python3 tools/verify_repository.py --report-dir research/quality/local-replay
python3 tools/quality_audit.py --json research/quality/local-content-audit.json --report-only
```

The replay saves exact commands, exit codes and logs, rejects zero-test discovery,
and records unavailable optional tools as BLOCKED. Git whitespace checks need a
Git checkout, so both are BLOCKED for the source archive. PASS describes the
specified contract; it never certifies a full educational domain.

| Optional lab | Required local tools and actual scope |
| --- | --- |
| C byte parser and byte arena | C11 cc/GCC/Clang with undefined-behavior sanitizer support; O0/O2/UBSan builds |
| Compile/link observation | C compiler plus nm, objdump and readelf from a compatible native toolchain; selected ELF observations reflect the tested platform |
| C synchronization | C11 threads.h and thread library/compiler support, including pthread linking on the tested Linux host; defined atomic/lock/condition operations |
| C++ lifetime | g++ with C++17 and undefined-behavior sanitizer support; O0/O2/UBSan builds |
| Bash arguments | bash available through PATH; argv observations are shell-specific |
| RISC-V assembler comparison | riscv64-linux-gnu-as; arithmetic/model tests run separately without it |
| SystemVerilog register/FIFO | iverilog12.0 and vvp observed; finite simulation and intended mutants, not synthesis/timing |
| VHDL FIFO | GHDL4.1.0 with VHDL2008 support observed; finite queue contract and intended mutants |
| Rust ownership | rustc1.99.1 observed, edition2021; debug/optimized tests and intended compile rejections |
| Zig allocation/error unit | Zig0.13.0 required; newer APIs are not silently treated as compatible |
| Go cancellation | Go1.27.3 observed plus a native C toolchain for race-detector support; no third-party modules |
| Java objects/resources/threads | JDK17 compiler and jdk.jdeps modules; run.py can use java modules when javac/javap launchers are absent |
| Binary reconstruction | C11 cc plus UBSan, original local target compiled into a temporary directory |
| Git whitespace | git and repository metadata; source archives have no Git history |

The integration environment's recorded versions are evidence, not a portability
guarantee. A present compiler can still lack C11 threads, sanitizer or binutils
support; retain the actual failure instead of treating tool discovery as success.
Unit-local README/SOURCES files define narrower algorithm, platform and input
bounds. Physical hardware, biological assays, quantum hardware and production
deployments are not validated by these synthetic runs.

For selected groups:

```sh
python3 tools/run_reference_tests.py
python3 -m unittest discover -s tools/tests -v
python3 tools/validate.py
python3 tools/render.py --check
python3 tools/validate_expansion.py
```

The content inventory intentionally has outstanding findings. Omit --report-only
to use the strict nonzero risk gate. The auditor parses/compiles Python without
running arbitrary snippets and checks common internal links, repeated text,
public project bindings, source/assessment/experiment evidence and contradictory
completion claims. Its heuristics need qualitative review and cannot establish
scientific truth, source rights or learner mastery.

Read [the current test report](research/quality/2026-10-23-zip/TEST_REPORT.md) for actual
executions and [the final window audit](FINAL_EXCELLENCE_AUDIT.md) for incomplete
domains. Learner study begins at [START_HERE](START_HERE.md) and follows
[the progressive route](STUDY_ROUTE.md), with predictions and unaided attempts
recorded separately from development evidence.

## New experiment replay and tool provenance

```sh
python3 tools/replay_expansion_experiments.py --report-dir research/quality/local-experiments
```

This replays ten trusted synthetic expansion experiments and retains fresh JSON,
stdout,stderr and commands. It includes a native local C oracle, local SQLite
transactions, direct-child process kills and temporary files; review its code
before executing. It never downloads data/tools or writes to a remote service.

Native tools are found through PATH. Rust/Zig/Go unit runners also accept their
documented --compiler or environment variable overrides when run directly. Use
a trusted compiler installation suitable for your OS/architecture; this source
archive does not install system packages. Exact observed versions and package/
archive hashes are retained in research/quality/2026-10-23-zip. Ubuntu packages
were checked against HTTPS package-index SHA256, without independent Release
signature verification; language archive provenance comes from the actual fetch
record. These are transparent execution records, not a general software supply
chain certification. Native compilers stay outside the repository and ZIP.

The recorded C/C++/RISC-V/HDL/Rust/Zig/Go/Java executions all passed in this
window. A missing or incompatible optional tool on your host remains BLOCKED.
No tool path is hardcoded to the development workspace or historical /tmp layout.

## Optional protected-history dependency and native checkpoint

Core portable reference groups use Python standard library. Protected encrypted
history is a separately gated optional group requiring cryptography50.0.2:

```sh
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install -r security-cryptography-mastery/provenance/requirements-protected.txt
python3 security-cryptography-mastery/provenance/run_protected.py
```

The pinned runner reports BLOCKED, exit2 if the dependency is absent or has a
different version. It does not silently pass. The new database locking/publication
lab needs a local POSIX filesystem. Native ABI/ELF investigation additionally
needs Linux x86-64 and cc/readelf/objdump/nm. Tool distributions and private source
originals are excluded from the ZIP; exact execution versions are in its reports.
