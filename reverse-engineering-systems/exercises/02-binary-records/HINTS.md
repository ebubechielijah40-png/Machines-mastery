# Hints

1–3: Position changes include checksum bytes. Compare1,256 and0x1234.
4: Map the unsigned word w≥32768 to w−65536.
5–6: Preserve length while permuting nonidentical bytes; then change length with zeros.
7: Startffff, XOR the byte into the high byte, then perform eight masked shifts.
8–9: An independent C encoder is a different oracle; validate exact consumption.
10–12: A sender can recompute an unkeyed checksum. New version identifiers must
not reinterpret an old version's fields silently. State your probe distribution.
