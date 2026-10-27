# Networking: executable entry path and remaining scope

Start with [From bytes to messages](stream-boundaries/LESSON.md). It teaches why a stream lacks application message boundaries, derives a bounded incremental decoder, traces split/coalesced prefixes, defines clean/truncated EOF and terminal failures, and exercises real local socket partial I/O and backpressure. It contains a proof of its pending-buffer bound and distinguishes that bound from total memory use.

Then build the [one-request HTTP subset](../projects-guided/p06-http-server/README.md). Entry gate: explain the decoder state invariant and why retrying a whole message after a partial send duplicates bytes. The HTTP project changes the framing grammar, forcing byte-level header parsing, exact response lengths, an absolute header deadline and connection ownership under exceptions. Its rejected features and lack of general HTTP conformance are explicit.

Next connect the decoder to the [authenticated provenance experiment](../security-cryptography-mastery/provenance/LESSON.md). This demonstrates why syntactically complete messages still require identity, authorization and replay state. It remains a local synthetic model; it does not deploy a network service or claim TLS protection.

Every stage provides worked examples, executable code, recorded actual observations, exercises, hints and separated solutions. Reconstruct the stage from memory and pass independently written boundary vectors before moving onward. Use the linked source maps to see which claims come from inspected specifications and which observations were executed locally.

Coverage remains PARTIAL. Addressing/subnets, routing, UDP datagrams, DNS recursion/caching, TCP congestion/retransmission and TLS handshakes do not yet have comparable self-contained implementations and experiments here. The local socketpair observations establish stream-interface behavior in the recorded environment, not IP packet behavior or Internet performance.
