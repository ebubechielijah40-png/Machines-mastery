# Actual local provenance investigation

Question: which attacks differ from an authenticated false claim? Hold public synthetic keys, schema, allowed stream and transform fixed; vary mutation, replay, forbidden stream and complete suffix deletion. Fragment the signed request through the bounded frame decoder in three-byte chunks before ingestion. Instrument decoder peak storage, accepted tip, exact output and exception class.

Run `python3 security-cryptography-mastery/provenance/experiment.py`. The [actual JSON](../../security-cryptography-mastery/provenance/evidence/observed.json) records a184-byte framed request, output25001/1000 Celsius, replay SequenceError, forbidden stream AuthorizationError and mutation IntegrityError. A correctly tagged120000 milli-Celsius claim is accepted; source truth remains unverified. A valid one-line prefix reopens without a checkpoint and rejects against the retained latest tip.

Alternative explanation for a valid tag is another holder of the shared key. The trial does not measure physical truth, brute-force resistance or network security. Follow-up: implement independent checkpoint persistence and inject failure between append and checkpoint publication; define recovery before claiming freshness across crashes.
