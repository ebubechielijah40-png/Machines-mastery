# Dwork (2006): define the neighboring worlds before adding noise

Cynthia Dwork, **Differential Privacy**, ICALP 2006, part II. The original twelve-page manuscript is [hosted by Microsoft Research](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/dwork.pdf); its [institutional publication record](https://www.microsoft.com/en-us/research/publication/differential-privacy/) confirms author, venue and year. Source ID **D06** in the [inspection record](../../SOURCE_VERIFICATION_CONTINUATION.json) identifies the exact bytes and inspected sections. This is an original instructional reconstruction of a definition and scalar mechanism, not a transcription of a book or an implementation certified for sensitive data.

**Scope: STRONG for the bounded mathematical unit; PARTIAL for the whole paper and the privacy research domain.** The impossibility theorem's extractor construction, modern privacy accounting and implementation-level numerical privacy are outside the completed unit. The paper credits earlier work and collaborators; a single-author citation does not imply every underlying idea originated in this manuscript.

## 1. Historical context

Statistical releases need to reveal population structure while protecting contributors. D06's introduction and sections 2–3 explain why removing explicit identifiers cannot alone define the adversary's capabilities: auxiliary information can connect a useful release to a person. The source's impossibility statement has explicit distributional and utility assumptions. It is not a theorem that every possible useful statistic exposes every person's private value.

## 2. Unresolved problem

What promise can an analyst make when they cannot enumerate everything an observer already knows? A promise that nobody learns any fact about anyone would also forbid learning a genuine population regularity that applies to people outside the dataset. The engineering problem is to specify a guarantee about the release mechanism's dependence on one contributor.

## 3. Why it matters

An accurate average can be useful and still allow a known person's value to be inferred when combined with other facts. Conversely, a release containing only random bits protects contributors but teaches nothing. A valid system needs a defined neighboring relation, a privacy parameter and an explicit utility target; saying that data are “anonymized” supplies none of these.

## 4. Previous approaches

D06 discusses non-interactive sanitization, statistical disclosure limitation and interactive query answering. These are descriptions of the inspected paper's historical comparison, not independent verification of all its references. De-identification is a transformation of records; differential privacy is a quantified comparison of output distributions. Either can be implemented badly.

## 5. Limitations of the earlier goal

Consider an original toy example: a public survey correctly reports that a machine component's batch commonly fails after 300 hours. An observer also knows that a particular owner's component comes from that batch. The observer learns something about the owner even if the owner's data were never collected. Preventing all such learning would defeat the survey. Distinguish this general inference from the extra influence of one person's participation.

## 6. Research question

Can neighboring databases produce sufficiently similar observable distributions while preserving useful aggregate information? Before doing algebra, choose adjacency. In this unit neighbors differ by adding or removing one person's bounded record. A replace-one definition is different and can change sensitivity by a factor of two. Multiple rows per person require a user-level contribution bound.

## 7. Central insight

For every neighboring pair \(D,D'\) and measurable output event \(S\), require

\[
\Pr[M(D)\in S]\le e^\epsilon\Pr[M(D')\in S].
\]

Because the relation is symmetric, the reverse inequality also holds. The quantifier covers every event, not just the output mean or one attack's success rate. Smaller nonnegative \(\epsilon\) constrains the distributions more tightly. This is the definition reconstructed from D06, section 4, Definition 2.

## 8. Mathematical mechanism: sensitivity and scale

For a scalar query \(f\), define \(\Delta=\sup_{D\sim D'}|f(D)-f(D')|\). Consider \(M(D)=f(D)+Z\), where the noise has density

\[
p_Z(z)=\frac{1}{2b}e^{-|z|/b},\qquad b>0.
\]

Here **b is scale**, with the same units as the released quantity. It is not variance; integration gives \(E|Z|=b\) and \(\operatorname{Var}(Z)=2b^2\). The local notation avoids ambiguous scale/variance prose in the inspected manuscript. Its Theorem 4 expresses privacy loss as sensitivity divided by scale; derive the required scale from that relationship.

For any real output \(y\), cancel the common normalizer:

\[
\frac{p_D(y)}{p_{D'}(y)}
=\exp\!\left(\frac{|y-f(D')|-|y-f(D)|}{b}\right)
\le \exp(\Delta/b).
\]

The triangle inequality bounds the numerator of the exponent. Integrating the pointwise density bound over \(S\) proves the event bound, including intervals and unions. Set \(b=\Delta/\epsilon\) for \(\epsilon>0\). At \(\epsilon=0\), a nonconstant count cannot use any finite b to satisfy this mechanism's promise. Continuous singleton probabilities are zero; density ratios, followed by integration, are the appropriate argument.

## 9. Architecture and worked example

A contribution-bounded collector computes a query, calibrates noise using a public bound, and exposes only the noisy answer. Count one Boolean contribution per person: \(\Delta=1\). With \(\epsilon=0.5\), choose \(b=2\) people. For neighboring counts 7 and 8, at \(y\ge8\), the likelihood ratio in one direction attains \(e^{1/2}\). With b=1 it attains e and violates the desired bound. A check of sample averages would miss this exact counterexample.

The tail law is \(\Pr(|Z|>t)=e^{-t/b}\) for \(t\ge0\). Thus a 95% absolute-error envelope has half-width \(b\ln20\approx5.9915\) people. That is a probability statement about the mechanism, not a promise that any particular run is within six. For a fixed-size mean over values clipped to [0,1] under replace-one adjacency, \(\Delta=1/n\). Do not import that sensitivity into an add/remove mean with a varying denominator without a new argument.

## 10. Experimental design

The principal result is mathematical. A useful local investigation asks whether an implementation matches its stated distribution and whether an intentionally under-scaled mechanism violates the density bound. Hold adjacency, query and \(\epsilon\) fixed; vary b. Use symbolic or analytic density comparisons as the reference. Random samples can diagnose a sampler but cannot quantify over all possible outputs. Use synthetic counts only; there is no reason to expose private records during this exercise.

## 11. Baselines and metrics

The exact count is an accuracy baseline: error zero and no finite privacy guarantee for distinguishable neighbors. A constant output is a privacy baseline with poor data-dependent utility. The calibrated scalar mechanism has expected absolute error b and squared error \(2b^2\); these follow by integration. Measure violations of the analytical log-density bound, sampler goodness of fit if a sampler is added, and error at the stated contribution limit. Counting files or hiding names is not a privacy metric.

## 12. Reported findings and independently established results

**Reported:** D06, Definition 2 and Theorem 4 provide a privacy definition and sensitivity-calibrated exponential-noise result; Theorem 5 treats adaptive strategies. These are formal findings, not a benchmark table. No empirical dataset result from this source is claimed here.

**Reconstructed here:** the scalar density-ratio proof, two neighboring-count calculations and tail/error calculations above are original worked derivations. No floating-point sampler or end-to-end privacy service has been executed or certified by this dossier. The [separate assessment](../../../projects-guided/p16-research-reproduction/EXERCISES.md) contains independently checkable analytical work rather than fabricated measurements.

## 13. What the evidence supports

Under the stated add/remove contribution model, exact real arithmetic and independent Laplace noise of scale \(1/\epsilon\), a scalar count satisfies the displayed definition. Clamping a released noisy count to a public interval is post-processing: for a deterministic map g, apply the event inequality to \(g^{-1}(S)\). This derivation requires that the clamp bounds themselves do not leak private data.

## 14. What it does not establish

The result does not imply anonymity, prevent all correct inference, make the raw collector safe, or supply authorization. It says nothing about data-dependent error messages, timing, logs, random-number failures, floating-point gaps or additional unaccounted releases. Choosing \(\epsilon\) is a policy decision with contextual consequences, not a universal safe constant.

## 15. Limitations and failure modes

An unbounded sum has unbounded sensitivity. Computing a bound from the private maximum can leak information. Releasing fresh independent noise repeatedly consumes a cumulative privacy budget: for a fixed transcript of k conditional mechanisms each bounded by \(e^{\epsilon_i}\), factor the transcript likelihood and multiply to obtain \(e^{\sum_i\epsilon_i}\). Reusing one noise draw on two counts can cancel noise in their difference and needs a joint-distribution analysis. A finite grid test does not prove a universal inequality.

## 16. Subsequent developments

Modern approximate differential privacy, privacy accountants, private optimization and numerical implementation defenses require additional primary sources. They are **UNVERIFIED in this reconstruction**. They are follow-up reading tasks, not implied properties of D06 or of the toy derivation. Do not label the modern privacy curriculum complete after studying this one definition.

## 17. Reproduction requirements

For the bounded result: definitions of neighboring databases, absolute value, density, integration and the triangle inequality; no external dataset or special hardware. For a deployed mechanism: a proved contribution bound, secure randomness, an implementation-specific numerical argument, composition tracking, access controls and an audit of every observable release. These requirements are not satisfied by the paper exercise alone.

## 18. Implementation exercises

Before coding, compute the likelihood ratio for neighboring counts 0 and 1 on each of the three intervals \(( -\infty,0),[0,1],(1,\infty)\). Then derive an inverse-CDF sampler on ideal uniforms and identify why an endpoint uniform creates a logarithm singularity. Design a histogram experiment comparing add/remove and replace-one sensitivity. See exercises D1–D4 and separated [solutions](../../../projects-guided/p16-research-reproduction/SOLUTIONS.md).

## 19. Connections

Sensitivity is a worst-case stability bound on a function, while a probabilistic error bar describes repeated random outputs. The distinction connects [mathematical error analysis](../../../foundations/mathematics/change-error-and-evidence/README.md) to experimental design. A database transaction can protect raw state integrity without protecting released statistics; a transport cipher can protect bytes in transit without limiting what a recipient infers.

## 20. Open questions

Which unit of contribution matches the real privacy promise? How much useful information survives the required error? What observable side channel invalidates the mathematical model? Can a tested finite-precision mechanism implement the intended distribution? Answering these requires a defined application and further source-grounded engineering, rather than a smaller noise constant chosen to improve a demonstration.
