# Experimental research practicum: a claim ledger with executable evidence

This practicum connects [the research coursebook](../coursebooks/11-research.md) to [project16](../projects-guided/p16-research-reproduction/README.md). It teaches one complete investigation cycle, not every research design. The reference materials are STRONG for finite computational mechanism studies; the wider phase remains PARTIAL. Learner completion is not assumed.

## 1. Construct a claim ledger

Begin with the smallest claim that has observable consequences. A paper's title is too broad to reproduce. The following ledger is filled from actual local work and inspected primary sources.

| Source and locator | Source claim type | Local target | Completed evidence | Scope boundary |
|---|---|---|---|---|
| L78, pp558–560, clock condition and logical rules | formal causal-order property | timestamp every finite trace edge consistently | hand trace, independent reachability,80 generated traces and two bad-rule controls | no online ordering or physical clock |
| CT65, pp297–300, transform factorization | mathematical algorithm and operation cost | radix-two positive-sign transform | direct definition, known signals, Parseval, convolution and loop counts | no original source program or historical performance |
| DG04, section3.3, failure semantics | distributed system behavior under assumptions | deterministic duplicate-attempt output acceptance |24 completion orders,50 generated jobs, output snapshots and external-effect counterexample | no network, persistent state or cluster |
| D06, Definition2 and Theorem4 | distributional privacy guarantee | scalar count proof | original density-ratio derivation and analytical exercises | no production privacy service |

Exact versions, hashes, authors, links, inspection access and licensing limits are in the [source record](../research-paper-reconstruction/SOURCE_VERIFICATION_CONTINUATION.json). Source statements and original local deductions are labeled in each dossier. No copied full text or paper figures are bundled.

Now write a ledger for a new claim. It must identify a falsifying observation and an independent way to recognize it. A missing source or unavailable dataset is a bounded blocker for the relevant claim, not permission to invent its results.

## 2. Work one investigation completely

Question: does increasing every process's local counter preserve message causality? The intended property is “send precedes its matching receive numerically,” including transitive local dependencies. The competing explanations are that local increment suffices, or that receipt must incorporate the sent counter.

Construct A-local a,b,send s; B-receive r,local c; independent C-local u. Before running, write the graph a→b→s→r→c and isolated u. With local-only updates, A reaches3 at s while B starts1 at r. This predicts a violation s3≥r1. With receive=max(local,sent)+1, predict r4,c5. A third intervention receive=max(local,sent) predicts equality s3=r3, exposing why strictness matters.

Run `python3 projects-guided/p16-research-reproduction/code/experiment.py`. The saved [actual result](../projects-guided/p16-research-reproduction/evidence/causal-clocks.json) contains zero, five and one causal-pair violations for the correct, local-only and non-strict rules respectively. Five failures for local-only include transitive pairs; counting only s→r would report one and miss the broader downstream effect.

Interpretation: the input distinguishes the three transition rules. The independent graph oracle prevents the clock from defining its own correctness. The edge argument proves the universal property under the model; finite tests check the specific program. Neither establishes behavior of an unobserved real network, crash recovery or a complete synchronization protocol.

## 3. Design experiments as comparisons of predictions

For every intervention, list the quantities held fixed and the mechanism changed. In the clock study, fixing the graph isolates receive handling. In the publication study, fixing shards and changing whether attempts or logical tasks are counted isolates identity. In the FFT study, the algorithms differ in many implementation costs, so elapsed time supports an end-to-end code comparison on that workload, not an isolated estimate of one complex multiplication's cost.

A negative control should fail for the expected reason. A silently corrupted input that crashes a program tests validation, not the algorithm's invariant on valid inputs. Keep these separate. Likewise, a test with the wrong expected value can falsely accuse correct code; verify the oracle through hand cases and another independent structure where practical.

Predeclare the target and analysis before inspecting results. Exploratory work is still useful when labeled exploratory. If a surprising result leads to a new hypothesis, preserve the discovery run and test the new hypothesis on a fresh, specified run rather than presenting the discovery as a preplanned confirmation.

## 4. Build a measurement chain

A measurement is an output of an apparatus with a specified relationship to a quantity. The FFT experiment's timer observes elapsed nanoseconds around a complete Python call. Its operation counter observes loop butterflies. Neither measures a physical signal's frequency. To assign cycles per second to a DFT bin, a sampled signal also needs an acquisition interval in seconds and a convention for positive/negative frequencies.

The saved [FFT evidence](../projects-guided/p16-research-reproduction/evidence/fourier.json) retains every one of five timing repetitions per method and size. At n256 the direct routine performs65536 value products and the FFT1024 butterflies; these counts follow the code and match the derivation. Approximately1.50×10^-12 maximum coefficient difference in that run reflects two floating evaluation paths, not a universal error tolerance for every input scale.

Distinguish resolution, repeatability and bias. A timer can have nanosecond units while system scheduling varies by much more. A sensor can repeatedly return the same biased value. Averaging reduces some random variability under assumptions; it cannot remove a fixed calibration offset or reconstruct unrecorded failures.

For a physical extension, a proposed experiment might compare a sampled sinusoid's DFT peak with a known source while varying sampling rate. That experiment has **not been executed here**. It would require calibrated source frequency, capture timing, aliasing controls, amplitude/window conventions and acquisition uncertainty. A simulated tone validates software conventions; it cannot validate the physical instrument.

## 5. Analyze failures without changing the target

Use the smallest counterexample to locate a discrepancy. A reversed FFT sign can pass round-trip but fail a known tone; a repeated task can pass clean-run tests but fail the duplicated-completion trace; a non-strict clock can be monotone within each process yet fail a message edge. Each failure points to a specific omitted constraint.

Do not hide differences with an arbitrary tolerance. First reconcile mathematical definitions, units, input identity and source version. For floating calculations, then vary input scale or precision and compare an independently derived reference. For noisy timing, retain all samples, control execution order and machine load as far as possible, and explain remaining confounding.

Do not relabel a planned experiment as an actual observation. A benchmark that was not run must have a “not executed” status even if its expected trend is obvious. A missing compiler or dataset is a real limitation; passing a structural validator does not supply the missing scientific result.

## 6. Make the result reviewable

A minimal result package contains the ledger, derivation, inputs or generator/seed, implementation, independent tests, exact commands/environment, unedited raw results, interpretation, alternatives and limits. Put hints and solutions after the learner attempt. The [project test record](../projects-guided/p16-research-reproduction/TESTS.md) links actual unittest output and three executed JSON files.

A review should ask: are the mathematical conventions consistent; does the oracle share the suspected bug; did the negative control fail; is a reported number traceable; does a local conclusion exceed its apparatus? These questions assess educational and technical evidence rather than file count. A reviewer can classify a bounded mechanism STRONG while leaving a whole domain PARTIAL.

The final learner assessment is project16 exercises R1–R4 plus one mechanism track reconstructed from memory. Transfer to a new domain only after declaring its own state, invariants, measurements and failure modes. A graph proof method transfers; assumptions about message delivery do not become assumptions about genes, sensors or quantum hardware merely because the same programming language implements the model.
