# Design a decision before collecting its evidence

The earlier [finite probability lesson](README.md) explains binomial counts,
confidence coverage and p-values. This investigation closes another loop:
**choose a decision rule, derive its false-alarm behavior, measure its detection
ability, and check how changing the stopping rule changes that behavior.**

Prerequisites are exact fractions, binomial masses, conditional probability,
finite sums and a loop invariant. Read the preceding lesson through§7 first;
no normal approximation, optimization library or new calculus is required here.
The experiment is an exact synthetic model, not advice for operating a factory,
conducting a real trial or interpreting an unexamined dataset.

## 1. A process question becomes a statistical decision

Suppose a local fault injector emits one binary outcome per independent trial.
Let1 denote a fault and assume an unchanged fault probabilityp on every trial.
We want evidence thatp is **greater** than a declared acceptable boundaryp₀.
The null isH₀:p≤p₀; the alternative isH₁:p>p₀. These statements concern a
probability parameter in the model, not the truth of a particular observed bit.

Before observing results, declare the trial countn, direction, statistic
K=number of faults, null boundaryp₀ and false-rejection budgetα. A nonrandomized
upper-count rule rejectsH₀ whenK≥c. The count model has masses

\[
P_p(K=k)=\binom nk p^k(1-p)^{n-k},\qquad
T_p(c)=P_p(K\ge c)=\sum_{k=c}^{n}P_p(K=k).
\]

An upper-tail p-value for an observedk isT_p₀(k). It describes tail probability
**under the null boundary model**, notP(H₀|data). Choosing the upper tail after
seeing that an observed count is unusually high changes the predeclared testing
procedure; that choice must be included when evaluating false alarms.

Select the smallestc for whichT_p₀(c)≤α. We also permitc=n+1, a rule that
never rejects, sinceT_p(n+1)=0. For mathematical boundary tests,α=1 permits
c=0, which always rejects. Ordinary experimental design uses an informative
α between those extremes; the endpoints are tested to make the API unambiguous.

Why the smallest validc? Increasingc removes rejection outcomes and can only
decrease detection probability. Among these upper-threshold rules, the smallest
one satisfying the error budget has greatest power at everyp>p₀. This is a
statement about this declared rule family, not a claim of universal optimality
among all statistical procedures.

## 2. Work the exact threshold and prove the composite-null control

Forn=5,p₀=1/2, the binomial numerators are1,5,10,10,5,1 over32.
Atc=3, the upper tail is16/32=1/2. Atc=4 it is6/32=3/16. Atc=5 it is1/32.
Ifα=1/4, the smallest valid critical count isc=4, with actual size3/16.
Ifα=1/20, the chosen count isc=5 and size1/32, below.05. A finite count space
usually cannot spend exactlyα without randomizing a boundary; this unit does
not implement that additional mechanism.

Calibrating atp₀ must also control everyp≤p₀ in the composite null. Here is a
finite coupling proof. For each trial construct a three-category variable with
masses(p,p₀-p,1-p₀). SetX=1 only in the first category; setY=1 in the first
or second. ThenX has Bernoulli probabilityp,Y has probabilityp₀, andX≤Y
for every category outcome. Take independent copies acrossn trials. Their
counts satisfyK_p≤K_p₀ on every joint path. Thus

\[
\{K_p\ge c\}\subseteq\{K_{p_0}\ge c\},\qquad
P_p(\text{reject})\le P_{p_0}(\text{reject})\le\alpha.
\]

This proves the upper-tail claim under the specified iid Bernoulli model.
It does not show that observed faults are independent, that a drifting process
has constantp, or that a biased collection system records every fault.
Those questions require measurement/design evidence outside a tail calculation.

## 3. Power requires a specified effect

The test's size is its rejection probability atp₀. Its power at a specified
alternativep₁>p₀ isπ(p₁)=T_p₁(c); its miss probability there isβ(p₁)=1-π(p₁).
The effect size here is the absolute proportion changep₁-p₀. A power target
has no single meaning without specifying that alternative and sampling model.

