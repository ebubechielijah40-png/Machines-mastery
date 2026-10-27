# From local evidence to operated systems

The scripts run on locally controlled data. Their deployment target is a learner's process, not an internet service. They require no secrets. Do not accept arbitrary uploaded traces or huge arrays into an exposed service without separate resource and input isolation.

## Causal logging

Clock counters need a process identity, restart epoch and a fixed-width wire policy. A restarted process reusing an identity with counter0 can violate intended uniqueness across old and new logs. Logs need authenticated origin, durable capture, schema/version handling and a stated retention policy. Timestamp sorting cannot recover uninstrumented causal channels or infer seconds. Monitor dropped records and parse failures separately from causal violations; silently dropping invalid evidence can make a false clean result.

An online total-order system needs protocol rules for missing messages, membership, acknowledgment, crashes and recovery. The offline `total_order` routine does not decide when a prefix is safe. Build and test that protocol before connecting it to scheduling, billing or external effects.

## Fourier computation

Specify sign, normalization, real/complex layout, input scale, units and sampling interval at the API boundary. A frequency index k corresponds to k/(NΔt) cycles per time unit under a declared interpretation; bins above Nyquist require the appropriate negative-frequency reading. Aliasing occurs before software can reconstruct unmeasured frequencies. Windowing changes amplitude interpretation and should have its own derivation and tests.

The reference caps arrays at4096 points, uses a copied list and creates roots. A production library may reuse plans and memory, specialize real inputs, select mixed radices, vectorize or run on accelerators. Compare mathematical results with reconciled conventions and measure allocation, latency distributions and workload-specific throughput. Do not deploy this scalar Python code merely because its asymptotic count is better than the direct sum.

## Retried task output

Logical IDs must remain stable across retries; attempt IDs identify executions. Publication must be atomic with respect to the authoritative durable state, with conflict/fencing rules after coordinator or worker restart. A backup that loses must not overwrite a later generation's output. Define cleanup and retention for temporary outputs; monitor incomplete tasks, duplicate attempts, skew and stragglers separately.

External effects need their own transaction/idempotency boundary. The experiment deliberately emits duplicate synthetic notifications. A durable outbox plus a receiver that atomically persists effect and operation ID is one design pattern to analyze; simply keeping a set in coordinator memory cannot survive a crash. This pattern is an exercise, not an implementation supplied here.

## Research operation

Pin source versions and input generators. Preserve raw measurements before analysis; retain failed runs with reasons. Use representative workloads and controls for timing, allocation and machine load. A reported result can remain scientifically useful when local behavior differs, provided the discrepancy is explained rather than hidden. [Source verification](../../research-paper-reconstruction/SOURCE_VERIFICATION_CONTINUATION.json) and [limitations](LIMITS.md) define this build's actual scope.
