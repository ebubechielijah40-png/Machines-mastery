# Engineering the boundary beyond the learning loop

This project is a local deterministic arithmetic build. Before any service exists,
its useful engineering boundaries are numeric state, corpus identity and output
evidence. Validate finite losses/gradients before mutation; report invalid steps
as failures rather than silently saving a partially updated model. Record seeds,
code revision, tokenizer order, corpus/split hash, architecture and objective.
Restoring weights without the matching tokenizer can silently change semantics.

A real resumable checkpoint also needs optimizer state, step/example position and
random-generator state. Save to a new path, flush/close it, validate a round trip
and atomically publish it under a declared filesystem contract. The teaching JSON
loader neither authenticates an artifact nor stores a complete training state.
Do not expose arbitrary local file loading as a remote API.

Concurrent requests cannot share a mutable forward graph or sequence cache
without an ownership rule. Bound tokens, context, dimensions, output length,
queue size and work per request. Track numerical failures, request latency and
input/output sizes separately from model quality. Input text may contain private
information even when the model weights are public. Logging everything is not a
privacy design. The [local retrieval/controller](../../16-machine-learning/retrieval-agents/README.md)
shows a small typed capability boundary, not an authenticated production service.

For performance, count nodes/operations and measure peak memory and repeated
warm timings before choosing a tensor library. Then compare an equivalent
objective and independent outputs/gradients. Faster code with shifted labels or
future leakage is a different, incorrect experiment. Deployment, robust security,
fault recovery and model-monitoring policy require additional implemented evidence.
