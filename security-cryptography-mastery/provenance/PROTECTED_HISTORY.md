# Encrypted history, key epochs and an independent remembered head

The [first provenance build](LESSON.md) authenticates typed observations and
their transformation, but its records remain readable and its writer owns one
append path. It can detect an old prefix only if a trustworthy newer head
survives elsewhere. This original continuation makes those boundaries executable:
encrypt the payload, retain historical key schedules, serialize competing writers,
reserve nonces outside a failed append, and compare history with a signed external
head. Its separate authority is a local educational model. Two files on one
machine do not provide independent security custody.

Enter after the first lesson: explain a producer MAC, a hash chain, canonical
encoding, replay and why an authentic temperature can still be false. Know
[transactions and isolation](../../07-databases-data-systems/query-isolation/README.md),
[Python values and aliasing](../../02-programming/python-entry/README.md), binary
integers/XOR and finite sequences. This chapter introduces its polynomial bridge
before using it. Exit by reconstructing the append/recovery state machine and
predicting every kill phase before consulting observed output.

## Define the claims before choosing cryptography

An accepted producer observation means a holder of an authorized producer key
authenticated a restricted record. It does not mean a sensor was calibrated,
the named producer is a legal person, or the temperature represents reality.
Encryption adds a different claim: a party without the encryption key should
not recover the payload under the primitive's assumptions. Sequence and chain
checks address ordering/substitution; an independently remembered head addresses
rollback. A successful cryptographic check cannot repair a missing measurement
or authorize a principal outside the configured policy.

| Boundary | Input and state | Output and invariant |
| --- | --- | --- |
| Producer authentication | Typed record, producer/key ID, sequence epoch, stream policy | Valid HMAC over an exact domain-tagged canonical envelope |
| Encryption | Envelope/output, epoch key, unique nonce, bound header | Ciphertext with a full tag; payload is hidden, header remains visible |
| Local transaction | Complete verified prefix, next producer sequence, serialized writer | One new immutable entry or no local append |
| Witness | Independently protected counter/head, authorized calls | Nonce reservations never reused; compare-and-set extends one head |
| Receipt verification | Pinned public key, ledger/config identity, fresh challenge | Signature binds the exact head to this expected context |

The attacker model permits reading/copying/editing the ledger file and replaying
old artifacts. It does not permit replacing trusted configuration, stealing keys,
rolling back the witness, or impersonating authorized witness writers. Violating
those assumptions is part of the negative controls, not a claimed defended case.
The supplied demo keys are public deterministic bytes. They protect no real data.

## Separate payload, authenticated context and visible metadata

The plaintext contains the complete producer envelope and derived rational
temperature. Its associated header names version, ledger, global index, previous
digest, producer, writer key ID, producer sequence, stream, encryption key ID,
nonce and request digest. AES-GCM authenticates that header without encrypting it.
Changing a stream or position changes the expected context and fails verification.
Metadata still exposes who writes, when positions grow and which keys/streams are
used. Confidentiality of payload is not anonymity or traffic-analysis protection.

The code delegates AES-GCM to `cryptography`. A128-bit authentication tag is
appended to ciphertext by that API; decryption releases a payload only after
verification. Wrong key, nonce, context or ciphertext is a failed verification.
The ledger uses32-byte keys,12-byte nonces and no shortened tags. These selected
library contracts and versions are mapped in [PROTECTED_SOURCES](PROTECTED_SOURCES.md).
No home-written cipher protects the data.

The explicit [tag mechanics](gcm_mechanics.py) are a separate learning mechanism.
They do not replace the library. AES block evaluation is still delegated, and
this repository does not yet teach a complete AES round/key-schedule implementation.

## A small polynomial bridge before128-bit fields

Represent a polynomial with binary coefficients by a bit string. In this small
example `11` denotes x+1 and `10` denotes x. Coefficients add modulo2, so1+1=0;
addition of these strings is XOR. Multiplication distributes polynomial terms
without integer carries. Thus `(x+1)x = x²+x`, represented as `110`, whereas
ordinary integer3×2 also happens to equal6 here but is not the general rule:
`11 × 11` gives `(x+1)²=x²+1`, or `101`, not integer9.

Choose a two-degree modulus `x²+x+1`. In the quotient, `x²=x+1` because
subtraction and addition agree modulo2. Reduce the first product:
`x²+x = (x+1)+x = 1`, giving `01`. Reduce `(x+1)²` to
`x²+1=(x+1)+1=x`, giving `10`. Multiplication followed by reduction keeps
the result within two coefficients. Reduction removes a highest-degree term by
XORing a suitably shifted modulus; repeat until its degree is below the modulus.

The same representation idea scales to128 coefficients with a different fixed
modulus. The test oracle performs carryless multiplication and polynomial long
division. The mechanism instead shifts and conditionally reduces one128-bit
register for128 iterations. Their agreement checks two different descriptions;
it does not prove constant-time execution or cryptographic security in Python.

