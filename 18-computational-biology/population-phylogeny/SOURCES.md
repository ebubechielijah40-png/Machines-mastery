# Source verification and scope — 2026-10-23

| Inspected primary/authoritative source | Exact support | Limitations and integrity notes |
| --- | --- | --- |
| NHGRI, [Allele](https://www.genome.gov/genetics-glossary/Allele) and [Genetic Drift](https://www.genome.gov/genetics-glossary/Genetic-Drift), page display updated2026-10-23 | Definitions of sequence variants at a genomic locus and chance frequency changes | Human-focused glossary diploid wording is restricted locally to an ideal autosomal diploid model; it is not universal ploidy |
| Joe Marcus, [Introduction to the Wright-Fisher Model](https://stephens999.github.io/fiveMinuteStats/wright_fisher_model.html), dated2016-03-29, last updated2019-03-31, hosted in Matthew Stephens's author teaching repository | Definition, finite binomial transitions, neutral mean/variance derivation, absorbing endpoints | Its fixation section writes eventual fixation as a next-step probability. The local lesson corrects the distinction explicitly: eventual p vs immediate p^m, independently derived and tested. R code/plots were not copied or independently rerun |
| Manolis Kellis/MIT6.096, Spring2005, [Lecture9 PDF](https://ocw.mit.edu/courses/6-096-algorithms-for-computational-biology-spring-2005/500e617100543090b65834cebfa2ae12_lecture9.pdf),9PDF pages | PDF page4 nucleotide Markov rate/mismatch correction; page5 cross-leaf UPGMA averaging, ultrametric condition and clock failure | Original local examples/implementation differ. Historical examples elsewhere in this2005 lecture are not adopted as current evidence; no whole-course/book reconstruction or source tree experiment claimed |
| University of Helsinki, Introduction to Bioinformatics Autumn2006, [handout117–137 PDF](https://www.cs.helsinki.fi/bioinformatiikka/mbi/courses/06-07/itb/handouts/itb0607_handouts_117-137.pdf),4PDF pages | Printed118–131: stochastic substitutions, binomial mismatches, aligned-site assumptions and distance inversion; printed136 model limitations | Author not identified in this inspected excerpt. The equal-frequency JC69 special case is derived locally; no likelihood-tree implementation or cited textbook contents inferred from the bibliography |

Original code, derivations, hand examples, matrices, seeds and experiments are
local work. Publicly accessible pages/PDFs are linked, not copied or relicensed.
No source license is assumed to authorize distributing its figures or chapters.
The selection extension is derived from explicitly declared copy-fitness weights;
it is not attributed as a validated diploid biological model.

Unavailable attempted evidence: the large Graham Coop population-genetics notes
exceeded the fetch limit; the WSU Paul Joyce notes and Auckland lecture returned403;
PMC4269093 returned a browser challenge. Their full contents were not inspected
and do not support local completion claims. No original1930s papers, modern
primary-paper reproduction, empirical genomic dataset or clinical validation was
completed in this unit. These remain separate research-depth work.
