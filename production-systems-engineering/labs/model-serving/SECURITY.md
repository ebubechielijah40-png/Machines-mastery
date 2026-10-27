# Local model-serving input limits

The validator checks the expected vector length, supported numeric types, finite
values and configured range. It rejects out-of-range values; it does not clamp
them. These are in-process feature checks, not transport byte/memory limits or
a proof against all adversarial payloads. Existing tests cover selected cases.

One token bucket is attached to the whole server instance. It has no per-client
identity, authentication, synchronization or fair queue and is used only by the
single-thread experiment. It cannot justify concurrent DoS protection, starvation
prevention, model extraction resistance or safe public deployment. The unbounded
success-latency list is a known retention limit.
