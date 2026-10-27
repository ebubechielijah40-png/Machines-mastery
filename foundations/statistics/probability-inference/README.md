# Finite uncertainty, inference and evidence

Prerequisites: [algebra/functions](../../mathematics/core/01_ALGEBRA_FUNCTIONS.md)
and [sets/counting/proofs](../../mathematics/core/02_PROOFS_DISCRETE.md).
No external statistics tutorial is needed for this unit's finite experiments.
Later sections use a square root and the explicitly stated normal-score
approximation; they do not assume that an approximation is an exact theorem.

The purpose is to make a claim about a population or mechanism through an
explicit model of what could have been observed. A computed number cannot
repair a missing sampling process. We start with finite models so the relevant
outcomes, assumptions and independent checks can all be enumerated.

## 1. Outcomes, events and masses

A sample space Ω lists mutually exclusive elementary outcomes for one declared
experiment. An event is a subset of Ω. Assign mass p(ω)≥0 to each outcome,
with total mass1; event probability is the sum of its included masses. The
empty event has probability0 and Ω has probability1. Disjoint events add
because no outcome is counted twice. For overlapping events,
P(A∪B)=P(A)+P(B)−P(A∩B), subtracting the double-counted part.

Uniform masses are an assumption, not a consequence of writing a list. A
six-position selector can be modeled by {1,…,6} with masses1/6, but a worn
mechanism or unequal input generation could invalidate that model. A dataset's
rows are also not automatically independent random observations of the target
population. Logged successful requests exclude failures unless collection was
designed to retain them.

In [probability.py](probability.py), `FiniteDistribution` requires exact rational
masses summing to1. It rejects an incomplete total rather than silently
renormalizing a modeling error. Use `Fraction(1,10)` for exactly one tenth;
`Fraction(0.1)` represents the already rounded binary float. The public mass
mapping is read-only and copied from the caller. Outcomes must be hashable.
Numeric values and predicates supplied to methods are locally controlled;
this is not a service that executes untrusted functions.

## 2. Conditioning changes the denominator

Suppose the uniform selector result is known to be at least4. Only outcomes
{4,5,6} remain. Two of these are even, so the conditional even probability is2/3.
Originally the even probability was3/6=1/2. The event description changed the
available information, not the physical outcome after the fact.

For P(B)>0, conditional probability is P(A|B)=P(A∩B)/P(B). Its masses on B
are the original masses divided by P(B), restoring a total of1. In this finite
model an event of mass0 has no defined conditional distribution by this rule;
the implementation raises instead of inventing a uniform answer.

Independence means P(A∩B)=P(A)P(B). Disjointness means P(A∩B)=0. Two
positive-probability disjoint events therefore cannot be independent. For two
independent fair bits, “first bit is1” and “second bit is1” have intersection
probability1/4, exactly the product of their1/2 probabilities. Knowing the first
does not change the second. Independent tests can still share a hidden cause;
assuming independence without investigating collection can severely overstate
evidence.

## 3. Reverse a conditional through an explicit fault model

Let F mean a faulty part and + a positive detector reading. Assume P(F)=.01,
P(+|F)=.9 and P(+|not F)=.02. In a constructed batch of10,000 parts that
matches these proportions exactly, there are100 faults giving90 positives,
and9,900 nonfaults giving198 positives. Only90 of288 positive readings are
faults: P(F|+)=90/288=5/16=.3125. Sensitivity90% is not the probability of
a fault after a positive reading.

The algebra is Bayes' rule. Both P(F|+)P(+) and P(+|F)P(F) equal P(F∩+).
The total positive mass is P(+)=P(+|F)P(F)+P(+|not F)P(not F). Therefore

`P(F|+) = sensitivity*prior / (sensitivity*prior + false_positive*(1-prior))`.

The counts above are an illustrative exact model, not measured factory data.
Change the prior while holding the detector model fixed to see how deployment
population changes inference. If the detector's error rates also shift, prior
adjustment alone is inadequate. A zero denominator says this observation was
impossible under the stated model; it does not authorize returning certainty.

## 4. Random variables summarize outcomes

A random variable X is a numerical function of the outcome, not a mysterious
moving number. Its expectation is E[X]=Σωp(ω)X(ω). Grouping equal values yields
the same sum over its probability mass function. Expected values need not be
possible outcomes: a fair six-position numerical selector has mean3.5 even
though it never selects3.5.

