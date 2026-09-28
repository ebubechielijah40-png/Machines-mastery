# Computational biology — self-contained deep handbook

Computational biology is not “apply Python to DNA.” It is the use of computational and mathematical models to reason about living systems while respecting how biological measurements are produced and what they can and cannot establish.

## 1. Biology as layered physical information processing

A cell is a physical chemical system. DNA is a polymer whose sequence can carry heritable information; RNA can carry, regulate, catalyze, and mediate information; proteins are polymers that fold into structures whose physical chemistry enables functions. The familiar `DNA → RNA → protein` central-dogma diagram is useful but incomplete: regulation, non-coding RNAs, reverse transcription, RNA processing, degradation, localization, feedback, and epigenetic mechanisms complicate the flow.

### Mental model

```text
genome
  ↓ transcription + regulation
RNA population
  ↓ processing / translation / degradation
protein population
  ↓ interactions / localization / modification
cell state
  ↕ environment, metabolism, signaling, feedback
phenotype / measured output
```

A sequence file is therefore not “the organism.” It is one measurement/representation of part of a biological system.

## 2. Molecules and chemistry you actually need

Atoms form bonds according to electron structure. Biological macromolecules exist in water, so polarity, hydrogen bonding, ionic interactions, hydrophobic effects, and pH matter. Thermodynamics asks which states are energetically favored under constraints; kinetics asks how quickly transitions happen. A reaction can be thermodynamically favorable yet slow without a catalyst.

Proteins are built from amino acids; side-chain chemistry affects folding and interactions. Nucleic acids use complementary base pairing, but real stability depends on sequence context, salt, temperature, structure, and molecules present. Computational sequence rules are simplified models of richer chemistry.

## 3. DNA, RNA, genes, and genomes

DNA strands have directionality. Complementary bases pair A-T (or A-U in RNA contexts) and C-G in the canonical model. Because antiparallel orientation matters, “reverse complement” means reverse the sequence and complement each base. Genes include regions that can be transcribed; in eukaryotes, transcripts may contain introns removed by splicing and exons joined into mature RNA. A genome also contains regulatory and structural regions.

### Coding sequences
A codon is a triplet read in a particular frame. Translation depends on a start context, reading frame, genetic code, and stop signal. Simply finding `ATG` does not prove a real gene; organisms and organelles vary, annotation uses additional evidence, and alternative starts/splicing exist.

## 4. Sequence representation and file formats

FASTA represents named sequences. FASTQ couples sequence with per-base quality scores. SAM/BAM represent alignments. VCF represents sequence variants relative to a reference. GFF/GTF represent annotations. Each format has edge cases and conventions; production tools should use mature parsers for real datasets.

Data lineage matters: sample collection → extraction → library preparation → instrument → base calling → filtering → alignment/assembly → variant/expression inference. Every stage can introduce bias.

## 5. Sequence algorithms

### Exact matching
Naive matching compares a pattern at every position. Faster algorithms exploit prefix structure, hashing, suffix structures, or automata. Choice depends on pattern count, text size, alphabet, memory, and whether approximate matches are allowed.

### Alignment
Alignment is a model of correspondence, not a statement that two residues “really” descended from one another. Dynamic programming optimizes an explicit scoring function. Global alignment (Needleman–Wunsch) aligns full sequences; local alignment (Smith–Waterman) finds high-scoring regions. Gap penalties represent assumptions about insertion/deletion events.

For global alignment, define a matrix `F[i,j]` as the best score aligning the first `i` symbols of A with the first `j` symbols of B. Each cell considers match/mismatch, gap in A, or gap in B. This works because an optimal alignment's prefix must itself be optimal under the same state definition—optimal substructure.

## 6. Genomics and variation

A reference genome is a coordinate system/model, not a perfect “normal genome.” Variant calling compares observed reads against a reference and statistical/error model. Coverage, mapping ambiguity, sequencing errors, duplicated regions, and population diversity affect confidence.

Never interpret a variant's biological or medical meaning from a single computational annotation alone. Clinical interpretation requires validated evidence frameworks and domain expertise.

## 7. Gene expression and transcriptomics

RNA-seq measures fragments derived from RNA molecules after a complex experimental process. Counts depend on library size, transcript length, capture efficiency, composition, and protocol. Differential expression is statistical inference under a model; fold change alone is not enough. Batch effects can dominate biological signal.

## 8. Evolution and phylogenetics

Evolution changes populations across generations through mutation, selection, drift, recombination, migration, and other processes. Sequence similarity can reflect common ancestry, constraint, convergence, or chance depending on context. Phylogenetic trees are inferred models; branch meaning depends on method and model.

Distance methods compress sequence information into pairwise distances. Character-based methods model changes at sites. Bootstrapping assesses stability under resampling, not the probability that a tree is “true.”

## 9. Proteins and structure

Sequence constrains but does not trivially determine structure/function. Protein structure is commonly described as primary sequence, local secondary structures, 3D tertiary organization, and multi-subunit quaternary organization. Structure prediction estimates likely conformations from learned/physical constraints; confidence scores are model-dependent and do not replace experimental validation.

## 10. Systems biology

Systems biology models networks of interacting components: gene regulation, signaling, metabolism, population dynamics. Ordinary differential equations can model concentrations over time; stochastic models matter when molecule counts are small or randomness is central. Parameters are often uncertain and non-identifiable: multiple parameter sets may explain the same measurements.

Example two-state expression model:

`dM/dt = transcription_rate - degradation_rate * M`

At steady state, `M* = transcription_rate / degradation_rate`, assuming constant rates. This simple model predicts exponential approach to equilibrium; real cells may violate constant-rate assumptions.

## 11. Population genetics

Allele frequencies change due to selection, drift, migration, mutation, and mating structure. Hardy–Weinberg equilibrium is a null model under assumptions, not a law that populations must follow. Deviations can arise for many reasons; one observation rarely identifies a unique cause.

## 12. Synthetic biology — design reasoning, not wet-lab instructions

Synthetic biology applies engineering ideas to biological systems: modularity, sensing, control, expression, feedback, and design-build-test-learn cycles. This repository focuses on safe computational modeling, sequence-level toy designs, circuit logic, and measurement reasoning. It does not provide procedural pathogen modification, harmful organism engineering, or wet-lab optimization instructions.

## 13. Machine learning in biology

Biological ML inherits all ordinary ML problems plus severe dataset shift, confounding, label uncertainty, small cohorts, population structure, and causal ambiguity. Random train/test splits can leak patient, batch, or homologous-sequence information. Split design must reflect the deployment question.

## 14. Reproducibility

A computational biology result should record dataset identity/version, preprocessing, parameters, software versions, random seeds where relevant, environment, intermediate artifacts, statistical assumptions, and exclusions. Reproducible computation still does not prove biological causation.

## 15. What is possible and what is not

**Possible:** parse sequences, compute composition, search motifs, align sequences, infer models under assumptions, cluster expression profiles, simulate populations/networks, predict structures/functions probabilistically, and reproduce published computational analyses when data/code are available.

**Not guaranteed:** infer phenotype from genotype perfectly, establish causation from correlation alone, recover missing experimental context from sequence files, predict every protein interaction accurately, or make clinical decisions from a toy pipeline.
