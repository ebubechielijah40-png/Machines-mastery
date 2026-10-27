# Exercises: stream boundaries

1. Encode payload bytes `00 ff 00`, then decode the wire using one byte per call. Write every pending-buffer state and exact output call.
2. For the wire containing `hi` and an empty frame, classify EOF after each byte as clean or truncated. Explain why EOF after zero bytes is clean.
3. Prove that a peer announcing length `max+1` cannot make this decoder retain the announced body. What other memory remains outside that proof?
4. Debug a sender that repeats `send(wire)` until its total return count reaches the wire length. Give a concrete short-send trace showing corrupted output; repair the algorithm.
5. Run the local experiment twice. Separate invariants from environmental measurements. Explain why equal receive chunk sizes do not prove the sender wrote those sizes.
6. Change only the API design: yield messages before a later protocol failure. Describe when application side effects occur and how an exception after the first yield differs from this list-return API.
7. Reconstruction: without viewing the code, implement four-byte framing with a configurable maximum, empty messages, clean/truncated EOF and terminal failures. Use an independently written literal wire vector and every possible two-cut partition as checks.
8. Transfer: acknowledgements are lost after a request commits. Propose a request-ID and response-cache protocol. State why framing alone cannot determine whether retrying is safe.
