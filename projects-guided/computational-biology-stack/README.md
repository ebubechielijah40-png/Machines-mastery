# Build a reproducible biology analysis with explicit model boundaries

This project connects three complete local mechanisms: bounded FASTA/alignment,
finite-population sampling, and substitution-distance/tree construction. The
reference runner uses original synthetic inputs and writes a provenance-bearing
JSON report. The population and four-taxon tree examples are separate declared
models; two aligned strings do not magically determine a population history or
a four-species phylogeny. FASTQ quality modeling, read mapping, variant calling,
expression pipelines and empirical validation remain extensions, not implemented
features concealed behind the word “stack.”

## Prerequisites and internal architecture

Study [molecular meanings](../../18-computational-biology/01_MOLECULAR_FOUNDATIONS.md),
[alignment](../../18-computational-biology/02_SEQUENCE_ALGORITHMS.md) and
[population/phylogeny](../../18-computational-biology/population-phylogeny/README.md).
The mathematical dependencies are fractions, finite probability, weighted means,
variance, table recurrences and the exponential/log inverse derived locally.
Use Python3.10+ standard library; all data is synthetic and local.

The sequence route parses two records, computes a global alignment under explicit
scores, then estimates JC69 distance only for the resulting unambiguous gapless
sites. A gap/unknown or mismatch fraction≥.75 is a model diagnostic, not an
invitation to silently delete data. The population route propagates probabilities
of allele counts under neutral fixed-copy sampling. The tree route clusters a
separate exact ultrametric distance matrix and records every merge. Byte/source
hashes identify the run's inputs/implementation, not their biological truth.

## Derive and implement six milestones

1. Start with the [FASTA guided build](../p14-bioinformatics/README.md). Run the
   inventory starter, then derive global/local recurrences and traceback before
   using the reference. Deliver exact parser limits and a hand-scored table.
2. For synthetic AAAAAAAA/AAAAAATT at match2,mismatch−1,gap−2, predict a gapless
   score10. Independently count mismatches and derive distance−.75ln(2/3)≈.3040988.
   Demonstrate rejection if N, a gap or a saturated mismatch fraction is passed.
3. Construct m4,i2's binomial row[1,4,6,4,1]/16. Implement exact propagation,
   predicting after3generations E P=.5 and E H=.5(.75)^3=.2109375. Use a separate
   Bernoulli simulator; do not replace distributions with one “typical” path.
4. Trace AB2,CD4,all cross6 into merge heights1,2,3. Reconstruct every pair
   distance from the tree. Then run the nonclock counterexample and explain
   why a valid tree-shaped output can still encode the wrong split.
5. Connect reports without conflating units: alignment scores are dimensionless
   objective values; JC distance is substitutions/site; allele count is copies;
   tree height here is half a distance, not calibrated years. Preserve exact
   input/source hashes, parameters, commands and environment.
6. Close all references and rebuild the recurrence, count transition and cluster
   averaging. Explain immediate vs eventual fixation and a neutral path's
   misleading likelihood winner. Extend one assumption only after specifying
   its new state/observation model and an independent oracle.

The executable [run_stack.py](run_stack.py) is a reference after an attempt.
It uses the underlying original implementations rather than duplicated answers.
Checkable exercises, hints and solutions are separate in the alignment and
population units. Do not read solutions before recording your own derivation.

## Run and evaluate

```sh
python3 projects-guided/computational-biology-stack/run_stack.py
python3 -m unittest discover -s projects-guided/computational-biology-stack -p 'test_*.py' -v
python3 -m unittest discover -s 18-computational-biology/population-phylogeny -p 'test_*.py' -v
```

[Actual output](evidence/stack.json) includes the exact fixture hash, source hashes,
score10, distance≈.3040988, finite distribution and rootheight3.
[Integration test output](evidence/tests.txt) records one passing semantic-boundary
test; the underlying population/tree suite records twelve independently grounded
tests. [VALIDATION.md](VALIDATION.md) states what those outputs establish.

Deliver original code, derivations, a hand trace, raw JSON/test logs, a biological
assumption table and one failed-model analysis. Rubric:25points objective/state
correctness,25 independent mathematical oracles,20 provenance/units/limits,
20 predicted and executed failure experiments,10 memory reconstruction. A score
alone does not establish learner mastery; an unsupported causal/clinical claim,
invented observation or unexamined missing-data policy requires remediation.

## Failure, security, performance and deployment

The local runner takes no uploaded or external data. Its fixture/model sizes
are fixed. The FASTA workbench separately bounds bytes and table cells; exact
population propagation guards state/work size and UPGMA guards taxon count.
Large alignments need score-only/banded/other algorithms with changed contracts;
whole-genome data needs streaming and provenance beyond this exercise.

Real biological records may be sensitive. A byte hash is neither de-identification
nor authorization to redistribute sequences. Do not put real identifiers into
these synthetic fixtures. Reproducible local deployment is the commands above;
no clinical service, wet-lab procedure or cloud pipeline was created. The inspected
source maps in each unit distinguish author definitions, locally derived equations
and sources blocked by access. The full biology stack remains PARTIAL overall.
