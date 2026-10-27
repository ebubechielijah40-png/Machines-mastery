# Validation layers

Run both suites from the repository root:

```bash
python -m unittest discover -s 05-operating-systems/code -p 'test_*.py' -v
python -m unittest discover -s projects-guided/p05-mini-kernel-labs/code -p 'test_*.py' -v
```

The model suite checks complete worked traces, boundary arrival order, explicit
switch cost, idle and same-job continuation, invalid workloads, 100 seeded
conservation workloads, permission faults, remapping, unmapping, all 256 virtual
addresses against a direct-map oracle, LRU eviction, per-space isolation and
supervisor/user access. The interface suite invokes the actual CLI as a child
process and checks JSON results, bounded-input rejection, exit status and error
output. [Raw validation](evidence/validation.json) preserves executed commands.

Write your own counterexamples before checking reference answers:

- q=1, cost=1 with A(0,2), B(1,1): account for every tick.
- A alone at tick 3 with cost 100: no false different-job switch should appear.
- Warm VPN 2 → PFN 7, then remap it to 9: the next PA for address 45 must be 157.
- Warm a read-only entry, then request a write: hit status cannot bypass PROTECTION.
- Put the same VPN in two AddressSpace instances with different PFNs: no cross-
  space translation should leak.

Do not repair a failed oracle by copying the implementation's output into it.
Explain which transition or invariant was wrong, then derive the expected
result again. Tests do not establish CPU privilege enforcement, multicore TLB
shootdown, crash safety, POSIX behavior or actual scheduler latency.
