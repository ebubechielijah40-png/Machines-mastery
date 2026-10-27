# Inspected primary sources and claim scope

Inspected 2026-10-23. Code, state machines, derivations and examples are original.
References verify API/language context; local records verify only executed runs.

| Resource and version | Exact inspected locator | Claim supported |
| --- | --- | --- |
| WG14, [N1570 C committee draft](https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf), 2011-04-12 | §5.1.2.4 paragraph25 and note26; §7.17.3 paragraphs6–12 | C data-race undefined behavior and sequentially consistent ordering context |
| Same draft | §7.17.7.1–2 and §7.17.7.5 | Atomic store/load versus atomic read-modify-write APIs |
| Same draft | §7.26.4.1–3, .6; §7.26.5.1, .6 | Mutex lifetime/lock/unlock, thread creation/join and synchronization |
| Same draft | §7.26.3.1–4, .6 | Broadcast/signal on current waiters, condition lifetime, atomic release/wait and mutex reacquisition |
| Remzi H. Arpaci-Dusseau and Andrea C. Arpaci-Dusseau, [OSTEP chapter30: Condition Variables](https://pages.cs.wisc.edu/~remzi/OSTEP/threads-cv.pdf), version1.10 visible, ©2008–25 | Printed pp.3–4, 9–13; while/if, wake/recheck and producer/consumer discussion | Predicate-based waiting context and robustness motivation; not a complete book reconstruction |

N1570 is a C11-era draft, not the latest standard or every defect resolution.
OSTEP's historical illustrative volatile example is not used as a valid C11
synchronization recipe here. Upstream copyrights remain with the originals;
no source chapter, substantial prose or upstream code is bundled.
The model's optional wake budget, finite geometry and path counts are declared
project assumptions/results, not guarantees about the local C runtime. No
weak-memory, fairness or hardware-lock implementation source was reconstructed.
