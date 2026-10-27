# Bounded model and remaining work

This build aligns two in-memory strings exactly under an integer additive match/mismatch/linear-gap model. The DNA wrapper treats N literally and does not infer strand, complement, frame, gene, function, ancestry, variation pathogenicity, or experimental quality. It is not a read mapper, assembler, clinical workflow, whole-genome aligner, or calibrated biological significance test.

Opposing adjacent gaps are admissible; severe mismatch penalties can make them optimum. Multiple optimal paths can exist. Deterministic tie handling chooses one and hides none of the underlying scientific ambiguity. Source verification is limited to the [recorded primary-paper locators](../../18-computational-biology/alignment/SOURCE_VERIFICATION.md); neither original paper's full experimental results are independently replicated.

FASTA parser support is intentionally restricted to DNA ACGTN. Real formats can have richer alphabets, descriptions, conventions and metadata. The CLI limits byte input and matrix cells but not CPU cgroup quotas, total process RSS, concurrent job load, or a service queue. Table storage is quadratic and Python object overhead is material. Provenance hashes identify recorded bytes, not truth or authorship.

Further substantial units are needed for affine gaps, substitution matrices, calibrated inference, indexing/search, read mapping/quality scores, transcriptomics, proteomics, population models, phylogenetics, structural modeling, biological experimental design and data engineering. No domain-wide excellence claim follows from this project.
