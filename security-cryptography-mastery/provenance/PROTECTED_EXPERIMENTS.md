# Protected-history experiments

Question: can confidentiality, key history and concurrent recovery coexist
without confusing local commit, witness acknowledgement or nonce allocation?
Hypothesis: reserving a nonce independently before encryption permits gaps on
failure, while a committed local suffix can reconcile against a lagging witness.
A current witness should reject an old local prefix; restoring both stores is
expected to defeat that freshness assumption.

Controlled variables: public deterministic keys, fixed configuration/ledger ID,
typed synthetic temperature records, one local SQLite implementation and fixed
fault hooks. Independent variables: epoch position, producer interleaving,
process-kill phase, restored store set and nonce/AAD reuse. Instrumentation:
actual child return codes, entry counts, per-entry nonce/key IDs, exact output
objects, SHA256 source fingerprints and runtime versions. No physical sensor,
real private payload or external account is used.

Run from the repository root after installing the optional pinned dependency:

```sh
python3 security-cryptography-mastery/provenance/run_protected.py
python3 security-cryptography-mastery/provenance/protected_experiment.py
```

Record predictions and raw stdout under a new name. Historical records remain
unchanged. The actual author run is in
[protected-observed-2026-10-25.json](evidence/protected-observed-2026-10-25.json);
[the test log](evidence/protected-tests-2026-10-25.txt) contains25 executed tests:
9 preserved provenance contracts and16 protected-history tests. The optional
runner selects the16 protected tests; broad author discovery ran both groups.
The earlier5+20 breakdown was a reporting error, corrected against fresh separate-reader execution; the total25 was unchanged.

| Intervention | Actual observed result | Supported interpretation |
| --- | --- | --- |
| Four alpha entries across schedules | Writer IDs old,old,new,new; encryption IDs old,old,new,new; final numerator25004/1000 | Declared static epochs and retained historical interpretation worked |
| Two real writer processes, six records each | Both exited0;12 entries with12 unique nonces | One finite interleaving preserved per-producer sequence and global serialization |
| SIGKILL after nonce reservation or before local commit | Each child exited−9; recovered count1 after retry, nonce2, replayfalse | Reservation survived failed local append; process-only crash did not reuse nonce1 |
| SIGKILL after local commit or witness update | Each child exited−9; count1, nonce1, replaytrue | Original committed entry survived; retry/reconciliation preserved identity |
| Old local ledger, current authority | Rejected | Independently retained newer head detects this local rollback |
| Matching old copies of both stores | Old count1 accepted | Fresh challenge does not replace independent monotonic authority state |
| Same key/nonce, different AAD | Ciphertext XOR equalled plaintext XOR | Changed context does not repair repeated payload keystream |

Additional tests check inspected NIST vectors,32 polynomial-reduction oracle
cases,16 context/length tag comparisons, wrong validly signed configuration,
changed pinned key/challenge, header/ciphertext/suffix damage, retired keys,
stream policy, skipped/conflicting sequences and a corrupted nonce counter.
These are independent representation/known-value checks within the author suite;
they are not separate-author qualitative review. Root must obtain that review
before assigning a domain gate.

Alternative explanations/limits: SQLite/kernel caches survive process death;
this is not a power-cut experiment. Public keys/data make the run reproducible
but establish no real confidentiality. Same-host store separation does not
enforce a remote trust boundary. A successful finite concurrent run does not
establish arbitrary-schedule fairness or throughput. Whole-pair rollback and
key-domain reuse are intentionally demonstrated premise violations.

Follow-up: independently select new producer schedules and crash positions;
measure full-prefix verification cost with increasing N; implement an authenticated
configuration transition; test witness unavailability without resetting state;
design a separately protected key/backup custody procedure. Those operational
extensions are not claimed executed by this record.
