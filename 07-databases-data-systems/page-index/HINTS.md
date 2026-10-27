# Hints after an attempt

1–3. Subtract fixed header/CRC bytes before dividing by cell size. Decode signed
integers before comparing. Zero padding is canonical representation, not secrecy.
4–7. The right child's minimum equals its separator. Distinguish keys that route
from records that hold values. Leaf links follow key order, not allocated page IDs.
8–12. A split stages all changed bytes before publication. Minimum occupancy
requires balancing the final bulk group. A checksum-valid graph can still be wrong.
13–18. Valid shape is not transaction history. Trust the declared WAL boundary,
not a snapshot's visual plausibility. State which counts are model page requests
before drawing a device-performance conclusion.
