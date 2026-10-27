# Official Java inspection scopes

Root inspected2026-10-23:

- [JLS17 §4.3.1 and§4.12.4](https://docs.oracle.com/javase/specs/jls/se17/html/jls-4.html):
  objects/reference values and final-variable versus referenced-object distinction.
- [JLS17 §14.20.3](https://docs.oracle.com/javase/specs/jls/se17/html/jls-14.html#jls-14.20.3):
  reverse resource closing and primary/suppressed exception rules.
- [JLS17 §17.4.5](https://docs.oracle.com/javase/specs/jls/se17/html/jls-17.html#jls-17.4.5):
  selected monitor/volatile/start/join happens-before rules. No full memory-model
  proof or every allowed weak-memory outcome is claimed.
- [AtomicInteger API17](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/util/concurrent/atomic/AtomicInteger.html),
  incrementAndGet scope: atomic compound counter operation.

The bounded classes, barrier-controlled schedule, cleanup trace, fifteen checks
and actual bytecode observation are original. Actual OpenJDK17.0.20 commands are
retained in evidence/observed.json, including --release17 and interpreter mode.
No source manual, JDK binary or copyrighted source passage is distributed. Runtime
observations do not establish GC timing, service performance or full Java mastery.
