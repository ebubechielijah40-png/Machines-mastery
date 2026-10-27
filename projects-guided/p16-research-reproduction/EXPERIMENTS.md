# Executed experiments and extensions

The saved JSON files are actual executions on the environment they record. Inputs are original synthetic examples, not published datasets. Preserve these records when rerunning; write new results to a new filename. Exact times are observations of a particular run, not expected constants.

## E1: causal invariant under a receive-rule intervention

**Question and hypothesis.** On a fixed graph, does the correct receive rule preserve every causal pair, and do two plausible incorrect rules fail? Predict zero violations for `max(local,sent)+1`, at least one when the message is ignored, and equality on a send/receive edge when the increment is omitted.

**Controls.** Six fixed events, one message, the same independent graph-reachability oracle, counters initially zero. Only receive handling varies. There is no physical clock, live network or stochastic measurement.

**Procedure and instrumentation.** Run `python3 projects-guided/p16-research-reproduction/code/experiment.py`. It emits all events, ten causal pairs, each timestamp and each violating pair. Compare the timestamps to the hand trace before counting failures.

**Observed.** [Raw JSON](evidence/causal-clocks.json): correct rule0 violations, ignored-message5, non-strict1. Specifically send s=3 and receive r=4,1,3 respectively. Independent u has a smaller timestamp than c without a causal path.

**Interpretation and alternatives.** The negative controls distinguish a correct rule from two faults on this input. A broken graph oracle could mask a clock bug, so tests also check a known transitive closure and enumerate a small schedule family. Eighty seeded random traces broaden examples but do not replace the edge-invariant proof.

**Limit and next test.** No crash/restart or incomplete log is modeled. Extend to a restart epoch and test uniqueness; separately construct an unseen earlier request to refute a naive online sorting guarantee. These extensions are proposed, not executed here.

## E2: Fourier correctness, operation count and elapsed time

**Question and hypothesis.** Does the radix-two decomposition match the positive-sign direct sum while using the predicted value-multiplication count? Predict n² direct operations versus n log2(n)/2 butterfly multiplications. Expect small floating discrepancies, not bitwise equality. Elapsed time is a secondary exploratory measurement.

**Controls.** Seed1965, same complex input for both algorithms at each n, n=8,16,32,64,128,256; Python implementation and environment recorded. Five elapsed repetitions per method retain all samples. Root construction and interpreter overhead are included in elapsed time but excluded from value-operation counts.

**Procedure.** Run `python3 projects-guided/p16-research-reproduction/code/fft_experiment.py`. Read coefficient-error and count fields before inspecting timing. The independent oracle evaluates the defining sum; structural tests separately check sign, Parseval and circular convolution.

**Observed.** [Raw JSON](evidence/fourier.json): n256 has65536 direct value multiplications versus1024 butterflies. Its maximum absolute coefficient discrepancy is approximately1.50×10^-12 in the saved run. All five elapsed samples and their median remain in the JSON; rerunning changes them.

**Interpretation and alternatives.** Counts confirm the implemented loop structure on these sizes; the derivation supplies its general radix-two recurrence. Different summation order, trigonometric root rounding and accumulated arithmetic account for plausible error differences. The direct oracle also rounds. Warm-up, scheduling, allocation and different Python control flow can affect timing ratios.

**Limit and next test.** This is neither the original Fortran program nor IBM7094 performance. Input range is bounded to4096 in reference code and only small powers of two were measured. Follow up with cancellation-heavy inputs and a higher-precision independent oracle; randomize algorithm execution order for a stronger timing comparison. These follow-ups are unexecuted.

## E3: duplicate attempt versus logical task output

**Question and hypothesis.** Can retrying a deterministic shard alter the count? Predict that summing attempts double-counts red while accepting one output per task preserves the sequential result. Also predict that an effect outside the publication boundary can still happen twice.

**Controls.** Fixed shards s0=`red red` and s1=`blue`; completion order s0/first,s1/second,s0/backup. Same whitespace tokenizer and outputs; only aggregation rule varies. The synthetic notification list records effects outside publication.

**Procedure.** Run `python3 projects-guided/p16-research-reproduction/code/publication_experiment.py`. Inspect per-attempt acceptance, sequential oracle, naive total, accepted total and external-effect list.

**Observed.** [Raw JSON](evidence/publication.json): accepted flags true,true,false; naive red4/blue1; accepted red2/blue1; notifications for s0 appear twice. Tests additionally enumerate24 completion orders and50 seeded generated jobs against a sequential oracle.

**Interpretation and alternatives.** A task-identity publication boundary controls output inclusion, not execution count. If a map is nondeterministic, different winning attempts can yield different results; a test includes that counterexample. A real shared-state race or lost accepted output is absent from this single-process model.

**Limit and next test.** No real worker failure, network, atomic rename or durable coordinator exists. A next experiment would add persistent task generations and inject process loss between output write and publication; a separate transaction would investigate external effects. Neither has been executed in this project.

## Reporting practice

Every new run should retain question, pre-run prediction, controls, command, environment, input or seed, all raw measurements, interpretation, alternatives and limitations. Keep source-reported results in a different field from your measurements. Never fill an unexecuted result with a predicted value.
