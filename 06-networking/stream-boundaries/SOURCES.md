# Verified source map

Inspected 2026-10-22 during this development batch. Links are intellectual sources; no specification text is vendored. Lesson examples, machine, tests and socket observations are original.

| ID | Primary source and exact inspected scope | Supports | Does not establish |
| --- | --- | --- | --- |
| N1 | W. Eddy, editor, RFC 9293, *Transmission Control Protocol*, August 2022, [§2.2](https://www.rfc-editor.org/rfc/rfc9293.html#section-2.2) | TCP's reliable, ordered byte-stream service and distinction from IP datagrams | The local AF_UNIX experiment's internals, Internet performance or full TCP reconstruction |
| N2 | Python Software Foundation, Python 3.12 [socket documentation](https://docs.python.org/3.12/library/socket.html), entries `send`, `sendall`, `recv`, `socketpair`, `shutdown` inspected | Partial-send return contract, sendall exception limitation, EOF and local socket interface | Portable exact buffer sizes or cryptographic/authenticated delivery |

The documentation rendered as Python 3.12.15; the recorded interpreter is identified in each JSON evidence file (3.12.14 in the original run). No version equality is implied. RFC material retains IETF Trust terms; Python documentation retains PSF terms. This repository contains original explanations and uses standard-library interfaces rather than copying either text or implementation.

Classification of this bounded unit: STRONG after recorded tests, with total-memory, application-delivery and AF_UNIX/TCP limitations stated. Classification of the entire networking domain remains PARTIAL: routing, UDP datagrams, DNS, congestion control and a complete TLS/HTTP progression are not supplied by this unit.
