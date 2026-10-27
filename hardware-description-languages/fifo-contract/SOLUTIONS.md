# Reference checks

1. Empty push12/pop gives no consumed word and new queue[12]. Full[4,7,9] with
push12/pop consumes4 and yields[7,9,12].
2–3. At0, no pop; atDEPTH, push requires pop; inside, n can change by at most1.
These cases prove the displayed invariant by induction from reset.
4. Visible queues are[1],[1,2],[1,2,3],[2,3],[2,3,4],[3,4],[4],[]. Final occupancy0.
The physical pointers wrap at2→0 independently of a two-bit integer's capacity.
5. Two-bit truncation wraps3→0 but still permits address3, outside cells0..2.
6. Inactive cells are never returned as valid queue words; logical reset discards
membership. Physical residual data can remain, so confidentiality needs erasure
or a separate memory-isolation argument.
7. Nonblocking/signal assignments read old count; the last assignment can win.
At simultaneous push/pop, n must stay unchanged. The runner's count mutant fails
that specific observation in both actual simulators.
8. Compute take_pop := predicate on old count, then take_push := predicate using
that variable. Schedule pointer/memory/count signals with <=. Reading an assigned
signal immediately can still see its prior value; := updates the local variable.
9. When pop_fire is true, the consumed value is the old combinational head at the
edge. Compare that with the independent queue's popleft result before inspecting
the new output. A post-edge value alone names the new head, not the transfer.
10–11. New parameters/latency require a parameterized bench and changed expected
interface timing. No unexecuted extension result is supplied as a solution.
12. Pass requires a derived contract, safe range/wrap behavior, reset priority,
independent observation tests and a clear boundary between functional simulation
and physical timing. Reference source alone is not a learner reconstruction.