GCM's bit ordering is easy to confuse with an ordinary integer polynomial
encoding: the mechanism processes the most significant input bit first, and
right shifts use the `e1` reduction constant in the high byte. The independent
oracle explicitly reverses128 coefficient bits before its ordinary polynomial
division and reverses the result afterward. Simply swapping in integer `%`
cannot implement this field operation.

For the restricted96-bit-nonce/full-tag case, tag reconstruction computes
H=AES(K,0), folds padded context and ciphertext blocks with GHASH, binds their
bit lengths, and masks the resulting block with AES(K,nonce||1). GHASH repeatedly
multiplies `(previous XOR next block)` by H. The length block distinguishes
different context/ciphertext partitions. `reconstructed_tag` matches an inspected
published vector and16 independently varied context/payload length cases. This
finite reconstruction is not an AES implementation or a general GCM API.

## Why one failed append must still consume a nonce

For counter-mode payload blocks write `C=P XOR S`, where S is the generated
keystream. Reuse the same key/nonce for two payloads and S repeats:
`C1 XOR C2 = P1 XOR S XOR P2 XOR S = P1 XOR P2`. Knowing one plaintext then
reveals the other overlapping plaintext. Changing the associated ledger ID
changes authentication context, not this repeated keystream. The test deliberately
encrypts A-filled and B-filled payloads under the same public test key/nonce with
different associated data and checks the XOR equality.

The witness allocates an increasing integer and commits it in its **own**
transaction before encryption. The96-bit nonce is32 zero bits followed by the
64-bit counter. SQLite storage limits this example's usable counter to signed63
bits; it refuses exhaustion rather than wrapping. If the local append fails,
the reservation remains consumed. Gaps are safe; repetition is not. A nonce is
an encryption identifier, not the producer's sequence or the ledger position.

Example: position1 reserves nonce1, then the process dies before local commit.
The local ledger has no entry1. A retry still writes position1, but reserves
nonce2. If it had reused its position as nonce, a ciphertext observed before
the crash could share a keystream with the retry. Reserving only inside the
rolled-back local transaction has the same defect.

Encryption key material must be exclusive to this allocator's lifetime/domain.
Two witnesses both starting at1 can collide even when their ledger IDs differ.
The configuration rejects duplicate encryption material across its own epochs
and rejects authentication/encryption key reuse, but cannot discover another
machine using the same key. A retained-history guard refuses a reserved nonce
already visible locally **before** encrypting. It cannot remember encryptions
removed by a complete history rollback or previously failed transactions.

## Rotation is policy history, not merely a new dictionary entry

An authentication epoch names producer/key ID, first and last producer sequence,
and authorized streams. The demo authorizes alpha-old for1–2 and alpha-new from3.
Sequence2 retains its old key ID when read later. A new sequence3 signed with
alpha-old is rejected even if its HMAC is mathematically correct. Relabeling an
old MAC as the new key ID also fails because the ID is authenticated.

Encryption epochs are indexed by **global ledger position**, since several
producers may interleave. The first two positions use cipher-old and later ones
use cipher-new. Producer sequence and global position are different clocks.
The actual two-process run has six alpha and six beta entries; each producer's
sequence remains1…6 while global positions form one1…12 history.

Old verification/decryption keys remain necessary for full historical semantic
verification in this implementation. Removing them is not a supported erasure
or archival migration procedure. A stolen old producer key can create old-key
messages; retained sequence/content checks and the external head constrain their
acceptance here, but do not erase that compromise. The witness's signing key is
also fixed; rotating that trust anchor requires a separately authenticated
transition, not accepting whichever public key arrived beside a receipt.

This build freezes the full epoch schedule and policy at construction. A canonical
configuration fingerprint binds IDs, ranges, streams and key-material digests
without storing key bytes in either database. Ordering of epoch lists is part
of that fingerprint. It is not a secret vault, dynamic administrative revocation
protocol or general key-management service. Public demo keys and their digests
must never be mistaken for high-entropy secret provisioning.

## Serialize the local append, then reconcile acknowledgement uncertainty

Each append obtains a SQLite `BEGIN IMMEDIATE` transaction before reading the
current ledger. Cooperating writers serialize at that boundary or time out;
there is no claim of writer fairness. The implementation re-verifies the bounded
prefix, decrypts frames, checks producer authentication/sequence/output and
reconstructs the last head. This intentionally expensive full scan makes the
invariants inspectable. It costs O(N) entry checks per append and O(N²) over an
N-entry history; it is not a high-throughput storage design.

An identical `(producer,sequence,envelope)` retry returns its original index and
digest. Reusing the same producer/sequence with different content is a conflict.
The new entry and its global position commit together locally. Only afterward
does the witness advance its head. A successful API response follows witness
reconciliation, but a lost response leaves an uncertain acknowledgement.

