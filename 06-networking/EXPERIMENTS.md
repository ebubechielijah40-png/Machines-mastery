# Networking experiments

## Executed bounded investigations

[Stream boundaries and backpressure](stream-boundaries/LESSON.md) now has an actual socketpair experiment, environment/output JSON and boundary tests. The [HTTP subset](../projects-guided/p06-http-server/EXPERIMENTS.md) adds actual local response/framing cases. These are AF_UNIX interface observations; no TCP/IP packet behavior, Internet latency or TLS experiment is claimed.

## Further experiments, not yet executed here

1. **Message boundaries:** feed a length-prefixed decoder one byte at a time, random chunk sizes, and multiple frames at once. Explain why TCP is a byte stream, not a message queue.
2. **Backpressure:** build a local producer faster than a bounded consumer. Observe queue growth/drop/blocking policy.
3. **Timeouts:** add an artificial slow dependency and compare no timeout vs timeout+retry. Demonstrate retry amplification under failure.
4. **Concurrency:** run 1, 10, 100, then more local clients; measure throughput/latency and resource use.
5. **Failure:** restart the local server mid-request and document client-visible states.
6. **TLS concept lab:** on a local endpoint, compare trusted certificate/name/time success and controlled validation failures; never disable verification as a production fix.
