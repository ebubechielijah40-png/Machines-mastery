# Computational biology: representation, optimization and biological inference

A computational result has a precise meaning only after its data and model are
specified. A maximum alignment score is a mathematical optimum; an allele-frequency
trajectory is a population model; a tree is an inferred relationship under
substitution/rate assumptions. This coursebook connects those layers through
complete bounded local builds while keeping the larger biology domain PARTIAL.

## 1. Identify the biological object before the data structure

Begin with [molecular foundations](../18-computational-biology/01_MOLECULAR_FOUNDATIONS.md).
DNA/RNA are nucleotide polymers; proteins are amino-acid chains with folded
physical behavior. Text records retain a sequence aspect, not a molecule's full
state. The symbols A/C/G/T, orientation, coordinate convention and missing-base
policy are data contracts. A T→U string transform on a declared coding-strand
record is not a chemical transcription simulation or a translation mechanism.

An allele is a variant at a locus. A diploid autosomal model counts two copies
per individual, but frequencies do not preserve genotype grouping. FourAA,
twoAa,fouraa among ten individuals give A frequency.5 but observed heterozygote
fraction.2. Two independent allele draws differ with probability2p(1−p)=.5.
Confusing those values silently imports a mating assumption. The bridge has
original examples, executable assertions and verified NHGRI definition links.

## 2. Derive an alignment instead of trusting a similarity label

For synthetic strings AG/ACG, an inserted gap creates A-G/ACG and makes a proposed
A/A,G/G correspondence visible. A gap is an alignment symbol, not an observed
historical insertion. With match2,mismatch−1,gap−2 this alignment scores2. Define
F(i,j) as the best score for the first i/j symbols. Its final column either pairs
them, leaves a gap in the second, or leaves a gap in the first. Thus F is the
maximum of diagonal+pair score,up+gap,left+gap, with global boundaries F(i,0)=ig,
F(0,j)=jg. The last-column argument is the correctness proof's decomposition.

Local alignment changes the question to best substrings, so it adds a zero
restart, zero boundaries, maximum endpoint anywhere and stop-at-zero traceback.
A global bottom-right endpoint is now wrong. Traceback must recover displayed
columns and declared zero-based half-open spans; reversing a collected path
matters even when an unordered rescore happens to pass.

The [complete alignment lesson](../18-computational-biology/02_SEQUENCE_ALGORITHMS.md)
contains worked tables, original mechanisms, independent short-input exhaustive
oracles, exercises/hints/solutions and actual gap-sensitivity evidence.
The [FASTA guided build](../projects-guided/p14-bioinformatics/README.md) adds exact
two-record parsing, memory/input bounds, provenance hashes and CLI tests. It uses
synthetic data and literalN behavior; it does not establish functional similarity
or ancestry from a score. Affine gaps, protein matrices and large-scale search
remain extensions rather than hidden features.

## 3. Replace one trajectory with a population distribution

The [population/phylogeny lesson](../18-computational-biology/population-phylogeny/README.md)
starts with m gene copies and count X. Independent with-replacement reproduction
makes X'|X=i binomial(m,i/m). The combination factor counts different draw orders;
it is not a fitted magic formula. For m4,i2 the transition row is[1,4,6,4,1]/16.
Mean remains2 but there is a1/16 immediate fixation chance and a1/16 loss chance.

Dividing counts by m gives E[P'|p]=p and Var(P'|p)=p(1−p)/m. Define H=2p(1−p).
From E[P'²]=p²+p(1−p)/m obtain E H'=H(1−1/m). Repeated averaging gives constant
ensemble mean and decaying expected diversity, not a flat typical trajectory.
Eventual fixation probability p0 differs from one-generation p0^m; absorption
and conserved expectation prove the eventual result.

The original exact propagator enumerates finite states, while a separate seeded
simulator samples Bernoulli copies. At m20,start10,t30, exact mean≈.5,expected
H≈.1073194 and loss/fixation probabilities≈.3496843 each. Two thousand synthetic
replicates gave mean.5025 and fractions.3555/.358. Raw counts, seeds, environment
and test output are local; these are simulations, not observed evolution.

## 4. Modeling selection does not make every decline selective

A declared haploid/copy-fitness extension weights A by1+s and a by1, giving
q=(1+s)p/(1+sp) before reproduction. It is not a diploid dominance law. The path
likelihood multiplies transition probabilities for consecutive complete-population
counts; read-count data would require another observation layer.

A recorded neutral seed0 path10→2→1→0 in40copies favors s−.2 over0 on the tested
likelihood grid. We know the generator was neutral because this is a synthetic
experiment. Thus a best-fitting selective story for one short realization is
not proof of the mechanism. The lesson separates model prediction, data sampling,
parameter ranking and evidence limitations; it does not fabricate significance,
a confidence interval or biological causality.

## 5. Distances and trees add assumptions beyond alignment

An equal-rate four-base substitution model gives mismatch fraction
f=.75(1−exp(−4d/3)) after expected path length d substitutions/site. Inverting gives
JC69 d=−.75ln(1−4f/3). For f.25,d≈.3040988, greater than the observed difference
because repeated changes may be hidden. At f≥.75 the inverse is not a finite
estimate; sensitivity diverges near saturation. This distance is not years.
Unknown/gapped sites, unequal base frequencies and site/lineage rate variation
need explicitly different models.

UPGMA averages all cross-leaf distances, selects the closest clusters and places
their parent at half their distance. Cluster-size weighting matters after unequal
merges. Under a strict clock, contemporaneous tips imply an ultrametric matrix:
two largest distances in every triple agree. The implementation reconstructs a
hand ultrametric matrix exactly and intentionally fails to preserve the known AB
split in a synthetic nonclock additive tree. That counterexample teaches the
model boundary; a returned tree alone is not an ancestry validation.

## 6. Reconstruct, test and extend with provenance

Use the [stack build](../projects-guided/computational-biology-stack/README.md) after
the alignment and population mechanisms. Rebuild the recurrence, neutral moments,
JC inverse and cluster average without notes; check them with independent oracles.
Write down which quantities are measured, assumed or inferred before adding a
new dataset. Keep raw inputs, byte hashes, model parameters, software version,
coordinate/alphabet policies and source-verification records together.

The exact population/tree suite has twelve passing mechanism/boundary tests and
executed raw evidence. Biological wet-lab work, large empirical datasets,
transcriptomics/proteomics, population structure, recombination, likelihood trees,
structural modeling and major paper reconstructions remain incomplete. A
self-contained bounded model is useful preparation without claiming those
unperformed investigations have been completed.
