# Independently checkable solutions

1. Responses are5,12,5; final state12 with only A:+5 and B:+7 retained.
2. Commit counter+=5, then insert key, creates a window where a crash leaves5
   without its receipt. A retry adds another5. Put both writes in one transaction;
   an aborted transaction retains neither. Verify by reopening, not merely reading
   a cached value in the same object.
3. If both readers observe absence before either serializes writing, both can
   attempt an effect. Obtaining a writer transaction first makes lookup and effect
   part of one ordered critical transaction. Busy failure is an outcome to handle,
   not permission to continue with an unprotected update.
4. Same-key retry can recover the stored response, provided identity history and
   correct routing remain intact. A new key can double the effect. A current total
   is insufficient: another user's operation may have changed it.
5. Allowed=1000*.01=10, remaining=10−17=−7; burn=(17/1000)/.01=1.7. SLO fails.
6. G/N is0/0 when no requests exist. Report no observation/null, never infer that
   hypothetical users succeeded.
7. Nearest-rank p50=3, p95=100, mean=27.25 ms. The percentile ranks and mean measure
   different aspects; none alone tells which requests were rejected or incorrect.
8. Shard A has100 samples1 ms; shard B has one100 ms sample. Shard p95 values are1
   and100; their unweighted average is50.5. Pooled p95 is1 because rank96 of101 is1.
9. Generator lag2, queue10, residence8; total20 ms. The database stopwatch omitted12.
10. Ideal ceiling2/.012≈166.7 requests/s, before overhead and serialized writes.
    A125/s offered rate may be sustainable;250/s exceeds this ideal ceiling.
    Neither calculation proves an actual host capacity or absence of bursts.
11. Extra waiting slots may trade overload rejections for deadline expiry or slow
    completions. Without more service capacity or less offered work, they cannot
    remove a persistent rate deficit. Execute and inspect all outcomes; do not
    credit a lower rejection count while omitting bad delayed work.
12. Hold an event inside one worker's apply call. With capacity1 the second valid
    offer immediately returns overload. Release the worker, await completion and
    submit again in an unexhausted session. The finally block returns its slot on
    expected errors too. Our test separately checks session observation exhaustion.
13. A known result that arrived after the declared latency deadline belongs in
    the bad SLI count. Durable state can still include the effect. Compare the
    operation receipt table to the counter invariant, separately from good-event count.
14. The coordinator kills only its own spawned application process at an emitted
    before/after-commit marker. The actual stored observations show0 then first
    application for before-commit,7 then duplicate response for after-commit. They
    do not kill the OS or test power loss, device firmware or a corrupted filesystem.
15. Expiring a key after1 hour lets an otherwise valid24-hour retry look new and
    apply twice. Retention must cover the retry horizon plus justified margins,
    or use a permanent/compacted receipt scheme with equivalent identity semantics.
    Bind keys to an authenticated principal and operation schema. A caller-supplied
    name alone is not proof that the caller owns another request's identity.
16. Accept a different schema if it preserves one atomic effect/receipt boundary,
    original reply retention and explicit conflict behavior. For a reservation,
    atomically retain receipt and resource debit; add an independent no-negative-
    inventory invariant. Availability/latency and resource correctness still require
    separate evidence. This does not solve expiry, distributed routing or external
    payment-provider uncertainty automatically.
