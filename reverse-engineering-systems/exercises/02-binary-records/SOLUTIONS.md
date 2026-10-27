# Reference model after the attempt

| Zero-based location | Meaning |
| --- | --- |
|0–1|magic4d58|
|2|version1|
|3|enabled bit0, all other bits zero|
|4–5|unsigned sequence, little endian|
|6–7|sample modulo65536, big endian, signed two's-complement interpretation|
|8–9|payload length, little endian, limited0–32|
|10 through10+length−1|opaque payload bytes|
|final two|CRC16 over all preceding bytes, stored big endian|

The candidate CRC startsffff, XORs each byte shifted left8, then repeats eight
times: shift left one; if the old high bit was1, XOR1021; retain low16 bits.
For ASCII'123456789' it returns29b1 and agrees with Python `binascii.crc_hqx`
with initialffff over the finite tested lengths. No keyed secret enters it.

1. Repeated identical outputs support determinism for those probes; different
   outputs would require testing a counter, timestamp, random field or unstable build.
2. Sequence1 then256 distinguishes a low-byte carry into a second position.
3. Sequence0x1234 gives34,12; sample0x1234 gives12,34. Whole-record byte order fails.
4. ffff→−1,8000→−32768,7fff→32767 under w−65536 for the high-bit-set words.
5. A zero payload increases length and emitted byte count. It is data, not a terminator.
6. Payload41ff andff41 preserve a sum; actual trailers5df6 and26e1 reject that model.
7. The shift loop above is the reference; `test_binary_records.py` compares100
   independent inputs to the library. A lone standard check value is insufficient.
8. A reversed-order encoder and reversed-order decoder can round-trip perfectly
   and still disagree with the target. Asymmetric fixed words/native output reject it.
9. Check bounded bytes input, header semantics, exact length and CRC. Recomputing
   a trailer for a reserved flag does not legalize that flag.
10. Encode sample0 and sample1 with newly computed trailers. Both are accepted:
    integrity against accidental changes is not sender authentication.
11. A new version can introduce a larger field under a new identifier. The old
    decoder rejects version2 rather than guessing a compatible old interpretation.
12. Compare fresh held cases, retain failures and bound the claim to observed
    behavior and the explicit schema. Closing source files does not create a
    security boundary. [reference/reconstruction.py](reference/reconstruction.py)
    is the readable Python implementation after the learner's independent build.
