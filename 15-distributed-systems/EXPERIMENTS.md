# Distributed systems experiments

Use local processes/simulators and explicit fault models.

- duplicate messages → require idempotency/deduplication;
- reorder messages → identify operations that commute and those needing ordering/versioning;
- drop messages → retry and observe duplicate risk;
- delay one replica → stale reads and eventual convergence;
- partition two groups → decide availability/consistency policy under the application model;
- crash/restart → persist enough state to avoid forgetting committed actions;
- clock skew → show why wall-clock ordering is unreliable without assumptions;
- hot key → observe skewed load despite even node count.

For every lab, state what your toy model omits from real networks and storage.
