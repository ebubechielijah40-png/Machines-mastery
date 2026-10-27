# Research: turn a claim into a checkable investigation

A research result connects a question, a model, a method and evidence. The work is to discover which conclusions survive explicit checks. This coursebook teaches that process through three local reconstructions: [causal clocks](../research-paper-reconstruction/domains/distributed-systems/01_lamport_clocks_1978.md), [Fourier factorization](../research-paper-reconstruction/domains/scientific-computing/01_cooley_tukey_1965.md) and [duplicate task publication](../research-paper-reconstruction/domains/data-systems/01_mapreduce_2004.md). Their code, independent tests and actual synthetic observations are in [project16](../projects-guided/p16-research-reproduction/README.md). No historical hardware or cluster result is claimed as reproduced.

Prerequisites are [functions](../foundations/mathematics/core/01_ALGEBRA_FUNCTIONS.md), [relations and proofs](../foundations/mathematics/core/02_PROOFS_DISCRETE.md), basic programming and the ability to preserve raw data. Read [finite probability](../foundations/statistics/probability-inference/README.md) before interpreting confidence procedures or hypothesis tests. The aim is not to memorize a universal checklist: it is to build an experiment whose observations distinguish specific competing explanations.

## 1. Start with the claim's quantifiers

“Clocks order events correctly” is underspecified. Which events, which order, under which communication model? The bounded causal claim is: for every valid trace and every pair linked by local order, a send/receive edge or their transitive closure, the assigned integer strictly increases. It does not say that a smaller integer proves a causal link. It does not describe seconds.

Write the claim as `assumptions → property`, then seek a smallest counterexample to a stronger reading. A has events a,b,s; s sends to B, which receives r and performs c. A separate process C performs u. Correct logical values are a1,b2,s3,r4,c5,u1. The inequality u1<c5 holds, but no causal path links u and c. This single construction refutes the converse without refuting the actual one-way claim.

A useful research question identifies what observation would change your mind. “Can I implement clocks?” is a build objective. “Does local-only receive counting preserve send-before-receive on a fixed trace?” is an investigable mechanism question. Its negative control predicts r1<s3. The prediction precedes the run so it cannot be rewritten to match any outcome.

## 2. Separate model, algorithm, implementation and apparatus

A model defines valid states and observations. For the clock lab, process order and message matching generate a directed graph. An algorithm assigns counters. An implementation represents those rules in Python. The apparatus runs it on a specific interpreter and records outputs. A failure may occur at any layer.

Suppose a clock test passes because its oracle defines causality by sorting the same clock values. The implementation and test agree, but neither checked the desired relation. Replace the oracle with graph reachability built from message and process edges. First test that oracle on a hand-known closure. Independence is a structural property of the evidence, not a different function name.

For the Fourier lab, the defining sum is the model, even/odd factorization is the algorithm, staged butterflies are the implementation and the timer is apparatus. A forward/inverse round-trip can pass when both routines use the opposite sign convention. A known complex tone or direct sum distinguishes this shared mistake. A timer cannot diagnose a sign error; an exact operation count cannot characterize operating-system scheduling noise.

## 3. Inspect the source you actually cite

Record title, all authors, venue/year, exact version or file hash, host, inspected section/table/equation, access date and licensing limits. A landing-page abstract establishes metadata and a summary, not the content of an unseen theorem or benchmark. A readable university scan of an original paper is still the primary text; the host's existence does not confer an open redistribution license.

The [continuation source record](../research-paper-reconstruction/SOURCE_VERIFICATION_CONTINUATION.json) distinguishes obtained PDF bytes from the claims actually inspected. The source PDFs and full extracted texts are not bundled. Local instruction uses original explanations, derivations and examples. A later paper listed in a bibliography remains unverified until its original is inspected.

Build a claim ledger with columns `claim`, `source locator`, `assumptions`, `local target`, `evidence type`, `limitation`. For the MapReduce paper, its terabyte sort timing is a reported source result; our local target is accepting one output per logical task. These are related at the mechanism level but cannot be divided to obtain a speedup. For theoretical work, an independently reconstructed proof can be the appropriate evidence even when there is no empirical result table.

## 4. Derive before measuring

Consider deterministic shard outputs m_i(w), where i is a logical shard and w a word. Desired total is `C(w)=Σ_i m_i(w)`. If A_i attempts finish for shard i, naive aggregation gives `Σ_i A_i m_i(w)`. That is a different expression unless every A_i equals one or the extra terms vanish.

A publication rule accepts one completion per logical shard. With indicator I_i,a and `Σ_a I_i,a=1`, summing accepted deterministic outputs returns C. This derivation identifies the invariant and two essential assumptions: all logical tasks eventually publish, and attempts for one task produce equal output. A dictionary keyed by attempt ID would violate the intended identity boundary even if its code had no syntax errors.

Now construct s0=`red red`, s1=`blue`, with s0 retried. The prediction is naive red4/blue1 and accepted red2/blue1. The executed [publication record](../projects-guided/p16-research-reproduction/evidence/publication.json) has those results. It also shows duplicate synthetic notifications outside the publication boundary. That observation prevents “one accepted output” from being promoted to “exactly-once external effects.”

