# Explained solutions

1. The MAC authenticates the restricted record under the configured key/policy.
   It cannot establish calibration or truth. Encryption hides its payload only
   from parties without the encryption key under the declared assumptions;
   producer/stream/count metadata remains visible. The demo keys are public.
2. Alpha1,beta1,alpha2,beta2,…,alpha6,beta6 is legal. Alpha5 is position9 there.
   Either producer may run ahead; the required subsequence for each is1…6.
3. Old-key3 fails authorization. New-key3 can append only when alpha's next
   expected sequence is3. Relabeling a MAC changes authenticated bytes and
   cannot turn an old MAC into a valid new-key envelope.
4. Addition is01. Multiplication11×10 gives x²+x→1, or01.
   Multiplication11×11 gives x²+1→x, or10. Integer3×3=9 differs from
   carryless `(x+1)²=x²+1`; ordinary integer division uses the wrong algebra.
5. All GHASH inputs, including the length block, are zero. Starting at zero
   and multiplying zero gives zero. The tag is therefore AES(K,J0); this is
   exactly the inspected empty-message example, not a claim for nonempty data.
6. `00000000000000080000000000000010`. The halves encode8 and16bits.
   The protocol specifies bit lengths; substituting byte lengths changes tags.
   A length block also distinguishes different context/ciphertext partitions.
7. Each overlapping byte XORs to03 because41hex XOR42hex=03hex.
   Both legitimate tags can verify under their own context while repeated
   keystream exposes the plaintext XOR. Different AAD does not restore secrecy.
8. The local ledger remains empty. The authority's head remains zero but its
   nonce counter is1. Retry reserves2 and writes position1. Wasting a nonce
   does not reuse a keystream; resetting reservations can do so.
9. `(2,1)` can reconcile the verified committed suffix if the witness digest
   matches entry1. `(2,3)` is rollback and fails. `(2,2)` succeeds only when
   the exact remembered head matches. Count equality cannot replace digest
   equality, and no case authorizes silently changing policy or keys.
10. No. The restored old signer can sign the fresh challenge using its old
    stored head. A protected newer checkpoint/authority fact is absent.
    The actual experiment deliberately demonstrates this assumption failure.
11. It changes the fingerprint, so existing metadata must reject it. A real
    transition needs an authenticated relation from old to new policy, defined
    effective position, old-key verification/decryption policy, independent
    authority agreement, crash handling and rollback rules. This build does
    not implement that administrative migration; its schedule is fixed.
12. Require exact expected ledger and configuration, exact fresh challenge,
    then verify the signature under the separately pinned public key. A
    signer-supplied replacement public key would let an attacker nominate its
    own authority. Valid signatures do not make wrong questions correct.
13. An HMAC verifier with the shared secret can also create a MAC. A public
    Ed25519 key checks signatures without granting the private signing seed.
    The witness receipt still authenticates only its bound head/context,
    not every real-world assertion in a decrypted observation.
14. Possession permits new old-key MACs, but old-key sequence3 is unauthorized
    in this schedule. An already used sequence with changed content conflicts.
    Replacing a witnessed prefix changes its digest and fails against the
    protected witness. Compromised configuration/witness or whole-pair rollback
    violates those premises and is not defended by this argument.
15. Refuse to acknowledge unsafe new work while authority state is unavailable;
    recovery/reconciliation can be delayed. Recreating an empty authority
    discards freshness evidence and may reset nonce allocation. Availability
    does not justify presenting a weakened assumption as the same guarantee.
16. Require12 entries, distinct global positions1…12, alpha projection1…6,
    beta projection1…6, valid declared transforms and12 distinct nonces.
    The actual process order may vary. A single expected interleaving would
    reject correct schedules without checking the real concurrency invariant.
17. The raw frame product is327,680,000bytes, or312.5MiB. Table/index/page
    overhead is additional. The64MiB check occurs before a connection opens;
    it is a protective lab check, not a hard transaction/disk quota or a
    bound on stalled operating-system calls. Limits must state their boundary.
18. `{numerator:25123,denominator:1000,unit:'celsius'}` represents25.123exactly
    without a binary-float wire convention. Reject a Boolean sequence, wrong
    unit, out-of-range integer, unknown field or duplicate JSON key.
19. The standard supports the GCM operations/nonce requirement; the NIST file
    supplies fixed expected values; the versioned API defines library calls
    and failures; SQLite defines the local writer transaction boundary; actual
    raw output records process behavior here. None establishes a deployed
    remote witness, protected key custody or physical durability in this lab.
20. Reserve/commit a fresh nonce externally; verify and commit one local entry;
    reconcile/advance the witness; then acknowledge. Before local commit,
    retries consume a new nonce; after commit they return the original entry.
    An external job effect might have happened before a reply vanished and
    remains outside SQLite. Use a retained external operation identity and
    authoritative reconciliation; blindly making a new identity can duplicate
    the effect. A copied database alone cannot prove the remote job's outcome.
