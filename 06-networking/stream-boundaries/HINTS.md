# Hints: stream boundaries

1. The length is three, not seven; retain the prefix until the body is complete.
2. Count prefix and payload bytes for each individual frame. The empty message still consumes four wire bytes.
3. Locate the check executed immediately after the fourth header byte. Separate input ownership, pending buffer and returned payload ownership.
4. A first send accepting two bytes has already changed the peer's stream. Move the starting index of the next attempt.
5. Compare decoded payloads first; compare kernel buffer numbers separately.
6. An iterator may already have executed the consumer's handler when a later `next` raises.
7. Draw OPEN with HEADER/BODY substates, and distinct CLOSED and FAILED terminal states.
8. A durable cache keyed by authenticated identity plus request ID can associate retries with the same result. Define request-ID reuse with different content as an error.
