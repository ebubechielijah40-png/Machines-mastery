# Explained solutions

1. Retain `(A,5,5)` and `(B,7,12)`. Counter12 equals5+7. A's identity selects its
original response5; reading current counter12 answers a different operation.

2. Main-only copy can contain12 and pass its own database integrity check. The
engine snapshot includes committed D and contains16 in this controlled schedule.
Neither outcome alone proves the newest state under arbitrary concurrent writes.

3. Newdirectory→copieddatabase→verifieddatabase→synceddatabase→syncedmanifest→
synceddirectories. Readers require all checks and the manifest. A missing marker
means incomplete generation, never permission to invent one. Actual child kills
are application failures while the kernel/storage remain alive; no power cut ran.

4. A writer can commit C after the copied state is selected and before the
manifest's informational timestamp is recorded. The copy can be consistent
without containing C. Unsynchronized wall clocks add another ordering problem.

5. A/B evidence agrees, so promotion can pass while C is lost. A/B/C evidence
refuses promotion because C is absent. Empty evidence cannot detect that loss.
The verified claim quantifies only over supplied receipts; completeness needs
an independently trustworthy inventory of accepted operations/data boundaries.

6. After all state/digests are rewritten consistently, byte hash, logical hash
and sum invariant pass. A separately retained `(D,4,16)` disagrees with `(D,8,20)`.
Its protection must be independent of the replaced snapshot. A receipt copied
inside that same attacker-controlled manifest would not supply this independence.

7. Rows `(A,5,999)` and `(B,7,12)` with counter12 satisfy the sum invariant but
A's result is impossible from initial zero if A preceded B. Even ordinary integer
bounds on999 do not restore historical knowledge. External receipts and an
authenticated, ordered operation history address different missing information.

8. Existing descriptors can still access an old inode while new opens see the
replacement; WAL/SHM/journal files can belong to another database state. Stop all
users, restore to another unused path and verify before changing routing. This
lab assumes trusted offline paths and does not implement concurrent promotion.

9. Counts are `[2,3,4]`, overflow1, sum18 and N5. p50 rank3 has exact value2,
upper bound2. p95 rank5 lies beyond finite bound5, so the returned bound is null
with overflow1. An empty summary also returns null but has N0, not N5.

10. Split `[0,1]` and `[2,5,10]`: cumulative counts `[2,2,2]` and `[0,1,2]` sum
to `[2,3,4]`; overflows0+1 and counts2+3 also pool. For each bound, indicator
sums distribute over a disjoint union. Overlap adds one event twice and can bias
both the denominator and quantile. Schema validation cannot infer membership.

11. Worker quantiles1 and100 average50.5; pooled rank95 is1. Traffic weighting
gives1.99, still not1. A quantile is an order statistic, not a linear statistic.
Pooling a distribution representation preserves information that both means lose.

12. Good requires a successful or duplicate response, so good≤ok+duplicate.
Empty populations sum zero observations and must have sum0. A conserved total
can still violate these semantic restrictions. Passing them does not prove that
reported events really happened; an authenticated measurement chain is separate.

13. The selected observed value is greater than5 and at most10, provided prior
cumulative buckets put the rank above5. Returning10 is a conservative bound.
Linear interpolation would impose a distribution assumption within that bucket;
the implementation makes no such assumption and cannot establish the exact value.

14. Shortburn=(2/10)/.05=4; longburn=(2/40)/.05=1. Both populations are sufficient,
but the long burn is below2, so no alert. Adding populations double counts short
events already inside the long window; it is not a new fifty-event population.

15. A low-volume outage can lack ten/thirty eligible events; a short spike can
be diluted in the long window. At99%, burns in the preceding case become20 and5,
so that case alerts, but the minimum population blind spot remains. Targets
change policy sensitivity and budget; they cannot manufacture missing evidence.

16. Keep A's returned5, perform B(+7), retry A and require5 with duplicate true.
The mutant returns12, so reject it even though `/ready` responds and counter12
remains correct. These checks intentionally cover response compatibility beyond
process liveness and final effect consistency.

17. Stable and mutant share the exact schema and retained response format.
Dropping a column required by stable would break rollback. A safer sequence adds
new optional representation while supporting old readers/writers, verifies mixed
operation, then removes old representation only after rollback/retention windows
are explicitly closed. This is a design exercise, not an executed migration claim.

18. The recorded start is immediately before `restore_backup`; the end follows
restored process startup, three HTTP operations and context-manager shutdown.
It includes file validation/copy/sync, scheduling, startup, sockets and teardown.
For decomposition instrument each boundary, repeat with fixed data/caches/tools,
report variation, and retain empty/control trials. Integer ns is a unit of stored
intervals, not proof of nanosecond accuracy or an externally promised RTO.

19. Independent success means reproducing required behavior from contracts,
not identical helper names. Accept only create-only generations, explicit external
receipt rejection, conserved pooled counts and old-client regression detection.
Explain failure with the smallest state trace; record an honest unaided attempt.
The author tests and this solution do not certify any learner's reconstruction.

20. Queue state/identity and local accounting can commit together; an email
provider's effect is outside that transaction. Sending then losing acknowledgement
can cause a retry to send twice; committing then restoring a stale queue can
forget the first effect. A durable outbox plus provider-recognized idempotency or
independently queryable effect receipts helps reconciliation under stated retention
assumptions. The local lab implements neither a remote provider nor distributed
atomic delivery, so do not call the transfer solved without that evidence.
