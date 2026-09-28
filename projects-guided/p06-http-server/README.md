# HTTP service

**Mechanism chain:** TCP framing → request parser → concurrency → timeouts → metrics.

**Suggested implementation:** C/Go/Rust.

Start at A0. Do not read `HINTS.md` until you have written a design attempt. The objective is not merely to make tests green; explain why the design works, what assumptions it makes, and what a production/physical version would add.
