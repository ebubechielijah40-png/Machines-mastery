# 14 — Inference and serving

Serving a language model is a scheduling, memory, and reliability problem.

## Prefill and decode

**Prefill** processes the prompt and builds internal state/KV cache. **Decode** repeatedly produces one or more new tokens. Their resource profiles differ: prefill can exploit parallel matrix work over many tokens; decode is often memory-bandwidth/cache sensitive and sequential across generated positions.

## Batching

Batching improves accelerator utilization, but requests have different prompt and generation lengths. Continuous batching dynamically inserts/removes requests rather than waiting for an entire static batch.

## Quantization

Representing weights/activations with fewer bits reduces memory/bandwidth and may improve throughput, but introduces approximation error and hardware/kernel constraints. “4-bit model” is not one universal technique; calibration, per-channel scales, outliers, and which tensors remain higher precision matter.

## Reliability

A production server needs admission control, timeouts, cancellation, bounded queues, observability, versioning, rollback, and resource isolation. Model correctness does not imply service correctness.

## Lab

Build a toy request scheduler around a tiny model. Measure latency and throughput under single-request, static-batch, and simple continuous-batch policies. Track queue wait separately from model compute.
