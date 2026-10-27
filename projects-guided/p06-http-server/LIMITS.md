# Exact protocol and evidence limits

The accepted language is one ASCII HTTP/1.1 request, origin-style slash target, exact Host localhost, no Transfer-Encoding, no Expect, and Content-Length absent or exactly0. All duplicate fields reject. It supports GET routes only, emits one response, then closes. Request bodies, chunked grammar, persistence, general Host syntax, TLS, cache negotiation, Date handling and broad interoperability are absent; it is not a complete conformant HTTP server.

A pure parse rejects already-collected bytes after the header delimiter. Later-arriving extra bytes may instead be discarded on close, so this is not global pipelining detection or a proxy security proof. Header memory and deadline are bounded per connection; connection count and application admission are not implemented. Tests use local AF_UNIX sockets; one timeout test uses injected time. No production performance or security certification follows.
