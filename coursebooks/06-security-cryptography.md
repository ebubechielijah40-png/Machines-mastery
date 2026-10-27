# Security and cryptography: authority over bytes and information

This original coursebook now develops a connected, executable entry sequence rather than treating a list of security topics as completed instruction. Its completed chapters are bounded framing, measurement/content identity, HMAC-authenticated provenance, and a mathematical privacy-release model. Follow the derivations and assessments in order. The broader field remains PARTIAL: encryption/AEAD, public-key constructions, PKI, real identity, key lifecycle, side channels, production operations and post-quantum mechanisms require substantial additional chapters.

## Chapter 1: meaning must survive representation

A receiver cannot authorize a request until it knows which bytes belong to it and how they are interpreted. The [stream lesson](../06-networking/stream-boundaries/LESSON.md) derives four-byte length framing. Four prefix bytes hold an unsigned big-endian payload size; the payload can arrive in any read partition. Its incremental machine retains at most one bounded incomplete frame, rejects an oversize declaration before accepting its body, and distinguishes a clean EOF boundary from a truncated message. This is an application framing convention over an ordered byte stream, not TCP packet boundaries.

The [HTTP project](../projects-guided/p06-http-server/README.md) changes the grammar. Field duplication, conflicting length conventions and Unicode-first parsing can create interpretation disagreements. Its deliberately restricted parser rejects unsupported forms, imposes a byte budget and one absolute header deadline, and always closes its owned socket. It is not a complete conformant HTTP stack. Worked wire vectors and actual local socket tests let a learner reconstruct the mechanism and its excluded cases.

Entry check: encode `hi` followed by an empty message, then predict decoder state under every EOF position. Exit check: explain why a memory bound for the incomplete frame does not bound all queued messages, and why repeating a whole message after a short send duplicates bytes.

## Chapter 2: a digest identifies content, not authority

The [scientific build](../projects-guided/p08-scientific-pipeline/README.md) parses bounded integer milli-Celsius observations, computes exact rational statistics and records input/code/configuration identity. For 25000,25002,24998 milli-Celsius, mean=25000 and sample variance=4 milli-Celsius squared. A shared correction -10 with supplied standard uncertainty5 gives corrected mean24990 and combined variance79/3 in the same squared units. The model, not the checksum, determines whether those assumptions fit an instrument.

A SHA-256 manifest can detect mismatch against a trusted expected digest. An attacker allowed to replace both data and adjacent digest can construct a fresh matching pair. The hash does not decide who may assert a measurement, whether a sensor was calibrated, or whether a result was derived correctly. Reproducibility and trusted origin therefore need different evidence.

Entry check: derive the sample and mean variance and explain the shared-calibration uncertainty floor. Exit check: replace a synthetic input and recompute its digest; explain why no secret was needed and which trusted authority could detect the replacement.

## Chapter 3: derive authenticated messages and history

The [provenance chapter](../security-cryptography-mastery/provenance/LESSON.md) introduces assets/adversary/trust boundaries before HMAC. A producer tags a validated canonical semantic record with HMAC-SHA256. The original teaching function constructs ipad/opad and nested hashes; SHA-256 compression remains a standard-library primitive, and the running pipeline uses standard-library HMAC. An independent RFC vector checks bytes. Neither vector matching nor a few failed tamper attempts proves cryptographic security.

A tag binds version, producer, stream, sequence, integer value and unit. Strict schema avoids duplicate-key and bool/integer ambiguity. A policy checks which streams a key holder may write. A per-producer next-sequence invariant rejects replay and unaccepted order. These are independent controls: a correct tag may still accompany a forbidden stream or an already committed message.

The processor converts the value exactly to a rational Celsius quantity and authenticates the observation, transform version, output, index and previous digest. Reopening verifies every line and reconstructs the snapshot. An altered output or reordered entry fails; a valid prefix after suffix deletion remains valid without an independently trusted latest tip. Write/sync failure may leave bytes behind, so the object poisons itself and requires reconciliation rather than assuming no commit.

Shared MAC keys let the verifier generate tags too; no public nonrepudiation claim follows. Tags do not encrypt values. A correctly authenticated false claim remains false. The local caller supplies reader identity, so this function argument is not a login system. These limits are central content, not footnotes to a claim of production readiness.

Entry check: compute the first pad bytes for a chosen key and classify authentication, authorization, replay and rollback failures. Exit check: rebuild the core ingest/reopen path, use independent adverse vectors and explain uncertain writes without guessing the outcome. Guided milestones and grading are in [p09](../projects-guided/p09-secure-pipeline/README.md); exercise solutions are separate from first attempts.

## Chapter 4: permitted outputs can still disclose

The [privacy chapter](../13-privacy/count-release/LESSON.md) starts from one bounded bit per protected row. Neighboring add/remove-one-row counts differ by at most one. For ideal Laplace noise with scale1/ε, the output-density ratio for neighbors is bounded by exp(ε), by the triangle inequality; integrating over events gives the stated pure-DP definition. It derives inverse-CDF sampling, mean absolute error1/ε and variance2/ε² rather than importing an unexplained noise call.

Independent repeated releases add conservative privacy cost even while averaging reduces noise variance. Exact integer microepsilon accounting prevents declared-sum rounding drift, but an in-memory object cannot enforce a shared policy after restart or across accounts. The code's finite floating sampler is explicitly not certified by the real-valued proof, and published synthetic seeds are for reproduction only. A known-seed test recovers the disclosure failure that good-looking utility moments would miss.

Entry check: derive sensitivity for one person allowed four rows. Exit check: prove the ideal scalar bound, compare a fixed total budget across repetition strategies, and list which guarantees the executable simulator has not established.

## Source map, practice and scope

Read exact inspected scopes in the [network](../06-networking/stream-boundaries/SOURCES.md), [HTTP](../projects-guided/p06-http-server/README.md), [measurement](../projects-guided/p08-scientific-pipeline/SOURCES.md), [HMAC](../security-cryptography-mastery/provenance/SOURCES.md), [information](../08-information-science/finite-information/SOURCES.md) and [privacy](../13-privacy/count-release/SOURCES.md) records. Intellectual sources are linked, not copied as textbook reconstructions. No uninspected source is counted as verified. Actual JSON observations and test logs live with each executable unit.

Capstone: reconstruct the path from framed bytes through validated measurement claims to authenticated history and a separately analyzed noisy aggregate. Use fresh vectors, fail one assumption deliberately at each boundary, and identify which observed result does and does not support the intended claim. Passing these bounded chapters supports STRONG local-unit classifications; it does not complete the omitted cryptography or security domains.
