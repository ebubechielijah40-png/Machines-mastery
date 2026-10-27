# Checkable solutions and debugging answers

1. `Host` and `hOsT` are the same field name after case normalization. The subset rejects any second occurrence. `Host :` is rejected because whitespace is not part of a token field name. A leading space is rejected rather than interpreted as a folded continuation.
2. `Content-Length: 0` plus `Transfer-Encoding: chunked` is rejected, not handled by choosing whichever appears first. This lab does not implement chunked bodies. A claim that it is a complete RFC 9112 parser would be false.
3. The valid request has no body. Its response body is exactly `b'ready\n'`, hence six bytes. Adding an invisible newline without updating Content-Length creates a boundary mismatch for a persistent receiver; this server closes, but should still produce accurate framing.
4. With `deadline=1.0`, first read at time .1 and next attempt at 1.1, the second read must not begin. Resetting a one-second timeout on every read would incorrectly extend the protocol's lifetime. The regression supplies a fake monotonic clock to make this distinction deterministic.
5. If recv raises ConnectionResetError before a response exists, a finally located only around send cannot close the connection. The outer finally owns the descriptor for every control-flow path. If sendall raises, it is unsafe to assume zero bytes were accepted and resend from byte zero.
6. A pure parser called with `GOOD+GOOD` rejects trailing bytes. A handler may collect only `GOOD`, parse, and close before a later second request arrives. Both are consistent with the one-request contract; neither establishes general pipelining detection.
7. Transfer exercise: adding request bodies requires an explicit body-length state machine, byte limits, chunked grammar if claiming HTTP/1.1 conformance, and rules for connection reuse after errors. Simply reading until EOF prevents a persistent peer from receiving a timely response and confuses body completion with connection termination.

Reconstruction is accepted only when the learner explains every listed boundary decision and reproduces tests with a separate literal request, not when they copy the reference implementation.
