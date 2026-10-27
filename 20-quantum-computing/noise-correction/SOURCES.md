# Inspected source map — 2026-10-23

All local prose, derivations, examples, matrix code, recovery code and synthetic
calculations are original. No source notebook, figure, chapter or hardware result
is redistributed as a local result.

| Source | Inspected sections supporting technical context | Limits |
| --- | --- | --- |
| IBM Quantum Learning, [Noise and errors](https://quantum.cloud.ibm.com/learning/en/courses/tools-for-quantum-advantage/noise-and-errors), accessed2026-10-22/23 | Density operators and coherence; channel constraints/Kraus completeness; energy relaxation and random phase flips, including nonmonotone coherence under a certain Z | Live unversioned course page. Local parameters/examples and code differ. No physical plots, fitted errors, device T1/T2 or Qiskit notebook were independently reproduced |
| IBM Quantum Documentation, [Repetition codes](https://quantum.cloud.ibm.com/docs/en/tutorials/repetition-codes), accessed2026-10-22/23 | Background explicitly limiting bit-flip protection; parity measurements with ancillas; conditional corrections | The published hardware memory demonstration uses a logical basis state and notes its classical-information limit. Local work instead models ideal projection on arbitrary complex encoded states. No IBM runtime job, hardware lifetime or fault-tolerant threshold claimed |

Our parity convention(s0=q0 XOR q1,s1=q1 XOR q2) is explicitly defined and differs
from an equivalent pairing in the inspected IBM circuit. Its correction table
is derived and exhaustively tested locally. The polynomial3p²−2p³ follows from
our independent single-cycle X-error assumptions; it is not a reported device
benchmark. Author textbook full chapters and research-paper reconstructions
remain uninspected here, so this unit does not count as completing those records.
