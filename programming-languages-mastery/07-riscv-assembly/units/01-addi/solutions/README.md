# Answers after attempt

1: rd=2,rs1=3,imm=4. 2: bits 11:7. 3: −1. 4: reads zero and discards arithmetic writes. 5: 8 in this restricted model. 6: 0x00100093. 7: x5 becomes 0xFFFFFFFF. 8: host ordering/alignment and object rules may differ. 9: compute from old state, mask result, suppress writes to zero; all unaffected registers preserve their bounds. New instructions need an inspected contract for decoding, state/memory effects and exceptions. 10: predictions and actual observations must be recorded separately.

[model.py](model.py) is the final reference; [program.s](program.s) is a minimal real assembly sequence.
