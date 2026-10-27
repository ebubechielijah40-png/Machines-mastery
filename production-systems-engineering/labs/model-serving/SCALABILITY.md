# Serial chunking and actual memory limits

The current batch helper iterates over individual predictions. Chunk size changes
Python call grouping in a finite benchmark; no accumulation queue, deadline
dispatch or batched numerical kernel exists. A throughput difference here cannot
establish a dynamic-batching or hardware-utilization gain.

Model weights require O(D) storage and the drift deque O(200D). Success latency
retention requires O(N) integers after N successful calls, and each percentile
calculation sorts O(N) values with O(N log N) work. Total memory is not constant
and out-of-memory prevention was not established.

A future batching mechanism must state both a maximum waiting population and
a dispatch deadline, bound diagnostic retention, distinguish client latency from
kernel time, and run independently controlled arrival/load trials. These are
unimplemented extensions, not results of the current serial benchmark.
