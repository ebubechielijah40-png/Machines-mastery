# Reference checks

1–4. The aliased object sees source[0]=8; copied Packet stays3 and stays3 after a
returned clone is changed to42. Rebinding the callee's local parameter leaves the
caller's reference unchanged; mutation through a shared reference would not.
5. Opens A,B; uses A,B; closes B,A. The body exception stays primary with B then A
as suppressed exceptions. These outcomes are actually checked by the native build.
6. With a normal body and both closes failing, B's closing failure becomes primary
and A's is suppressed. This extension is a language-rule prediction until run.
7. Both threads read0 before the barrier opens; both then store1. Volatile orders
its individual accesses but does not fuse that read/compute/write sequence.
8. AtomicInteger.incrementAndGet or one monitor enclosing the entire increment
returns final2. Protecting only a trailing assignment cannot repair stale reads.
9. A successful join orders completed-thread actions before subsequent caller use.
Interruption is cooperative and does not undo an already committed external effect.
10. javap reveals JVM instructions and calls, not physical register allocation,
final JIT machine code or a guaranteed GC schedule.
11–12. Add actual tests before marking an extension observed. A reconstruction must
explain ownership, exception precedence and the synchronization operation boundary,
not merely produce the three expected print strings.