Variance is E[(X−μ)²], μ=E[X], in squared units. Expanding gives E[X²]−μ²
in exact arithmetic, but subtracting nearly equal large floats can destroy
precision; use the [centered numerical statistics lab](../../mathematics/change-error-and-evidence/README.md)
when working with approximate measurements. For the uniform selector, E[X]=7/2,
E[X²]=91/6, so variance=35/12. A constant's variance is0. Adding an offset
does not change variance, which is why a precise biased sensor can still be
inaccurate.

For X,Y, expanding the centered square gives
Var(X+Y)=Var(X)+Var(Y)+2Cov(X,Y). Independence makes covariance0 when moments
exist, but covariance0 alone need not imply independence. If one recorded
measurement is copied n times, the mean is still that single measurement;
the copies do not provide n independent pieces of information. Under an iid
model Var(mean)=σ²/n. Without independence, covariance terms can prevent this
shrinkage entirely.

## 5. Repeated Bernoulli trials produce a binomial model

Let each of n independent trials produce failure1 with the same probability p
and success0 otherwise. A particular binary sequence containing k failures
has probability pᵏ(1−p)ⁿ⁻ᵏ. There are choose(n,k) distinct such sequences, so

`P(K=k)=choose(n,k)*p**k*(1-p)**(n-k)`.

This derives the count model from a process, including k=0,n and p=0,1.
For n=4,p=1/2, masses for k=0,…,4 are(1,4,6,4,1)/16. Thus P(K≥3)=5/16.
The implementation enumerates counts with exact rational arithmetic for
n≤1000; tests independently enumerate every binary sequence for small n.
This finite bound controls work, and is not a universal numerical distribution
library. Changing p between trials or correlated trials requires another model.

Write K=ΣX_i. A single bit has E[X_i]=p and Var(X_i)=p(1−p). Linearity of
expectation gives E[K]=np even without independence when each marginal is p.
Independence is needed for the simple sum of variances np(1−p).
For the proportion p_hat=K/n, Var(p_hat)=p(1−p)/n under the iid model.

## 6. Intervals are procedures over repeated samples

A frequentist confidence procedure maps each observed K to an interval.
At a fixed true parameter p, its coverage is
`Σ_k P_p(K=k)*indicator(p belongs to interval(k))`.
This is a property of the sampling procedure and model. After observing one
sample, this definition does not assign a95% posterior probability to its
fixed parameter; that would require a separate prior and likelihood model.

The common Wald approximation plugs p_hat into its own standard error:
`p_hat ± z*sqrt(p_hat*(1-p_hat)/n)`. At K=0 it returns[0,0], falsely suggesting
no uncertainty about a small positive failure probability. Clipping endpoints
to[0,1] cannot fix that degeneracy.

The Wilson score procedure instead asks which candidate p are compatible with
the approximate score bound
`n*(p_hat-p)**2 <= z**2*p*(1-p)`.
Expand and rearrange it to
`(n+z²)p²-(2K+z²)p+K²/n <= 0`.
Solving this quadratic produces center and radius

`center=(p_hat+z²/(2n))/(1+z²/n)`

`radius=z*sqrt(p_hat*(1-p_hat)/n+z²/(4n²))/(1+z²/n)`.

Here the standard-normal reference has density
φ(t)=exp(−t²/2)/sqrt(2π); probability over an interval is its area, rather
than its height at a point. Choosing z≈1.959964 makes the reference area
between−z and z approximately.95. Approximating the standardized binomial
count by this shape motivates a nominal95% two-sided interval. The exact
coverage experiment below does not need to assume that shape is accurate.
The normal approximation is an input assumption, not a
proof of95% coverage for every binomial p,n. For K=0, Wilson gives lower0
and upper z²/(n+z²), allowing unobserved failures. At K=n the upper endpoint
is mathematically1; the code enforces that endpoint exactly to avoid rounding
it below1 and excluding a deterministic true parameter.