## 5. Design controls around an alternative explanation

A control is useful when it makes a competing explanation produce a different prediction. In the clock lab, hold graph and oracle fixed while changing receive handling. This isolates a specific transition rule. In a performance study, holding the input generator fixed helps compare algorithms, but always running one first can confound algorithm choice with warm-up or machine drift.

Use negative controls that should fail and positive controls with known answers. The FFT constant sequence should concentrate at coefficient0. A single complex tone should concentrate at its predicted signed frequency. A wrong sign may leave the constant case unchanged, so one positive example is insufficient. A non-power-of-two input should reject under this restricted algorithm's contract; silently padding it would change the defined task.

A random seed makes one generated experiment replayable; it does not prove the generator represents a population. Multiple traces generated by the same flawed model can repeat the same omission. Combine generated cases, boundary cases, an independent oracle and a proof where feasible.

## 6. Measure the quantity the claim names

Declare units and the observation boundary. Elapsed time includes root generation, allocation and interpreter overhead in the local FFT experiment. Its operation counter excludes those and counts butterfly value multiplications. Both measurements are valid when named accurately; they answer different questions.

A length-n radix-two transform has log2(n) stages and n/2 butterflies per stage. At n256 that is1024 butterflies, compared with65536 value products in the direct definition. The [raw experiment](../projects-guided/p16-research-reproduction/evidence/fourier.json) preserves coefficient errors and five time samples per method. A median describes these samples; it is not a confidence interval, a hardware-independent constant or a universal guarantee.

For a physical measurement, additionally identify sensor resolution, calibration, sampling interval, environmental conditions and systematic offsets. Repeating a biased sensor can yield a small spread around the wrong value. For a software timer, dispatch noise and shared machine load can change elapsed time while leaving the arithmetic invariant untouched. Explain which errors repetition can reduce and which need a different calibration or model.

## 7. Uncertainty is attached to a sampling process

Suppose an independent Bernoulli model declares four trials with failure probability1/2. The count masses are `(1,4,6,4,1)/16`, so three or more failures have probability5/16. This exact calculation follows from counting the16 possible binary sequences. It is not the probability that the model is true after observing three failures.

A confidence procedure maps each observed count to an interval. At fixed p, its coverage sums the binomial masses of counts whose intervals include p. The [probability lab](../foundations/statistics/probability-inference/README.md) enumerates this finite sum instead of assuming nominal coverage is exact. The Wald interval at zero observed failures collapses to zero width, illustrating how a familiar formula can misrepresent uncertainty at a boundary.

Do not treat repeated timing samples as independent merely because they occupy different rows. Warm-up, cache state, sustained load and shared processes can correlate them. Declare the experimental unit and collection scheme before attaching an uncertainty formula. For exploratory results with only five samples, retaining all observations and stating the limited design is often more honest than presenting a spurious precise interval.

## 8. Preserve discrepancy instead of tuning it away

Classify a disagreement before changing the implementation:

| Mismatch | Discriminating check |
|---|---|
| definition/convention | reconcile sign, normalization, units, adjacency or identity |
| implementation | smallest failing input, independent oracle and state trace |
| numerical arithmetic | higher precision or scale sweep with the same mathematical target |
| source/version | compare exact equation/table and preserve any disagreement |
| apparatus/environment | repeat with recorded versions, input and timing boundaries |
| unsupported generalization | construct a counterexample outside the observed case |

If an FFT inverse produces the expected input but a tone lands at the wrong index, investigate convention before relaxing a tolerance. If a task result changes with the winner, inspect determinism and input version before adding a retry. If source text and a source table differ, record both locations; silently choosing the convenient number hides evidence.

A failed reproduction can be useful when its target, artifacts and limitations are precise. “Could not reproduce” without a matching setup is not proof that a paper is wrong. “Tests pass” without an independent specification is not proof that it is right.

## 9. Communicate conclusions at their supported scope

A defensible result states what was predicted, what ran, what was observed, what supports the interpretation and what remains unresolved. Use separate fields for source-reported values, locally measured values, mathematical deductions and proposed experiments. Leave unexecuted measurements labeled “not executed.”

For the clock example: the local correct rule produced zero violations on the saved six-event input; two deliberate faults produced violations; the generating-edge argument proves the condition under the model. These three statements support different levels of inference. None establishes consensus, real-time deadlines or behavior of an uninstrumented network.

Complete [project16 milestones and assessment](../projects-guided/p16-research-reproduction/CHECKPOINTS.md), including memory reconstruction and an unfamiliar transfer case. Then choose a new domain, inspect an original source and rebuild its claim ledger, mechanism, oracle and experiment. This coursebook and the [phase practicum](../19-experimental-research/SELF_CONTAINED_GUIDE.md) are STRONG for this bounded research method; research-paper breadth, advanced experimental design and domain-specific source reconstructions remain incomplete.
