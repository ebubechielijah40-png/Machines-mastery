# 19 — Production AI systems

A production AI system is a pipeline, not a model file.

```text
request → auth/rate limit → preprocessing → model/retrieval/tools
→ postprocessing/validation → response
            ↘ logs/metrics/traces/evaluation
```

## Operational metrics

Track at least request rate, queue time, prefill/decode or model latency, token counts, error rate, timeouts, memory/utilization, cache behavior, cost, and task-quality signals. Tail latency matters because users experience slow outliers, not averages.

## Versioning

Version model weights, tokenizer, prompt/system policy, retrieval index, tool schemas, preprocessing, and evaluation suite. A model rollback can still fail if the tokenizer/index/schema changed incompatibly.

## Deployment experiment

Serve a tiny local model or deterministic stand-in behind an HTTP API. Add bounded queues, request IDs, structured logs, health checks, metrics, timeout/cancellation, and a basic load generator. Increase concurrency until saturation. Identify whether latency comes from queueing or compute.

## Postmortem scenario

A new retrieval index improves offline answer accuracy but production p99 doubles and timeout rate rises. Investigation must connect deployment change → index size/lookup → queueing/model context length → resource saturation. “The model got slower” is not a root cause.