`wilson`/`wald` accept1≤n≤10⁹ and .01≤z≤10 as a declared floating teaching
range. `coverage` is limited by the exact binomial enumeration bound1000.
Rational sampling masses and the target parameter remain exact. Membership is
compared exactly against the actual binary-floating endpoint values, without
rounding the target to a float first. Those endpoints still approximate the
theoretical real score/Wald formulas, especially near a boundary. A source formula
and a passing ordinary case do not remove that distinction. For n=1, Wald's
only intervals are [0,0] and [1,1], so its coverage is exactly0 for every interior
rational p, including values too close to0 or1 to retain when converted to float.

## 7. Hypothesis tests condition on a null model

If a predeclared null is p=1/2 for four independent trials, observing K=3 has
one-sided upper-tail probability P_null(K≥3)=5/16. It is the chance, under that
null process, of a statistic at least this high by this specified ordering.
It is not P(null is true|data), the observed effect's magnitude, or a chance
that the dataset was random. A direction chosen after seeing the data changes
the selection procedure and its error behavior.

For an exact two-sided permutation test, hold observed numerical values fixed
and enumerate assignments of group labels that are exchangeable under the
specified null/design. With A=[0,0], B=[1,1], the absolute difference of means
is1. Among six ways to assign two of the four labeled positions to A, two
assignments have statistic at least1. The exact p-value is2/6=1/3.
Duplicate values remain distinct positions: reducing them to a set changes
the assignment probabilities. [The implementation](probability.py) enumerates
all assignments for a total size≤16 and uses exact rational comparisons.

Equal population means alone does not make all labels exchangeable when
variances or collection mechanisms differ. A randomized controlled assignment
supports one design-based interpretation under its sharp null; a convenient
observational grouping does not establish causation by permutation alone.
State the null, assignment mechanism, statistic and tail rule before collecting
or testing. If m tests each have false-rejection chance at mostα under their
nulls, the probability of any false rejection is at most mα by the union bound;
it need not stayα. Reporting only a favorable run also changes the evidence.

## 8. Entropy connects uncertainty to model loss

Define information for a positive-probability outcome as−log₂p. Independent
probabilities multiply, while these information values add. Their expectation
H=−Σp log₂p is finite Shannon entropy in bits, taking the limit0 log0=0.
A known outcome has entropy0; four equiprobable outcomes have entropy2 bits.
Entropy is a property of a declared distribution. A long random-looking byte
string or high empirical entropy alone does not establish secure randomness.

A predictor that assigns q to outcomes has expected negative log loss
−Σp log q. It penalizes confidently assigning tiny probability to a true event.
Its value depends on the evaluation distribution p and the choice of log base;
language-model losses normally use natural logs. The training unit implements
stable finite log-softmax rather than taking a raw exponential sum that can
overflow. Low loss on leaked or unrepresentative data still fails the intended
evaluation question.

## 9. Build, investigate and assess

Python3.10+, standard library only. From repository root:

```bash
python3 -m unittest discover -s foundations/statistics/probability-inference -v
python3 foundations/statistics/probability-inference/experiment.py --output foundations/statistics/probability-inference/evidence/your-run.json
```

Follow [experiments](EXPERIMENTS.md), attempt [exercises](EXERCISES.md), then
consult [hints](HINTS.md) and [solutions](SOLUTIONS.md) separately. Reconstruct
Bayes, the binomial PMF and the coverage sum from memory before entering
[machine-learning evaluation](../../../16-machine-learning/training/README.md),
[privacy count releases](../../../13-privacy/count-release/LESSON.md), or
repeated scientific measurements. [Sources](SOURCES.md) distinguishes inspected
definitions from the original derivations and experiments.

## 10. Design decisions and stopping before interpreting evidence

Continue to [exact decision design](DECISION_DESIGN.md) after§7. It derives a
calibrated upper-binomial critical count,power at a declared alternative,bounded
minimum-n search and exact optional-stopping error using an active-count dynamic
program. A finite coupling proof controls the composite nullp≤p₀; a predeclared
alpha-spending contrast uses the union bound without treating overlapping looks
as independent. [New practice](DECISION_EXERCISES.md) and
[actual decision experiments](DECISION_EXPERIMENTS.md) connect these mechanisms
to a guided investigation and reconstruction challenge.

This unit does not complete continuous distributions,asymptotic theory,general
regression inference,causal identification,general power analysis,anytime-valid
sequential methods or dependent-process inference. Its exact finite mechanisms
and explicit counterexamples provide a verifiable foundation for those subjects.
