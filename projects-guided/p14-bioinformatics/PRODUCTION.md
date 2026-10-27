# Engineering decisions and production delta

## Trust boundary and failure behavior

The caller chooses a local UTF-8 file. The CLI reads at most max_bytes+1 bytes and rejects oversized input. It accepts exactly two nonempty ACGTN records with distinct full headers. It rejects positive gap scores and table requests exceeding max_cells before allocating the matrix. Inputs and names are emitted through JSON serialization, never interpolated into shell commands. There is no network access, credential, server, or automatic overwrite in the application.

Errors become argparse-style nonzero exit status and stderr, with no result JSON. Tests distinguish rejected inputs from zero-valued valid alignments. Do not treat a missing output as a valid empty local alignment. File-read errors, decode failures, invalid symbols, and resource rejection are separate observable messages. Production logs containing sample identifiers or sequences may be sensitive; the provided CLI makes no central log or retention policy.

## Provenance and reproducibility

Hash the exact bytes already read and keep the parameters in the same report. Reopening the file for a separate hash could race with an edit. Record hashes of the executed Python modules as well. These are integrity/identity aids under a local trust assumption; they do not authenticate the machine, user, source origin, sample history, or biological interpretation. Reproducible arithmetic on wrong or contaminated input remains wrong or contaminated.

## Capacity and performance

Quadratic table cells bound work, not exact bytes: Python list/integer overhead and returned table copies matter. Multiple concurrent tasks multiply memory consumption. A public service would need process isolation, byte and cell limits chosen from measurements, timeouts, bounded job concurrency, authentication/authorization appropriate to its data, cancellation and monitoring. No public service is deployed or asserted ready.

The preserved experiment uses five timing samples per size and a separate traced-allocation run. It does not estimate p99 latency or prove scalability. Optimize only after retaining score/reconstruction/oracle equivalence. A two-row score-only implementation saves memory at the cost of ordinary traceback; that is an API trade-off, not a transparent replacement for complete alignment output.

## Operation and deployment

For this local teaching CLI, use the repository checkout and Python 3.10+. Run the documented test commands, then the reference command on the synthetic fixture. Keep source revision, file hashes, command, Python/platform and raw output with any report. There is no persistent database or migration to recover. If interrupted, rerun from the input bytes and pinned code; preserve completed reports rather than pretending partial stdout is a result. Durable report storage, access control, workflow orchestration and real dataset governance are outside this bounded implementation.
