# Separate-reader protected-provenance review —2026-10-25

Reviewer: recovered_provenance_gate, separate from the mechanism/teaching author.
This is a team review of a bounded educational system, not an external security
assessment, a deployed-authority audit or evidence of learner mastery. No code,
scope or scoring registry was edited by this reviewer.

## Scope actually inspected

Read AGENTS.md, the unchanged data-security card and scope fingerprint, preserved
plaintext HMAC/lineage lesson, the data-security route, protected_ledger.py,
gcm_mechanics.py, demo/configuration, tests, optional runner, protected-history
chapter,20 exercises and explained solutions, experiment/source records. Source
inspection is attributed to the author in PROTECTED_SOURCES.md; this reader did
not independently inspect all original NIST/PyCA/SQLite pages. The source map
states exact selected scopes rather than attributing the original protocol to
those sources or claiming that vectors certify security.

## Executed checks

```sh
python3 security-cryptography-mastery/provenance/run_protected.py
python3 -m unittest discover -s security-cryptography-mastery/provenance -p test_pipeline.py -v
python3 research/quality/2026-10-25-continuous/provenance-final-reader-probe.py
python3 -S security-cryptography-mastery/provenance/run_protected.py
```

The pinned protected runner passed **16** test methods, including actual competing
processes and all four Linux SIGKILL phases. The preserved standard-library suite
passed **9** methods. Combined25 is correct; the recovered prose's5preserved/20new
breakdown and claim that the optional runner selects20 are incorrect for these
source bytes. Reported this discrepancy to root for correction before publishing.
Historical raw outputs must remain unchanged, with an explicit erratum rather
than silently relabeling them. The separate `-S` run reported BLOCKED,exit2,
with cryptography absent from its import environment; this is an intended missing-
dependency result, not a passing cryptographic test.

Fresh logs are provenance-final-reader-protected-tests.txt,
provenance-final-reader-original-tests.txt and
provenance-final-reader-missing-dependency.json. The probe script and JSON retain
the exact mechanism hashes. No historical result was reused as a fresh run.

The independently selected probe uses gamma/delta rather than the demo producers,
three old gamma sequences, a new gamma key from4, and encryption epochs switching
after global position4. Eight deliberately unevenly interleaved entries preserve
both producer projections1…4 and the expected four/four encryption split. An old
gamma sequence2 retry returns original global index2 after later rotation.

A reader-injected witness advance failure occurs after local commit. Actual local
count is1 while the witness count is0; reopening with the authority available
reconciles to1 and returns the original entry/nonce as a replay. Thus the protocol
does not misclassify unavailable acknowledgement as absent local effect. This is
a local method-injection failure, not a remote network outage experiment.

At the storage counter boundary, reservation from2^63−2 yields the exact nonce
000000007fffffffffffffff. The next append refuses exhaustion and leaves the local
count1. A valid signed head replayed against another challenge is rejected. These
new cases add boundary evidence to the author's vector/field representation,
tampering, configuration binding, rollback, nonce-reuse and process tests.

## Technical and educational judgment

The chapter separates authenticity, authorization, physical truth, confidentiality
and remembered freshness. The polynomial bridge supplies prerequisites before
GHASH; explicit field multiplication/length binding is separate from the library
protecting data. Published known values and a different polynomial representation
are appropriate finite correctness checks, not cryptographic security proofs.

Epochs distinguish per-producer sequence from global history position. MAC key IDs
are authenticated, historical keys remain available, and changing the policy
fingerprint is rejected. AES-GCM uses bound context and an independently committed
nonce reservation. Different associated data is correctly shown not to repair a
reused encryption key/nonce. A retained-history collision guard runs before
encryption and does not pretend to remember removed or failed historical frames.

The witness receipt signs ledger, configuration, count, tip and fresh challenge
under a separately pinned public key. Reconciliation checks the exact witnessed
prefix before advancing a verified local suffix. Whole-pair rollback remains an
explicit executed assumption counterexample. The code and instruction do not
claim that colocated files enforce independent monotonic custody.

The20 assessments require algebra, state/crash traces, configuration/identity
counterexamples, independent concurrency invariants, exact unit conversion,
resource-limit reasoning and reconstruction. Hints and explained solutions are
separate. Six guided milestones and observable exit tasks connect the preserved
record/HMAC mechanism to encryption, transactions and witness recovery. This is
substantial original instruction, not an expanded template or mere API wrapper.

No critical conceptual or core mechanism error was found within the stated
trusted-path, immutable-configuration, authorized-witness-call and exclusive-key-
allocator contract. The test-count discrepancy is a publication/evidence accuracy
defect and requires the reported correction. No unavailable external permission
is invented as a blocker to additional local teaching and investigation.

## Fixed-domain gate recommendation

Recommended marks are instruction2/2/2/1, implementation2/2/2/1,
reproduction2/2/2/2, assessment2/2/2/1, prerequisites2/2/2/1 and
references2/2/2/1. The mandated weights produce **90.00** readiness. Core tests
and separate-author review pass. The bounded protected-history unit merits
STRONG after evidence-count correction and final integration replay.

The **whole fixed data-security domain remains PARTIAL**. Its unchanged scope
explicitly retains external authority infrastructure as unfinished. This build
models authorized witness calls using a local signing object; it does not
implement an authenticated independent service, protected authority/key custody,
its availability/recovery contract or authenticated administrative policy/trust-
anchor transitions. The static schedule teaches an important portion of key
rotation but does not supply those remaining operational mechanisms. They are
accurately disclosed; disclosure does not implement them or close the breadth
gate. Do not change the frozen scope or transfer a unit rating into a domain pass.

Set scope_breadth_confirmed=false until that remaining breadth is developed and
separately reviewed. Root should correct the count statements, retain these
fresh logs and the historical evidence, and execute repository replay before
publishing the source. The larger original EXCELLENT mandate remains PARTIAL.
