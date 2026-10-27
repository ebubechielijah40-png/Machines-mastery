# Progressive hints

For questions 1–5, separate bytes being visible from a new process from bytes surviving a host power interruption. The frame has a 16-byte header and a four-byte checksum; the file adds a separate seven-byte header.

For 6–7, a frame is the transaction boundary. The last four bytes matter even if both JSON operations are already readable. Try a final `put` lacking its value; checksumming malformed input does not make its operation grammar valid.

For 8–10, list three events separately: full bytes written, sync returned, caller received response. Absence of a response does not identify which earlier events occurred. A valid shorter history is still valid under a prefix-only format.

For 11, at every interruption ask which complete durable copy remains. A pathname switch and writing the referenced file are different persistence operations.

For 12, time only replay and keep the key count fixed. Include all five observations. Cached sequential reads, scheduler noise, JSON parsing and allocation can all affect the result.

For 13, the race starts before appending bytes: both readers choose the same next transaction number. Ownership must cover recovery, repair and append, not just one `write()` call.
