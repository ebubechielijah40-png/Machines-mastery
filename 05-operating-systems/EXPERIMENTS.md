# Model and host observations — keep the evidence classes separate

**Question A:** how does quantum size trade response and overhead in the declared
single-CPU model? **Hypothesis:** smaller quanta can reduce first-service delay
but increase charged switches. **Controls:** same three arrival0/burst8 jobs,
fixed switch cost1, integer model, same tie rule. **Procedure:** vary quantum
1,2,4,8; retain complete timelines and calculate useful/elapsed ticks.
**Instrumentation:** exact model events/metric formulas, no host timer.
**Observed:** elapsed47,35,29,26 respectively, useful24 in each. This tests the
specified accounting; it does not measure Linux context-switch performance.
Alternative event-boundary conventions can change results and must be stated.

**Question B:** does a cached address survive a remapping correctly?
**Hypothesis:** after VPN2 changes frame7→9, VA0x2d resolves125→157 and misses
once after invalidation. **Controls:** same16-byte page/offset and object.
**Measurements:** returned address, hit bit and access/protection flags.
**Observed:** raw trace retains first miss, hit, write protection fault and
remapped address. No real hardware MMU was instrumented.

**Question C:** are duplicate descriptors independent positions, and does closing
one writer yield EOF? **Hypothesis:** duplicate regular-file reads share offset;
EOF waits for all writer references to close. **Controls:** an owned temporary
six-byte file and empty pipe, no external processes writing them. **Procedure:**
open/dup/read, compare separate open, then nonblocking pipe read before/after
closing the last duplicate writer. **Observed:** reads `ab`,`cd`,`ab`, shared
offset4; would-block while writer reference remains, EOF after closing it.
These are actual local host observations, not model expectations.

The child-process observation additionally retains requested cwd, actual printed
cwd, exit7 and unchanged parent cwd. Python/platform are in the
[unaltered run JSON](evidence/observed.json). Run:

```sh
python3 05-operating-systems/code/experiment.py
```

All data are generated locally from declared inputs. No source book figure,
benchmark, process identifier, physical address or timing result was fabricated.
Follow-ups: vary arrival ties and test invariants, add a modeled I/O-blocked state,
disable cache invalidation to demonstrate stale authority, and retain one parent
writer in the shell project to reproduce missing EOF. Perform a real context-
switch timing study only with a separate workload/control/uncertainty protocol.
