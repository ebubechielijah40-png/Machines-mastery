# Attempt before opening the reference

1. Trace A:+5, B:+7, retry A:+5. List counter state and every response.
2. Write a two-commit implementation that can increment without storing a key.
   Mark the exact crash interval and repair it with one transaction.
3. Two workers receive the same previously unseen key. Explain why lookup before
   obtaining the writer transaction is insufficient; draw a harmful schedule.
4. A client times out after a write. Compare retrying with the old key, retrying
   with a new key and querying a current counter value. Which recovers its reply?
5. Derive allowed/remaining bad events and burn rate for N=1000, t=.99, B=17.
6. A window contains no offers. Explain why success=1 would be an invented result.
7. Calculate nearest-rank p50/p95 for `[2,3,4,100]` ms. Calculate their mean and
   explain which aspect each statistic reveals.
8. Construct two shards for which averaging their p95 differs from pooled p95.
9. For issued0, offered2, started12, ended20 ms, decompose latency. A database
   stopwatch reports8 ms; how much user time did it omit?
10. With two workers requiring12 ms each, derive the ideal service-rate ceiling
    before scheduling/SQLite overhead. Predict offered rates125 and250 per second.
11. Change capacity6 to60 while preserving that slow workload. Predict which
    outcomes can improve and which latency cannot be solved by extra waiting space.
12. Implement an event-gated overload test, not a timing guess. Show that active
    plus waiting admitted requests never exceeds capacity and every slot returns.
13. Explain why a late known success is a bad latency event but not a missing
    state change. Add an oracle checking the durable effect separately.
14. Run the two application-crash phases. State exactly what was killed, what the
    fresh process observed and which hardware durability claim remains untested.
15. Design key expiry for clients allowed to retry for24 hours. Give a counterexample
    when records expire after1 hour. State an additional identity/authentication rule.
16. Rebuild the transactional store and finite SLO evaluator from memory. Use a
    different table layout and independently prepared traces. Explain which tests
    still apply and perform a nontrivial transfer to a debit reservation or job receipt.

Deliver a predicted trace, implementation, independent tests, raw actual output,
metric denominator, changed-variable analysis and a short correction decision.
A rubric of20 points awards4 for state/transaction reasoning,4 for counterexamples,
4 for independent tests,4 for actual measurement interpretation and4 for transfer
with disclosed limits. Running the reference alone earns no reconstruction credit.
