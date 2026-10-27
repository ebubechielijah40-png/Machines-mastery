# Hints after a design attempt

For A1, find `b'\r\n\r\n'` before text decoding. Normalize field names, not the entire message. Reject a repeated normalized name even when both values look equal: the subset has a deliberately smaller accepted language than full HTTP.

For A2, construct the body bytes first, then compute `len(body)`. An independently written response checker should not reuse the response builder.

For A3, the next recv limit is the smaller of your chosen chunk size and `MAX_HEADERS-len(raw)`. The header terminator may be split across reads. A zero return before it is an incomplete request, not an empty valid request.

For A4, declare one deadline before the loop. Put `close()` around the whole handler rather than only around sending. Use an injected transport exception to reach the otherwise uncommon cleanup path.

For A5, separate client send chunks, server read limits and client response recv sizes. They measure different interfaces. Read [solutions](SOLUTIONS.md) only after recording predicted outcomes.
