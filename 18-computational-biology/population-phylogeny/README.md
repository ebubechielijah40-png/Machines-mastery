# From aligned strings to population dynamics and tree assumptions

The [alignment unit](../02_SEQUENCE_ALGORITHMS.md) optimizes a correspondence
between recorded strings. An optimum score is not an observed ancestry, a fitness
measurement or an evolutionary clock. This unit adds two explicit models: finite
sampling of gene copies across generations, and substitution distances used by a
clock-based tree algorithm. Every dataset below is original and synthetic. No
organism, patient, clinical prediction or wet-lab experiment is involved.

Start with [molecular terms](../01_MOLECULAR_FOUNDATIONS.md), the alignment lesson,
and basic fractions, probability and expectation. A probability is a weight in
[0,1]; an expectation Σp_i x_i is a weighted mean across possible outcomes, not a
promise for one outcome. Variance is Σp_i(x_i−mean)². The local
[probability/inference path](../../foundations/statistics/probability-inference/README.md)
provides the deeper prerequisite if these operations are unfamiliar.

## 1. Define what is being counted

A locus is a genomic position or region; an allele is a sequence variant at that
locus. Let A/a name two alleles, not necessarily the DNA letters A and a. In an
ideal diploid autosomal population of N individuals there are m=2N gene copies.
Let X_t be the count of allele A in generation t, and P_t=X_t/m its frequency.
Counts have units gene copies; frequency is dimensionless; t counts generations,
not seconds or calendar years. The code names m explicitly to avoid silently
confusing individuals with copies.

Our neutral model assumes fixed m, discrete nonoverlapping generations, random
sampling of each next-generation copy with replacement from the old population,
no mutation/migration/selection and no additional family structure. Those are
model premises, not claims that real reproduction is independent at every locus.
Biological drift is chance change in allele frequency; selection is not needed
for a variant to disappear. The source map records inspected NHGRI definitions
and author teaching material, including one correction to a source's notation.

## 2. Derive the transition law from independent draws

Given current count i, each next-generation draw is A with p=i/m. A particular
ordered outcome with j A copies has probability p^j(1−p)^(m−j). There are
C(m,j)=m!/[j!(m−j)!] ways to choose their positions. Summing gives

\[
\Pr(X_{t+1}=j\mid X_t=i)={m\choose j}(i/m)^j(1-i/m)^{m-j}.
\]

The transition depends on the present count, not the whole earlier history:
this is a finite Markov chain. Store an entire row for each current i. Each row
sums to(p+(1−p))^m=1 by expanding the product of independent choices. At i0 the
next count is always0; at im it is alwaysm. Those states are absorbing because
an absent allele cannot reappear without a mechanism such as mutation or migration.

**Complete small example:** m4,i2 gives p.5 and the row
`[1,4,6,4,1]/16` for next counts0,1,2,3,4. Mean count is
(0+4+12+12+4)/16=2. Second moment is(0+4+24+36+16)/16=5, so count variance1;
frequency variance1/16=.0625. There is1/16 probability of immediate fixation,
1/16 immediate loss and14/16 of remaining polymorphic. None is excluded by the
unchanged mean. An average population is not an actual population.

For independent Bernoulli variables B_k, E B_k=p and Var B_k=p(1−p). Cross-covariances
are zero, so E X'=mp and Var X'=mp(1−p). Dividing by m² gives
E[P'|p]=p and Var(P'|p)=p(1−p)/m. Smaller populations have larger frequency
fluctuations, not a preferred direction under neutrality.

## 3. Diversity can decay while the mean stays constant

Define H(p)=2p(1−p): probability two independent with-replacement draws have
different alleles at this locus. It is not automatically an observed fraction
of heterozygous individuals; that interpretation needs a genotype/mating model.
Sampling distinct copies without replacement instead has factor m/(m−1).

