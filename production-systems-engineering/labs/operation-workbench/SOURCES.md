# Inspected primary scopes and original contributions

Inspected2026-10-23. No complete book, website extraction or source figures are
redistributed. The implementation, counter workload, worked examples and finite
experiments are original repository teaching work. Public readability is not a
blanket redistribution license. Rights to reproduce the original books/websites
were not independently established; consult their own terms for such reuse.

| Source / authors or publisher | Exact inspected scope | Supported claim boundary |
| --- | --- | --- |
| Chris Jones, John Wilkes and Niall Murphy with Cody Smith; edited by Betsy Beyer, Google, *Site Reliability Engineering*, chapter4, [Service Level Objectives](https://sre.google/sre-book/service-level-objectives/) | Indicators/Objectives, aggregation distributions/percentiles and standardizing measurement conditions | Distinguishing indicator, objective and agreement; measuring user-relevant outcomes and specifying latency populations; not this workload's numeric target or deployment reliability |
| Steven Thurgood and David Ferguson with Alex Hidalgo and Betsy Beyer, Google, *The Site Reliability Workbook*, chapter2, [Implementing SLOs](https://sre.google/workbook/implementing-slos/) | What to Measure: Using SLIs, event ratios/error-budget example and specification versus implementation | Good/total event framing and declared boundary; our algebra, counterexamples and finite95% target are original derived examples |
| SQLite project, [Transaction](https://www.sqlite.org/lang_transaction.html) | §§2.1–2.2, read/write transactions and BEGIN IMMEDIATE | One concurrent writer transaction and busy failures; no assertion of unlimited retries or distributed isolation |
| SQLite project, [PRAGMA synchronous](https://www.sqlite.org/pragma.html#pragma_synchronous) | OFF/NORMAL/FULL/EXTRA and WAL-specific sync discussion | Setting/reading FULL and its documented storage assumptions; local process-kill tests do not independently reproduce power-failure guarantees |
| Python Software Foundation, Python3.12 documentation, [time](https://docs.python.org/3.12/library/time.html) | get_clock_info, perf_counter/perf_counter_ns, process_time/process_time_ns, sleep | Interval clock properties, CPU versus elapsed time and scheduling limitations; nanosecond integer units do not establish accuracy |

The live3.12 documentation page identified itself as3.12.15 during inspection;
actual execution used the runtime version stored in observed.json. The Google
chapters are selected intellectual sources, not full R-SRE reconstruction or an
endorsement of this toy objective. SQLite documentation is live/unpinned; the
actual linked SQLite runtime is recorded with each observation. No primary
source is claimed to prescribe our custom key schema, capacity or fault hooks.
