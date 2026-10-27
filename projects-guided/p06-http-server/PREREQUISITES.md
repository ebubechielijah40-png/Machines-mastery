# Entry gate: HTTP subset

Complete [stream boundaries](../../06-networking/stream-boundaries/LESSON.md), including all EOF positions and partial-send reasoning. Know Python bytes, bytearray, slices, exceptions, finally, dictionaries and a worker thread. Tools: Python 3.12 standard library and socketpair support.

Before A0, write the exact wire bytes for a GET request and count response body bytes independently. Explain why a recv call need not return a complete header and why a per-read timeout can be extended by repeated partial arrivals. The [README](README.md) supplies the protocol grammar and guided milestones; it does not assume prior HTTP server experience.
