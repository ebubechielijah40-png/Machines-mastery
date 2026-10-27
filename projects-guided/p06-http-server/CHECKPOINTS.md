# Concrete checkpoints

Use A0–A6 in the [build guide](README.md). Keep an attempt before reading reference code.

- A0: classify complete, duplicate-Host, bare-LF and incomplete requests by wire bytes.
- A1: pure parser accepts the literal request and rejects every shorter prefix.
- A2: an independent splitter finds exactly six bytes after the successful response header.
- A3: actual one-byte writes survive three-byte server reads and return the same response.
- A4: a fake monotonic clock proves the second read cannot begin after the absolute deadline; injected recv/send failures close ownership.
- A5: saved JSON reports 200/404/405/400 cases with consistent body length.
- A6: reconstruct the contract and implementation, then explain why unsupported chunking/persistence prevents a full HTTP conformance claim.

Do not substitute a count of passing tests for the explanation of boundaries and excluded semantics.
