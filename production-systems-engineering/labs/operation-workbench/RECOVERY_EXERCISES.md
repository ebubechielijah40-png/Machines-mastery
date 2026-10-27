# Recovery and telemetry assessment

Predict before executing. Explain assumptions and intermediate steps; final
numbers alone are insufficient. [Hints](RECOVERY_HINTS.md) and
[solutions](RECOVERY_SOLUTIONS.md) are separate from the initial attempt.

1. A(+5) returns5, B(+7) returns12, A retries after restart. Specify persistent
   rows and both the correct response and final counter. Why are they different?
2. A main database says12 and its WAL contains a committed D(+4). Predict the
   naïve main-file backup, engine snapshot and each structural check outcome.
3. Write the generation state machine. Identify what readers require after a
   kill between database sync and manifest creation. Which crash type was tested?
4. Why does a manifest creation timestamp not establish the latest committed
   operation? Give a concurrent-write schedule compatible with a consistent backup.
5. Backup contains A/B; C(+4) later receives16. Evaluate promotion with external
   receipts `{A,B}`, `{A,B,C}` and an empty set. State exactly what each establishes.
6. Change D's delta4 to8, result16 to20 and the counter to20; recompute all unkeyed
   checks. Which checks can pass? Which separately protected evidence distinguishes
   this false history from the original? Reproduce only on disposable data.
7. A restored counter equals the sum of retained deltas. Does that prove every
   stored original response is correct? Construct a counterexample.
8. List the risks of replacing a live database file while its process remains
   running. Explain why checking a destination filename alone is insufficient.
9. For latencies `[0,1,2,5,10]`, bounds `[1,2,5]`, derive cumulative buckets,
   overflow, sum, nearest-rank p50 and p95 upper bounds. Explain null.
10. Partition the preceding population into two shards and pool their counters.
    Prove why adding buckets preserves the whole result for disjoint shards.
    What if the shards overlap by one request?
11.99 events take1 unit in one worker and one takes100 in another. Calculate each
   p95, their mean and the pooled p95. Why does weighting worker quantiles by
   traffic still fail as a general quantile algorithm?
12. A ten-event summary claims ten good events but all statuses are overload.
   Another empty summary has nonzero latency sum. Explain why rejecting these
   contradictions is stronger than merely checking count conservation.
13. A percentile lies in a bucket `(5,10]`. What does the upper-bound algorithm
   establish? What extra assumption would an interpolated value need?
14. At target95%, short has10 events/2bad; long has40 events/2bad. Compute both
   burns and the alert. Explain why adding the nested populations is incorrect.
15. Give two mechanisms by which this two-window rule can miss a real incident.
   Would raising the target from95% to99% fix both? Show the arithmetic tradeoff.
16. Write an old-client compatibility test that catches the supplied mutant while
   a readiness-only and final-counter-only test both pass. Preserve old results.
17. Explain why reverting code worked in this drill. Design a migration where
   reverting code is insufficient, and specify a compatible two-release sequence.
18. Classify the measured restore interval. Identify its start/end events and
   included work. Design repeated trials that separate restore copy from process
   readiness without pretending clock units imply accuracy.
19. Rebuild backup/restore, histogram pooling and the compatibility probe from
   memory. Use adversarial tests selected before consulting the reference. Record
   which part you could not reconstruct and the smallest missing concept.
20. Transfer to a job queue whose worker sends an email after committing a row.
   Which effects can be covered by the database transaction? Show a lost-reply
   schedule, a restore schedule, and evidence needed to reconcile external effects.
