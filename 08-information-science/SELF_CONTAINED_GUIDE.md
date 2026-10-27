# Information science: finite uncertainty before security claims

The [finite information unit](finite-information/LESSON.md) develops logarithmic surprise, entropy, joint and conditional uncertainty, and mutual information through explicit probability tables. It implements finite-distribution calculations, checks independent algebraic oracles, and investigates a binary flip model where an always-inverted signal retains information. Required algebra and entry checks are specified within the unit.

Use the results to inspect representation boundaries. A 32-bit length prefix has fixed storage width, while its entropy depends on the distribution of lengths. A hash has a fixed output width, while authentication depends on trusted expected values or secrets. A dataset's high empirical byte entropy does not establish privacy or cryptographic unpredictability. These are different questions about the model and observer.

Progress to [stream framing](../06-networking/stream-boundaries/LESSON.md), [scientific content identity](../projects-guided/p08-scientific-pipeline/README.md), [authenticated origin](../security-cryptography-mastery/provenance/LESSON.md) and [bounded aggregate disclosure](../13-privacy/count-release/LESSON.md). Explain the output and threat at each boundary rather than applying the word information as if all quantities shared one meaning.

Entry assessment: compute H([1/4,1/2,1/4]) and mutual information of a fair bit paired with its exact inverse. Exit assessment: reconstruct the finite calculator and explain why neither observed entropy nor checksum agreement certifies a secure system. Exercises, hints, solutions, primary-source scope and actual computed model tables are separated in the unit.

Information science remains PARTIAL. Compression/coding algorithms, continuous distributions, retrieval, epistemic models and semantics need further developed instruction and experiments; this unit does not claim their completion.