For the n=5,α=.05 rulec=5, power atp₁=.7 is(.7)⁵=.16807. So false alarms
are at most5%, yet this small design misses that alternative more than83% of
the time. A failure to reject cannot validate the null or prove practical equality.
It may simply mean the design lacks information about the effect of interest.

Do not confuse three different denominators:

| Quantity | What is held fixed / varied? |
| --- | --- |
| p-value | Observed statistic fixed; integrate more-extreme hypothetical outcomes under the null boundary |
| Size | Parameterp₀ fixed; average the rejection decision over all hypothetical samples |
| Power | Parameterp₁ fixed; average the same decision over samples from that alternative |

None is a posterior probability without a prior model. A confidence interval,
effect estimate and domain-specific cost analysis answer additional questions.

## 4. Plan a bounded smallest sample, including discreteness

To find the smallestn with at least80% power atp₁, inspectn=1,2,… in order:
derive thatn's critical count underp₀/α, compute its power atp₁, and stop at
the first success. Every earlier failed size is retained as the minimality
evidence. A configured maximum bounds work; not finding a design within it
does not establish that no larger design could work.

It is tempting to use binary search on sample size. That assumes monotone power
at every integern, which this discrete rule does not have. Atp₀=.5,α=.05:
n=5 hasc=5 and power.7⁵=.16807; n=6 hasc=6 and power.7⁶=.117649. Adding one
trial made the critical rule stricter and reduced power. Long-term improvement
does not justify a false local monotonicity assumption.

The [actual exact search](DECISION_EXPERIMENTS.md) finds, forp₀=.5,α=.05,
target.8, minimum sizes158 atp₁=.6,37 atp₁=.7,18 atp₁=.8. These are conditional
outputs for this one-sided test family, not recommended real-world sample sizes.
Changing the alternative, error budget, missingness, dependence or stopping rule
changes the design problem.

## 5. Optional stopping changes the event being tested

Now inspect each prefix of a sequence through horizonN and stop at the first
upper-tail p-value≤α. Each fixed look has size≤α, but the overall rejection
event is a **union over looks**, not the final test's event. These tests overlap:
the same first bits occur in later prefixes. Independence across looks cannot
be assumed, so1-(1-α)ᴺ is not a justified exact calculation here.

Atp₀=.5,α=.05,N=10 the first-crossing mass can be counted by hand.
The first possible rejection is five initial ones, with mass1/32. The only
new crossing later occurs atlook8: seven ones and one zero, with that zero in
one of the first5 positions. Those5 paths each have mass1/256; a zero after
position5 would already have crossed atlook5. There are no new crossings at
looks6,7,9,10. Equivalently, bylook8 the union of first5ones andK₈≥7 has mass
1/32+9/256-1/64=13/256, subtracting their overlap. Therefore ever-reject probability is

\[
1/32+5/256=13/256=.05078125>.05.
\]

Each individual p-value calculation is correct; the interpretation of the
selected first significant prefix as a single5% procedure is incorrect.
More looks can increase the discrepancy: actualN=100 gives.2020580979 in
this model. This is a counterexample to a blanket validity claim, not a claim
that every sequentially designed test is invalid.

## 6. Derive the first-crossing dynamic program

Enumerating all2ᴺ bit strings is possible only for smallN. Many prefixes share
the same sufficient future state: lookt, countk, and whether a rejection already
occurred. Once a path has crossed, remove it from active mass so it cannot be
counted again. LetA_t(k) be mass of un-rejected paths withk ones aftert trials.
InitializeA₀(0)=1. Before applying lookt's boundaryc_t, propagate

\[
B_t(k)=(1-p)A_{t-1}(k)+pA_{t-1}(k-1),
\]

taking missing entries as0. Set first-hit mass
\(h_t=\sum_{k\ge c_t}B_t(k)\), and keepA_t(k)=B_t(k) only fork<c_t.
Then

\[
\sum_{j=1}^{t}h_j+\sum_k A_t(k)=1.
\]

Every transition distributes its old mass into exhaustive bit0/bit1 cases;
the boundary partitions candidates into hit/survival without overlap. Induction
therefore proves conservation and the first-hit interpretation. The final
ever-rejection probability isΣh_t. Simply adding fixed-look tail probabilities
double-counts paths and computes a different quantity.

