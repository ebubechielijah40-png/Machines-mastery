# Explained solutions

1. Correct state is `{2:D,3:C}`. Empty-state suffix replay yields `{2:D,3:C}`;
   applying only that dictionary to the base incorrectly retains1:A. Replay the
   ordered delete as an operation, not just surviving suffix puts.
2. Current global version44; next local frame4. Checkpoint keeps global44 and
   empties the suffix. The next batch has local frame1 and yields global45.
3. CURRENT selects a specific image, suffix and base version. Publishing first
   allows a reader to select a missing suffix. Write/sync both dependencies,
   sync their directory entries, then publish/sync the manifest pointer.
4. Atomic replacement prevents a missing-name interval for another local
   opener. Directory sync addresses persistence of that name update under the
   API/storage assumptions. Our killed application leaves a running kernel;
   it does not independently verify a physical power-loss claim.
5. Uncoordinated collection can unlink the selected image before the reader
   opens it. Here the reader holds a shared lock for selection and use; the
   collector needs an exclusive lock and cannot unlink until readers finish.
6. P2 opens inodeB and obtains its own exclusive lock while P1 retains inodeA.
   Preserve the same LOCK inode; release ownership by closing its descriptor.
   Do not delete that file as ordinary stale-generation cleanup.
7. Unconditional writes produce11 then11, losing one intended increment.
   A's expected5 succeeds and advances version6. B's expected5 fails. B reads11
   at6, recomputes12, and commits expected6; final12 preserves both intentions.
8. The global version rejects B even if A touched another key. This costs
   retries but avoids silent stale-snapshot writes. Per-key schemes need
   versions/tombstones or equivalent information for absence and reinsertion;
   they also need a policy for multi-row/predicate reads.
9. A full frame may already be visible after append, and a failed sync has an
   uncertain persistence outcome. Stop using the uncertain operation result,
   reopen under the lock, validate history, then reconcile the application's
   intended identity/effect. Do not blindly invent a new identity and add twice.
10. Every cut shorter than a complete valid frame exposes the base only;
    the complete checksum-valid frame exposes both operations. A nonempty
    incomplete tail blocks append until explicitly investigated/repaired.
    A checksum-invalid complete frame is corruption, not ordinary tail repair.
11. Validity does not imply freshness. The older generation can lose an
    acknowledged transaction. Raise the selected-state error; a separate
    operator recovery decision must name its data-loss boundary and evidence.
12. Live state is empty. The new image represents that empty state and the
    new suffix is empty. Once old generations are collected, the200-operation
    historical audit is gone; a separate archive is required to retain it.
13. Key7 contributes2×3=6 outputs; key9 contributes0. J6, nested work3×4+6=18,
    hash work3+4+2×6=19. Under this declared model nested wins. A complexity slogan
    cannot replace the specified costs and tiny workload.
14. Estimated J60; nested660, hash170. Grant19 excludes the20-row hash build,
    grant20 permits it. Actual21 exceeds that grant and must refuse/replan/spill;
    this implementation refuses. Statistics do not authorize hidden allocation.
15. Estimate floor(10000/11)=909. Exact90²+10=8110. Correct bucket lists emit8110;
    the estimate only influenced plan selection and predicted work. A wrong
    estimate affects performance expectations; dropping pairs changes meaning.
16. Left `(7,a),(7,b)` and right `(7,c)` require two outputs. One-row buckets
    overwrite one left occurrence and yield one. Compare output multiplicities
    with Cartesian equality or a Counter of complete output tuples.
17. Before restart totals0→3,1→7, offset3. The overlap skips2/3 and adds2 to
    group1 for event4. Final totals0→3,1→9, offset4, one newly applied effect.
18. Effects-first can duplicate after a crash before offset commit; offset-first
    can lose effects after a crash before their commit. One verified WAL frame
    atomically represents both local changes. This argument assumes an immutable
    ordered source and says nothing about unrelated remote effects.
19. The past event is skipped; changing its payload does not change local totals.
    The actual experiment retains group0=3 despite proposed old deltas999.
    Stable source/version provenance or an explicit correction/rebuild protocol
    is needed. A source name alone cannot establish historical immutability.
20. Email-before-local-commit can send then crash, causing a retry to send again.
    Local-commit-before-email can advance the offset then crash, skipping email.
    A transactional outbox can retain a delivery intention, but remote receipt,
    idempotency and retention rules still determine the final delivery contract.
21. Success requires observable invariants and negative controls, not matching
    reference private names. Check selected-generation dependency order,
    deletion persistence, version rejection/recomputation, bag multiplicity and
    progress/effect atomicity with new finite cases. State unexecuted boundaries.
22. Any intervening write changes a global version, so validating the whole
    snapshot version rejects all changed-key/predicate schedules, at the cost
    of false conflicts. A per-key scheme that checks only the updated product
    can miss a change to another product or an inserted row that affects the
    predicate. Remote supplier confirmation adds another commit/uncertain-reply
    boundary not covered by this single-directory transaction.
