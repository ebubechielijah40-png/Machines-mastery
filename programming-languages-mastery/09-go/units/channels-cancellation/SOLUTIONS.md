# Reference checks

1–2. Appends within shared capacity can overwrite the same second cell; sending
copies the slice value while retaining access to the same backing array. Explicit
input copying before spawning separates storage, provided the caller does not
race with the copy itself.
3. |x|≤10^6 implies x²≤10^12<2^63-1.
4. Results(index,value)=(2,25),(0,9),(1,4) produce answer[9,4,25].
5. The feeder alone closes jobs; workers send results; only the coordinator closes
results after feeder/workers finish. The coordinator then closes Done.
6. Cancel an abandoned stream while a worker send or feeder send is blocked.
A bounded wait on Done must fail for a deliberately broken protocol. Retain the
actual failure and clean up the test process; do not leave leaked tests running.
7. When multiple communications are ready, select chooses one; source order is
not a cancellation priority rule.
8. Cancel, then await Done. Retain or discard previously observed results according
to an explicit caller contract; context cancellation does not undo their effects.
9. Channel rules establish defined ordering. The race detector samples actual
executions and cannot prove all future schedules.
10. Acceptable rebuilds preserve finite input/error contracts, index order and a
join signal closed after all senders exit. The supplied tests exercise30 abandoned-
output trials, all worker counts and aliasing; they are references, not learner evidence.
