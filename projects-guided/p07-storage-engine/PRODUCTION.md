# Production reasoning from concrete failure paths

## Reliability and recovery

Expose `last_committed_id`, log byte size, replay duration, `valid_end`, incomplete-tail bytes and corruption offset to operators. A checksum alarm must stop mutation, preserve a byte copy and trigger investigation; suppressing it is not recovery. On disk-full/write/sync errors, stop the writer and reconcile unknown outcome before retrying. Test backup restoration separately from backup creation. Copying a live file without a defined snapshot boundary is not a tested backup protocol.

The baseline requests `fsync` for each batch. Group commit can share sync cost across batches, but acknowledgements must remain tied to the groups whose persistence barrier actually completed. A group failure produces multiple unknown outcomes. New-file and rename durability require namespace considerations absent from this baseline. Durability claims need tests against the chosen OS/filesystem/device settings and a defined power-loss model.

## Security

Use synthetic data in an owned local directory. The API does not defend against hostile symlinks, uncooperative writers or malicious log replacement. File permissions must be chosen by deployment code; this is not an authorization service. CRC detects accidental changes, not a determined writer. Add authenticated integrity only with key management, rollback protection and a clear trust model. Do not put secrets into the log: old values and deletions remain readable indefinitely until an independently correct retention/compaction system is built.

## Performance and scalability

Start-up reads all history; lookup uses a derived in-memory dictionary. The executed scaling experiment holds live keys fixed while growing history by 100×. That isolates one reason startup grows despite constant logical data size. It does not measure sync throughput, contention or cold-disk performance. A production experiment would separately measure write latency distributions, durability mode, replay time, memory, storage amplification and realistic batch sizes. Keep a correctness oracle while optimizing.

## Concurrency and deployment

No multi-user service should wrap this object without adding enforceable ownership. A mutex protects cooperating threads in one process; an OS lock can coordinate cooperating local processes; neither is distributed consensus. The current code has no locking implementation. Prefer a supported database for actual application deployment; use this engine as an inspectable lab.

A release protocol would need format/version compatibility, migration rollback, configuration validation, operational diagnostics, tested restore, disk capacity alarms, resource limits, request deduplication and incident procedures. The exercise's successful tests are evidence for its stated model only.
