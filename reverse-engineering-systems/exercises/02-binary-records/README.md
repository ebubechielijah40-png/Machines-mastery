# Recover a binary record through controlled observations

A program can expose a predictable behavior while hiding its representation.
This exercise reconstructs a small record encoder using probes, competing
hypotheses and independent tests. It is an original, authorized local target;
there is no remote device, proprietary firmware or third-party system to attack.
The native oracle is supplied so every observation can be repeated. Preserve
an attempt log before opening `reference/` or [solutions](SOLUTIONS.md).

Prerequisites: [byte representation](../../../04-computer-systems/SELF_CONTAINED_GUIDE.md),
[the C byte parser](../../../programming-languages-mastery/01-c/units/01-byte-parser/README.md),
hexadecimal, integer powers, Python bytes, and the distinction between a checksum
and authentication in [provenance](../../../security-cryptography-mastery/provenance/LESSON.md).
The last link may be reached through the security domain index if following the
broader curriculum. The lab needs Python3.10+ and a C11 compiler named `cc`.

## A bounded black box

The visible wrapper takes a uint16 sequence, a signed16-bit sample, an actual
Boolean enabled flag and0–32 payload bytes. It returns a hex string. Only these
input ranges are promised. The target has no hidden state; repeating an input
should produce the same bytes. Do not infer a device's physical units from a
field called sample; this synthetic format supplies none.

From the root, query only the oracle at first:

```sh
python3 reverse-engineering-systems/exercises/02-binary-records/oracle.py 0 0 0 ''
python3 reverse-engineering-systems/exercises/02-binary-records/oracle.py 4660 -2 1 41ff
```

Compilation happens in a temporary directory with warnings treated as errors.
No native executable is shipped in the source archive. `oracle.py` reads the
reference C source to build the target; the learner need not read that source
until after recording a model. A hidden implementation is an exercise constraint,
not a security boundary against someone with repository access.

## Observe, isolate, hypothesize, falsify

Begin with one empty baseline and annotate byte positions from zero. Change one
input at a time. Repeat the baseline between groups to check determinism. A probe
ledger has columns: input, output, changed positions, hypothesis, a competing
explanation, next falsifying probe and confidence. Store raw hex, not only notes.

The [executed ledger](evidence/observed.json) is available after an initial
attempt. Its baseline is `4d5801000000000000007913`,12 bytes. Sequence1 changes
byte4 and the final two bytes; sequence256 changes byte5 and the final two.
This supports a low-byte-first field at4–5. The asymmetric value4660=0x1234
produces bytes34,12 there, which rejects an accidental same-byte interpretation.
It does not prove that every other field shares the same byte order.

Sample1 changes byte7 while sample256 changes byte6. A hypothesis that the whole
record is little-endian has now failed. Sample−1 yieldsff,ff;−32768 gives80,00.
Treat the field as a16-bit two's-complement encoding, not a host-memory dump.
For unsigned word w, decode to w when w<32768 and w−65536 otherwise. This is a
representation rule; the native C encoder explicitly converts modulo2^16.

Setting enabled changes byte3. Probe other legal fields independently before
claiming that all remaining bits are free: the wrapper exposes only one Boolean
and the decoder rejects reserved flag bits. One zero payload byte changes length
and adds a byte even though its value is zero. This rejects null-terminated text
as the payload model. Use embedded00 andff; ASCII-only inputs cannot distinguish
many incompatible byte protocols.

The last two bytes vary with earlier fields. A sum, XOR, CRC and keyed tag are
competing explanations. Swapping payload41,ff toff,41 preserves a byte sum but
changes the observed trailer from5df6 to26e1. That falsifies a plain unordered
sum; it does not identify a unique CRC polynomial from two probes. Test a
candidate algorithm over many lengths and inputs, then compare to an independent
library. A candidate passing finite probes remains a behavioral model over those
probes, not proof that no alternative implementation exists.

## Reconstruct an explicit contract

After saving your attempt, read [the solution schema](SOLUTIONS.md). Implement
an encoder and strict decoder in your own file. Do not use native struct layout,
implicit signed casts or a platform's default byte order. A decoder validates
length before indexing, magic/version/flags before interpreting, exact payload
boundary before acceptance and the checksum before returning a record.

Required invariants are `decode(encode(r))==r` over legal records, byte equality
against the oracle, exact one-record consumption, and rejection of malformed
boundaries. Round-trip alone is weak: two wrong functions can agree with each
other. Native differential tests, explicit asymmetric words and the independent
CRC oracle give different kinds of evidence.

```sh
python3 -m unittest discover -s reverse-engineering-systems/exercises/02-binary-records -v
python3 reverse-engineering-systems/exercises/02-binary-records/experiment.py
```

Eight tests include200 deterministic random native/Python comparisons, boundary
cross-products, every single-bit mutation of one packet, all truncations of a
maximum record, trailing bytes, semantic-invalid records with recomputed CRCs,
and a native UndefinedBehaviorSanitizer build. These bounded checks cannot prove
absence of all C undefined behavior or all parser vulnerabilities.

## Experiment and interpretation

Question: which representation hypotheses survive discriminating inputs? Predict
each probe, keep sequence/sample/flag/payload fixed except the chosen variable,
compile once per run, collect the compiler version/build command/source hash and
binary hash, then record output hex and byte count. [experiment.py](experiment.py)
performs12 actual named probes; [observed.json](evidence/observed.json) is the
retained2026-10-23 execution. Its outputs support the schema and failure tests
above. Binary hashes can vary with compiler/path/build details; source hashes
identify which local target was used, not author identity.

A second question is whether checksum validity implies trusted content. The
reference tests intentionally create a different legal sample and recompute the
checksum. It is accepted. That is expected: an unkeyed CRC detects certain
accidental changes but does not authenticate an adversary's chosen content.
For an exposed protocol, add a separately designed authenticity, identity,
anti-replay and framing policy rather than relabeling this trailer as security.

## Milestones, deliverables and evaluation

1. Produce a probe log with at least three falsified hypotheses and a deterministic baseline.
2. Infer each field's width/order independently and predict a never-used legal input.
3. Implement the candidate encoder; compare held random cases against the oracle.
4. Implement a strict decoder; attack its boundaries locally with malformed bytes.
5. Explain checksum limits and extend a version without silently reinterpreting old records.

Deliver the log, schema, your code, raw test output and a limits statement. Award
one point per milestone for a correct model, independent evidence and explanation
of a failed approach, up to15. Missing raw observations earns no experiment
evidence. [EXERCISES](EXERCISES.md), [HINTS](HINTS.md) and [SOURCES](SOURCES.md)
provide practice, gradual help and source provenance. Final memory challenge:
close all references and reconstruct a compatible encoder/decoder with the same
bounds; then explain one new observation that could force you to revise the model.
