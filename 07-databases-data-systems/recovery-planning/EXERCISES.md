# Attempt before opening the reference

Record a prediction, derivation and independently checkable output for each
task. Mark assumptions explicitly. Implementation exercises use disposable local
directories; never point fault scripts at another process or a real database.

1. Base `{1:A,2:B}` and suffix `delete1,put3C,put2D` arrive in one batch. Derive
   correct state and the wrong result of updating the base with suffix.data.
2. Base version41 has three suffix batches. Derive global version, next local
   frame number, and both numbers after checkpoint plus one commit.
3. List the dependencies of CURRENT. Construct a failure if CURRENT is replaced
   before the new empty suffix exists.
4. Explain the difference between atomic replacement visibility and directory
   synchronization. Which does a process-kill test establish on this host?
5. A reader has selected the old generation but not opened its image. Explain
   why collection without coordination can fail, then show how this shared lock
   contract prevents that schedule.
6. P1 locks LOCK inodeA. A cleanup script deletes LOCK and creates inodeB. Show
   how P2 can enter concurrently; propose a correct cleanup rule.
7. Two clients read value10 at global version5 and intend to increment. Trace
   both unconditional writes, then expected-version writes and recomputation.
8. Two clients update unrelated keys after reading the same global version.
   Explain the safe false conflict and what per-key versions would additionally
   need to represent for deleted/nonexistent rows.
9. Explain why an exception after a full frame append is not proof that the
   batch is absent. Write a safe reopen/reconciliation procedure for a caller.
10. Enumerate every prefix of a two-operation encoded frame. State which rows
    recovery may expose and when append must refuse an incomplete tail.
11. A selected image is corrupt but an older image validates. Explain why an
    automatic fallback is dangerous even when startup would otherwise succeed.
12. A checkpointed log contains100 puts and100 later deletes of those same keys.
    What live state and audit history remain after collecting old generations?
13. Left keys `[7,7,9]`, right keys `[7,7,7,8]`: compute join multiplicities J,
    nested work and hash work under this lab's model. Is a hash plan always better?
14. For n20,m30,DL=DR=10, compare plans with row grants19 and20. Explain what
    execution must do if the supposedly20-row build side actually contains21.
15. Reproduce the90-hot-key cardinality failure. Derive estimated and exact J;
    distinguish a wrong estimate from a wrong result.
16. Replace hash bucket lists with one row per key. Give the smallest duplicate
    counterexample and an independent bag comparison that catches it.
17. Consume `(1,0,+4),(2,1,+7),(3,0,-1)`, checkpoint, then consume overlapping
    `(2,1,+7),(3,0,-1),(4,1,+2)`. Derive final offset, totals and new-effect count.
18. Construct the two crash windows for separately storing effects and offset.
    Explain how this WAL batch closes both windows and where that proof stops.
19. Change a past payload without changing its source/offset. Predict and execute
    the outcome. Explain what extra evidence a mutable upstream source requires.
20. A batch also sends an email. Draw the effect/offset/email commit orders that
    can lose or duplicate delivery. Explain why the current proof cannot promise
    exactly-once delivery to that second system.
21. Rebuild publication, OCC, bag hash join and stream commit without opening
    the references. Use a new case, different key values and new crash boundary
    probes. Explain every resource limit and any blocked toolchain.
22. Transfer to inventory reservations: a client reads two products and a total
    stock predicate, then updates one key. Explain why a global version is coarse
    but covers this snapshot precondition, and what a naïve per-key alternative
    might miss. State what remote supplier confirmation adds to the problem.