| Crash phase | Local committed entry | Witness head | Safe retry observation |
| --- | --- | --- | --- |
| After nonce reservation | Absent | Previous head; reservation retained | New append consumes a different nonce |
| Before local commit | Absent after rollback | Previous head; reservation retained | New append consumes a different nonce |
| After local commit | Present | May still lag | Verify local suffix, advance witness, return original digest |
| After witness advance | Present | New head | Identical retry returns original digest |

All code paths acquire ledger ownership before short witness transactions; an
external witness deployment would need its own authenticated authorization,
availability, failure and concurrency analysis. The local `snapshot` is not a
pure read: it also reconciles a committed unwitnessed suffix under this protocol.
It can advance the witness and requires the corresponding authority access.

## A signed head must bind the question that was asked

The witness signs a domain-separated canonical body containing ledger ID,
configuration fingerprint, entry count, head digest and a fresh32-byte challenge.
The reader supplies the expected ledger/configuration and pins the public key.
A signature on an unspecified ledger, another policy version or an old challenge
does not answer this reader's question. A validly signed wrong-configuration
authority is explicitly rejected by a test.

Ed25519 verification uses a public key without handing the reader the signing
secret. That differs from producer HMAC verification, where possession of the
MAC key also enables message creation. The library implements Ed25519; this is
a study of trust/context binding, not a new elliptic-curve implementation or
public certificate authority.

The witness advances with compare-and-set `(expected count,expected tip) → new
tip`; an identical acknowledgement retry is harmless, and a divergent expected
head fails. On reopen, if the witness has more entries than the local ledger,
or its remembered prefix digest disagrees, the ledger refuses rollback. If a
verified local suffix committed before the witness update, reconciliation can
extend the witness through that suffix. Authenticity of that suffix still
depends on the configured keys and authorized processor assumptions.

Rolling back both the ledger and witness can pass every local check. The actual
experiment demonstrates this: the current witness rejects a one-entry backup
after entry2, but restoring the matching old authority also makes the old pair
acceptable. A third independently protected newer fact would be needed to detect
that event. Challenge freshness proves that a response was signed for this
challenge; it does not by itself prove that the signer's stored state is current.

## Build, debug and reconstruct

Use a virtual environment with the optional pinned dependency:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r security-cryptography-mastery/provenance/requirements-protected.txt
.venv/bin/python security-cryptography-mastery/provenance/run_protected.py
.venv/bin/python security-cryptography-mastery/provenance/protected_experiment.py
```

Windows uses the virtual environment's `Scripts/python.exe`. The optional runner
reports BLOCKED if cryptography50.0.2 is unavailable; it does not claim that the
environment installed it. Actual Linux process-kill evidence is separate from
portable algebra/vector checks. Install dependencies through your normal trusted
package workflow; no copied compiler or cryptography wheel is bundled.

Build in these milestones before opening the reference:

1. Preserve the original typed-record/canonical/HMAC contracts. Add a key ID and
   hand-check old/new sequence authorization and a wrong-stream case.
2. Implement immutable epoch configuration and fingerprinting. Explain why
   changing only a public key ID is not changing secret material.
3. Build the bounded GHASH learning mechanism and independent polynomial oracle.
   Keep it separate from the library protecting data.
4. Add nonce reservation and an encrypted header/payload frame. Inject a failure
   before local commit and predict why the next nonce must differ.
5. Serialize competing writers and preserve exact original retry responses.
   Check a per-producer sequence projection independently of global order.
6. Sign configuration-bound challenge receipts, reconcile a lagging witness,
   and demonstrate both defended local rollback and the undefended whole-pair
   rollback. Never hide the negative control to make a result look safer.

Deliver a state-transition trace, runnable mechanism, actual raw output, test log,
two counterexamples and an operational limits statement. Suggested rubric:
25 points for exact state/cryptographic assumptions,20 for mechanism correctness,
20 for failure experiments/independent checks,15 for explained assessments,
10 for prerequisite/transfer reasoning,10 for provenance/reproducibility.
Reject a submission regardless of total if it reuses a nonce, silently accepts
a changed configuration, invents a physical test or calls a local witness a
deployed protected authority.

Try [20 exercises](PROTECTED_EXERCISES.md), then [hints](PROTECTED_HINTS.md) and
[explained solutions](PROTECTED_SOLUTIONS.md). Rebuild from memory the epoch
schedule, nonce/append/witness state machine and receipt verification contract.
Transfer to a medical sensor or job queue only as a design exercise: identify
which real-world truth, authorization, delivery and external effects are outside
these local invariants. [Actual experiments](PROTECTED_EXPERIMENTS.md) document
what ran. Dynamic policy, protected remote deployment, host failure, secure key
custody, key erasure, archival migration and high-volume operation remain open.
