# Molecular meaning before manipulating a sequence

A string of A/C/G/T is a representation of observations about a molecule. It
omits concentration, three-dimensional shape, chemical modifications, cellular
location and measurement errors. This bridge introduces the meanings required
by the local alignment and population models. It does not replace a full
biochemistry, gene regulation, proteomics or structural-biology course.

## DNA, RNA and proteins are different physical objects

In the usual cellular DNA description, a sugar/phosphate backbone joins an
ordered sequence of bases A,C,G,T. Two complementary strands pair A with T and
C with G. The sequence is information about one aspect of that molecule; a
FASTA text file is neither a double helix nor a physical sample. Reversing a
record's text and complementing each base are different operations. When a
pipeline compares complementary strands, it must specify the orientation and
coordinate convention rather than silently assuming that equal text direction
means equal physical orientation.

RNA uses ribose and normally U in place of DNA's T. Messenger RNA carries
protein-coding information, but ribosomal/transfer/regulatory RNAs have other
roles. Proteins are amino-acid chains that fold and interact physically.
Transcription produces RNA from a DNA template; translation uses an mRNA's
information during amino-acid-chain synthesis on ribosomes. These named
processes involve molecular machinery, substrates and energy; a Python string
replacement is only a narrow representation transform. It is not a simulation
of transcription chemistry or protein folding. Not every RNA becomes a protein.

For a deliberately restricted DNA **coding-strand representation**, changing
T to U displays the corresponding unprocessed RNA spelling in the same record
orientation. A template-strand representation instead needs complementary
orientation handling. Neither shortcut models splicing, transcription start/stop,
chemical modifications, isoforms, regulation or translation. Those missing
mechanisms can change biological conclusions even when every string operation
is correct.

## A minimal worked representation example

Take an original synthetic record `ACGTTA`. Its symbol count is6; its complement
in the same written left-to-right order is `TGCAAT`; reversing that complement
gives `TAACGT`. The two transforms differ because reversing changes coordinates.
The fraction of G/C symbols is2/6=1/3. A record's length here counts symbols, not
base pairs in an observed duplex, concentration or molecular mass. A tool should
state its alphabet and orientation instead of inferring more than the file says.

This example can be checked directly, without external packages:

```python
s = 'ACGTTA'  # original synthetic string, not a specimen or accession
complement = str.maketrans('ACGT', 'TGCA')
assert s.translate(complement) == 'TGCAAT'
assert s.translate(complement)[::-1] == 'TAACGT'
assert sum(base in 'GC' for base in s) == 2
```

Unknown base N is missing information, not a fifth measured chemical base. A
program can treat it as a literal symbol, a wildcard or a probability distribution;
those produce different answers. The existing alignment workbench explicitly
uses a literal convention: N/N matches, N/A mismatches. The new phylogenetic
distance function rejects N and gaps, because its four-state derivation has no
missing-data model. These are honest, bounded contracts rather than universal
biological interpretations.

## Loci, variants and copies

A locus identifies a genomic location or region. An allele is a sequence variant
there; a variant can involve more than one base. Labels A/a in a population model
name alternative alleles and are not automatically nucleotide symbols. A genotype
specifies the alleles an individual carries at the modeled locus. Under an ideal
autosomal diploid model, N individuals provide2N gene copies. That is a model of
ploidy/locus type, not a statement that every organism or chromosome has two copies.

Worked count: ten ideal diploid individuals give20copies. If four are AA, two
Aa and four aa, A-copy count is2·4+2=10 and frequency10/20=.5. The observed
heterozygous-individual fraction is2/10=.2. By contrast2p(1−p)=.5 is the
probability of different alleles on independent with-replacement copy draws.
Equating these quantities requires an additional mating/genotype model. A
frequency alone does not encode which two copies share an individual.

An alignment between two strings proposes column correspondence. It does not
identify the population's allele count, an individual's genotype, a causal
phenotype or a substitution rate. Measurement and inference need their own
contracts: who was sampled, which locus, what orientation, what uncertainty,
which reference/version and which coordinate system? A synthetic exercise has
known construction; a real dataset needs provenance and quality controls.

## Progression and practice

Proceed to [alignment](02_SEQUENCE_ALGORITHMS.md) to derive the string optimization,
then [population and phylogenetic models](population-phylogeny/README.md) to see
how inference adds assumptions. Their executable tests and synthetic experiments
are separate from unperformed physical/biological experiments.

1. Compute complement and reverse complement of `AAGC`; explain the order.
2. Under the stated genotype counts, verify both allele frequency and observed
   heterozygote fraction. Construct another genotype mixture with the same p.
3. Why can a correct parser not establish that two sequences are homologous?
4. Describe one error caused by treating a template strand as a coding strand.
5. Close this bridge and reconstruct the distinction between a molecule, sequence
   record, alignment, allele count and fitted evolutionary model.

Checkable answers:1.`TTCG` and`GCTT`.2.Frequency.5 andheterozygote fraction.2;
fiveAA/fiveaa gives the same frequency but zeroheterozygotes.3.Homology is an
ancestry claim requiring evidence beyond file syntax.4.The RNA spelling and
orientation can be wrong even though T→U replacement itself is implemented
correctly. These questions test representation boundaries, not wet-lab competence.

## Inspected institutional sources — 2026-10-23

Original examples and explanations above use NHGRI's glossary definitions:
[DNA](https://www.genome.gov/genetics-glossary/Deoxyribonucleic-Acid-DNA),
[RNA](https://www.genome.gov/genetics-glossary/Ribonucleic-Acid-RNA),
[Protein](https://www.genome.gov/genetics-glossary/Protein),
[Transcription](https://www.genome.gov/genetics-glossary/Transcription),
[Translation](https://www.genome.gov/genetics-glossary/Translation) and
[Allele](https://www.genome.gov/genetics-glossary/Allele). All displayed an updated
2026-10-23 date when inspected. Definitions, rather than narrated analogies or
uninspected linked videos, support this bridge. The institutional pages are
human-focused introductions; local ploidy claims are explicitly restricted.
No figures or substantial source passages are reproduced. Detailed nucleotide
chemistry, genetic-code tables, gene regulation, metabolism and protein structure
remain incomplete instructional units rather than implied prerequisites already taught.
