# Progressive hints

**Hint 1:** Draw the state machine/data-flow for `measurement → filtering → controller → actuator → feedback → safety` before choosing classes/functions.

**Hint 2:** Separate pure transformation logic from I/O so tests can isolate mechanisms.

**Hint 3:** Make failure states explicit rather than relying on exceptions/logs as the design.

**Hint 4:** Only optimize after a baseline benchmark identifies a bottleneck.
