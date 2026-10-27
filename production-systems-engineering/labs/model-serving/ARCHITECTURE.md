# Actual serial inference architecture

A call checks a global single-thread token bucket, validates a feature vector,
retains it in a200-vector drift deque, scales it and evaluates the logistic model.
Successful calls append an interval to the unbounded latency list. Rejections
return without a latency sample. `predict_batch` repeats this path sequentially.

Model/scaler parameters are unchanged during this inference path. Mutable
limiter, metrics, drift and latency collections are not protected for arbitrary
concurrent callers. There is no batching queue, hosted endpoint, trace exporter
or bounded lifetime telemetry pipeline. Study the operation workbench for the
separate developed admission/measurement/recovery contracts.
