# Twelve bounded investigations

1. Save repeated baseline outputs. What evidence would indicate hidden state?
2. Distinguish8-bit and16-bit sequence fields using a minimal carry probe.
3. Infer sequence and sample byte order independently with asymmetric values.
4. Derive decoding offfff,8000 and7fff as signed16-bit samples.
5. Distinguish a binary length field from null-terminated payloads using00 bytes.
6. Falsify a byte-sum trailer with an equal-sum pair of different payloads.
7. Derive the CRC shift/XOR loop over one byte and compare100 inputs to a library oracle.
8. Explain why encoder/decoder round-trip is insufficient; build a differential test.
9. Reject every truncation, trailing byte and reserved flag with an otherwise valid checksum.
10. Construct two different accepted records to refute checksum-as-authentication.
11. Design a version2 extension and state how a version1 decoder must respond.
12. Reconstruct without references, then run a held probe set and describe the untested input space.