[decision.py](decision.py) stores only active count masses and records first-hit
and survivor totals. It uses the preceding exact `binomial` mechanism to derive
boundaries, not a high-level testing package. Independent tests enumerate complete
binary paths through at most8 looks and classify each path's first crossing;
their oracle hard-rejects requests above12 to prevent accidental exponential work.
Additional hand counts supply an independently checkableN=10 contrast.

## 7. A predeclared spending policy

For a fixed horizonN, assign each lookα/N instead ofα. Each look then has null
rejection probability at mostα/N. The union bound gives
P(any rejection)≤ΣP(rejection atlookt)≤Nα/N=α. This bound requires no
independence between looks. The coupling argument also controls allp≤p₀.

This simple policy is often conservative with discrete counts and overlapping
looks. Spending more carefully, likelihood-ratio methods and confidence sequences
are separate sequential methods; this unit does not claim to implement them.
The fixed horizon and allocation must be chosen before looking. ChangingN or
trying multiple policies after inspecting the outcomes changes the procedure.

The experiment compares three fixed policies on the **same**p₀=.5 andα=.05:
`final` tests only once atN; `repeat` spendsα at every prefix; `spend` assigns
α/N to every look. This isolates the stopping/threshold rule. It does not compare
different devices, treatment effects or data-generating processes.

## 8. Numeric contract, costs and failure boundaries

The public input limit is1≤n,N≤200, with rational probability numerators and
denominators at most64bits; booleans are rejected. Exact Fraction arithmetic
preserves all derived probabilities. Inputs such as`Fraction(1,20)` encode
the intended.05 exactly; `Fraction(.05)` instead encodes its binary-float value.
The spending allocation is derived after validation and can add at most8
denominator bits. Outputs can be much larger rationals than the inputs.

The dynamic program attempts at mostN(N+1) bit transitions and retainsO(N)
count states plusO(N) recorded totals. Boundary construction and planning inspect
a quadratic number of binomial-mass terms over their bounded horizon. Exact
integer arithmetic has growing bit costs; these are not constant-time machine
word operations or a hard runtime guarantee. The budget bounds ordinary trusted
local work, not construction of hostile objects before validation or a sandbox.

Use `upper_test` to construct a calibrated rule. `UpperTest` also validates a
manually constructed record's numerical ranges, including0≤c≤n+1; a manually
supplied size does not certify calibration. c=n+1 means no possible observed count
rejects. `reject(k)` accepts only integer0≤k≤n. `minimum_n` returns a selected
rule orNone with every evaluated operating point; None means only not found
within the bound. These mechanisms do not diagnose a real sampling process,
select practical loss costs, or turn statistical association into causation.

## Guided investigation and reconstruction

Build in six milestones: derive the5-trial count table; write the tail sum and
critical-count selection; calculate power at a specified alternative; search
sample sizes in order; implement active-state first-crossing DP; add the spending
contrast and conservation check. Predict each result before opening the code.

From repository root, with Python3.10+ standard library:

```bash
python3 -m unittest discover -s foundations/statistics/probability-inference -v
python3 foundations/statistics/probability-inference/decision_experiment.py
```

Attempt [new exercises](DECISION_EXERCISES.md), then consult
[hints](DECISION_HINTS.md) and [solutions](DECISION_SOLUTIONS.md) separately.
Deliver a declared null/direction/model, a hand threshold calculation, your
implementation, an independent path oracle, exact raw operating curves, a
stopping counterexample, and a limits paragraph. Rubric: derivation and
interpretation25%; implementation/boundaries25%; independent experiment25%;
prerequisites, unaided reconstruction and transfer25%. Passing code without
explaining what probability its output represents does not pass the assessment.

Close the source and rebuild the count-tail rule plus first-crossing recurrence.
Then deliberately sum overlapping tails and explain the failure using one
repeatedly counted path. Transfer to a declared local software-fault experiment
by specifying collection, iid assumptions, relevant effect and stopping policy
before running it. [Sources](DECISION_SOURCES.md) and
[actual observations](DECISION_EXPERIMENTS.md) separate primary verification,
original derivations and executed model results.
