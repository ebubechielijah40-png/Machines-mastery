# Exercises: attempt before consulting hints or solutions

Record intermediate reasoning and a predicted output before executing code. The labels identify independently checkable tasks; completion is evidence you produce, not a property of the repository.

## Causal clocks

**L1 — trace.** A performs local a,b, then sends s to B; B receives r, then performs c. C performs independent u. List generating edges, all causal pairs, correct clock values and one timestamp comparison that does not imply causality.

**L2 — derive.** Prove the clock condition from the two generating-edge types. Give the smallest send/receive trace that breaks if receive uses `max(local,sent)` without adding one. Explain why testing strict increase on final process counters alone misses it.

**L3 — malformed evidence.** Construct duplicate message ID, wrong-endpoint and receive-before-send traces. Explain which assumptions each violates. Is an undelivered send invalid? What differs between a missing log record and an actual missing send?

**L4 — online transfer.** At one process, you have observed request `(5,B)`. May you safely emit it as the first global total-order request while A might still have an unseen request `(4,A)`? State what missing evidence prevents a decision.

**L5 — reconstruction.** Close code and notes. Rebuild a graph-reachability oracle and a clock stamper as separate functions. Generate at least one concurrent pair and one transitive pair; explain why neither function may call the other to compute its answer.

## Fourier factorization

**F1 — four-point derivation.** Using the positive-sign convention, transform `[1,2,3,4]` by the defining sum and by an even/odd split. Show each coefficient. Explain the sign of the imaginary coefficient at frequency one.

**F2 — resource count.** Derive stages, butterflies, value multiplications and complex additions for n=8 and n=256. State what the count excludes. Why can operation counts be correct while wall-clock ratios differ?

**F3 — misleading test.** A forward routine accidentally uses the negative sign and its inverse uses the opposite sign consistently. Does round-trip pass? Construct a single-frequency input that distinguishes the desired convention without using the inverse.

**F4 — transfer to nonperiodic convolution.** Multiply coefficient arrays `[1,2]` and `[3,4]`. Show why a length-two circular convolution wraps a term. Choose a valid FFT padding length that yields the linear result, and state a general minimum length.

**F5 — reconstruction and measurement.** Derive one butterfly without notes. Predict how its count changes on doubling n. Run five timing repetitions per method on identical inputs, retain all values, and identify at least two alternative explanations for one anomalous ratio.

## Task publication

**M1 — identity.** Trace s0=`red red`, s1=`blue` with completions s0/a, s1/b, s0/c. Compare naive and accepted-output totals. Prove that every completion preserves “at most one published output per logical task.”

**M2 — empty and absent.** Add an empty shard. Explain why an empty published output permits completion while an absent task does not. Change a caller's output dictionary after publication and state the required behavior.

**M3 — insufficient statistics.** A shard contains `[0]`; another contains `[10,10,10]`. Compare the true average with the mean of the two shard averages. Derive a mergeable representation that works for unequal shard sizes.

**M4 — side-effect transfer.** A task sends a notification, then publishes. Two attempts run and only one output is accepted. How many notifications can occur? Design a stronger transaction boundary or downstream idempotency scheme and identify what durable state it needs. Explain why an in-memory set is insufficient after restart.

## Analytical privacy extension

**D1 — adjacent counts.** For f(D)=0 and f(D')=1, derive the log-density ratio of Laplace outputs with scale b separately for y<0, 0≤y≤1 and y>1. Find its maximum absolute value.

**D2 — error and units.** With count sensitivity1 and ε=0.5, derive b, variance, expected absolute error and the 95% two-sided absolute-error envelope. Which quantities have count units versus squared-count units?

**D3 — histogram adjacency.** Derive L1 sensitivity for an add/remove-one histogram and a replace-one histogram when the replacement moves between bins. Why is independent per-bin sensitivity accounting needlessly loose for one histogram release?

**D4 — implementation boundary.** Derive an ideal inverse-CDF Laplace sampler using a uniform U in (0,1). What happens at U=0 or U=1? Explain why passing a histogram goodness-of-fit test does not prove differential privacy of a finite-precision release service.

## Evidence and transfer

**R1.** Classify these claims as reported, locally observed, proved within a model, or unsupported: the source's 891-second sort; a zero violation count on the saved trace; the induction over causal paths; “all networks deliver in this order.”

**R2.** A local FFT is faster at n=256. Write a conclusion that says exactly what was measured and one conclusion that would exceed the evidence. Identify the evidence needed to compare against a 1965 IBM 7094 table.

**R3.** Design a result table distinguishing a source value, its locator, your local target, raw-output path, discrepancy and next test. A blank local measurement must say “not executed,” not zero.

**R4.** Choose an unfamiliar mechanism from another domain. Define its state, transition, invariant, independent oracle, negative control and reproducibility boundary before writing its implementation. Explain which of the three completed tracks supplies a transferable method and which domain assumption does not transfer.