Since E[P'²|p]=p²+p(1−p)/m,
E[H(P')|p]=2(E P'−E P'²)=H(p)(1−1/m). Iterating expectation gives

\[
E[P_t]=p_0,\qquad E[H(P_t)]=2p_0(1-p_0)(1-1/m)^t,
\]
\[
\mathrm{Var}(P_t)=p_0(1-p_0)\{1-(1-1/m)^t\}.
\]

The variance expression follows from H=2P−2P² and fixed E P=p0; no diffusion
approximation is needed. For m4,p0.5, expected next H=.5×.75=.375. Across many
replicates the mean remains.5 while mass moves toward0/1 and within-replicate
diversity declines. A single trajectory can head either way.

Eventual neutral fixation probability is p0, **not** one-step fixation probability
p0^m. To justify the former, first note that every interior state has positive
probability of reaching an absorbing endpoint in the next step. There are finitely
many interior states, so their minimum endpoint probability ε is positive. The
probability of surviving t steps is at most(1−ε)^t→0. Thus absorption occurs with
probability1. At long times P is0 or1, so its unchanged expectation p0 equals the
probability of ending at1. For m4,i2,1/16 is immediate fixation and.5 is eventual
fixation. Confusing them invalidates the experiment's interpretation.

`evolve` propagates every count probability, multiplying current state weights
by transition probabilities. It guards m≤200 and work≤20million contributions.
This exact small discrete model is O(t m²), with O(t m) retained history. It is
not a scalable whole-genome engine or a continuous diffusion approximation.
`simulate` independently samples m Bernoulli draws per generation, allowing a
separate stochastic implementation to be compared with exact distributions.

## 4. A small selection model and an inference trap

An optional **haploid/copy-fitness** extension assigns relative fitness1+s to A
and1 to a, with s>−1. Weighting reproductive contributions then normalizing gives
q=(1+s)p/[(1+s)p+(1−p)]=(1+s)p/(1+sp). Sample next copies with probability q.
At p.25,s1, q.5/1.25=.4; fitness doubling does not double the final normalized
frequency. This is not a diploid dominance model; applying it to genotype-specific
fitness without deriving a new q would be a biological error.

For consecutive complete-population counts x0,…,xT under fixed m and s, path
likelihood is the product of transition probabilities. Sum their logarithms to
avoid underflow. The code computes binomial log terms via log-factorials; it
returns−∞ for an impossible transition out of an absorbing state. Observed
sequencing read counts are not complete-population allele counts and require an
additional observation/sampling/error model absent here.

The executed neutral seed0 path with m40 starts10→2→1→0. On the tested grid,
s−.2 has log-likelihood≈−7.3804, higher than neutral≈−9.3652. Yet the data generator
had s0. Chance loss in a short path can favor a misleading fitted selective
story. A grid winner is not proof of selection, an uncertainty interval or a
model-comparison significance result. More replicate loci, observation modeling,
parameter uncertainty and alternative demographic models would be required.

## 5. Sequence differences hide repeated substitutions

For two equal-length homologously aligned, unambiguous DNA strings, mismatch
fraction f is differences divided by aligned sites. It is not the number of
unseen substitutions. A base can change then return, or change more than once.
Pairwise global alignment does not itself establish homology or produce a
consistent multiple alignment; the caller must justify those prerequisites.
Our bounded function rejects gaps/unknown letters instead of silently deleting
them. A different missing-data policy must be declared before analysis.

Derive a symmetric four-state model: from each base to each other base use rate
α per unit time, so total leaving rate is3α. Let r(t) be the probability of the
original base. Probability flow gives dr/dt=−3αr+α(1−r)=α−4αr, r0=1. Solve the
same first-order deviation equation used in RC dynamics:
r=1/4+3/4 exp(−4αt). The expected substitution count along the path is d=3αt,
so mismatch probability f=3/4(1−exp(−4d/3)). Invert to obtain JC69 distance

\[
\widehat d=-\tfrac34\ln(1-4f/3),\qquad0\le f<.75.
\]

For AAAAAAAA versus AAAAAATT, f.25 and d≈.3040988 substitutions/site. Corrected
d exceeds the observed mismatch fraction under these premises. The derivative
dd/df=1/(1−4f/3) grows near.75, revealing saturation sensitivity. At f≥.75 no
finite nonnegative estimate fits this formula; the code raises a diagnostic
instead of emitting a finite evolutionary time. Real unequal base frequencies,
transition biases, site-rate variation and selection can violate the model.
A distance in substitutions/site is not calendar time without a rate calibration.

## 6. Construct and challenge a clock-based tree

UPGMA begins with one cluster per label. Distance between clusters is the mean
of **all original cross-leaf distances**. Merging clusters A/B updates distance
to C as(|A|d_AC+|B|d_BC)/(|A|+|B|). Equal weighting of the two cluster means when
sizes differ is another algorithm (WPGMA). Select the minimum pair, create a
parent of height distance/2, and repeat. Leaves start at height0; branch length
is parent height minus child height. Stable label-based tie rules make results
reproducible; a tie can still mean unresolved evidence rather than a biological
binary split.

A strict clock with contemporaneous tips implies equal root-to-tip distances.
In any triple, the two largest pair distances then agree: the **ultrametric**
condition. UPGMA can reproduce an exact ultrametric matrix. It always outputs
an ultrametric tree, even when the input violates that condition; returning a
tree is not validation of the evolutionary assumption.

Hand case, labels A/B/C/D: AB2,CD4 and every cross distance6. Merge AB at height1,
CD at2, then both at3. A/B branch lengths are1 each; the AB-to-root branch is2.
Every reconstructed pair distance equals the input. The tests check that exact
cophenetic matrix, not just the names of the leaves.

Counterexample: a synthetic additive unrooted tree has true split AB|CD, pendant
edges A1,B5,C1,D1 and internal edge2. Path sums give AB6,CD2,AC/AD4,BC/BD8. These
valid tree distances are not ultrametric: triple A/B/C has distances6,4,8, whose
two largest differ. UPGMA merges CD, then A with CD, losing the true AB split.
The recorded root height is11/3 and some reconstructed distances differ from
input. This is an assumption failure, not a floating-point bug. Neighbor joining
or likelihood models address different premises, but are not implemented here.

## 7. Executed experiments and reproducibility

From root, Python3.10+ standard library only:

```sh
python3 -m unittest discover -s 18-computational-biology/population-phylogeny -p 'test_*.py' -v
python3 18-computational-biology/population-phylogeny/experiment.py
```

Research questions: does neutral ensemble mean stay constant while diversity
declines, and does a tree algorithm expose violations of its clock assumption?
Hypotheses follow the identities/counterexample above. Controlled variables:
m20,initial10,30generations,s0,2000replicates,seeds0…1999; exact count propagation
is the oracle. Tree inputs are two specified original matrices. Instruments:
full exact distributions, replicate final counts, first five trajectories,
likelihood grid, merge traces and cophenetic distances.

Actual [raw output](evidence/population-phylogeny.json) records environment and
all those inputs. At generation30 exact mean≈.5, variance≈.1963403 and expected
H≈.1073194; loss/fixation probabilities≈.3496843 each. Simulated mean was.5025,
population-estimator variance.19904125, loss fraction.3555 and fixation fraction.358.
Sampling discrepancies are expected; the exact mean standard error for2000
independent replicates is√(.1963403/2000)≈.009908. The counts are not human data.
The clock matrix was reproduced exactly; the nonclock example yielded clade ACD,
not AB, and an ultrametric violation2.

Twelve [tests](evidence/tests.txt) use explicit four-draw enumeration, neutral
moment identities, immediate/eventual fixation distinction, direct likelihood
products, forward/inverse substitution equations, exact tree matrices, input
permutation and a known counterexample. A first-seed loss trajectory is reported
even though it contradicts a naive mean-path intuition; no successful trajectory
was selected to hide it. Finite precision limits the meaning of "exact" numerical
propagation: state enumeration is exact, arithmetic is floating point.

Alternative biological explanations for real frequencies include selection,
migration, mutation, unequal reproduction and sampling error; none is established
by this simulation. Follow-ups should add one mechanism at a time, or simulate
short finite alignments from a known tree and study distance/tree uncertainty.
No such follow-up is reported as executed. Begin [EXERCISES.md](EXERCISES.md), use
[HINTS.md](HINTS.md) if needed, then check [SOLUTIONS.md](SOLUTIONS.md). Exact source
inspection and limitations are in [SOURCES.md](SOURCES.md).
