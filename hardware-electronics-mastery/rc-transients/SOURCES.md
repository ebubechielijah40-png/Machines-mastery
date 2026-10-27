# RC source verification and original derivations

Inspected 2026-10-22. No source PDFs, figures, prose or implementations are
redistributed. Public access does not establish permission to redistribute a
particular artifact. This record covers the RC unit, not the entire hardware track.

| ID | Primary institutional source | Inspected locator | Claim scope and limits |
| --- | --- | --- | --- |
| RC-MIT | Manos Chaniotakis and David Cory, MIT 6.071/22.071, Spring 2006, *Transient Analysis of First Order RC and RL circuits* | [Original lecture PDF](https://ocw.mit.edu/courses/6-071j-introduction-to-electronics-signals-and-measurement-spring-2006/4b6a5fe626d65de20ceb97d8d23f38a4_transient1_rl_rc.pdf), printed pp.1–3,6,9–10, equations0.2,0.10,0.19,0.23–0.31 | RC initial state, first-order equation, time constant, equivalent resistance, source-free and constant-driven response. Metadata title returned by the reader differs from the PDF's visible opening title; use the latter. Other RL/pulse sections are not claimed as reconstructed here |
| RC-NIST | Barry N. Taylor and Chris E. Kuyatt, NIST TN1297 (1994 edition), web presentation | [§5.1–5.2](https://www.nist.gov/pml/nist-technical-note-1297/nist-tn-1297-5-combined-standard-uncertainty); [Appendix A, equationsA-3,A-7](https://www.nist.gov/pml/nist-technical-note-1297/nist-tn-1297-appendix-law-propagation-uncertainty) | Combination of standard uncertainties, covariance and first-order approximation; uniform-bound standard deviation. Tolerance distributions and independence in the example are hypothetical assumptions, not measurements |
| RC-PY | Python Software Foundation, Python3.12 documentation | [math.expm1 and math.log1p](https://docs.python.org/3.12/library/math.html) | Library entry points used for small-change arithmetic; local behavior is separately tested |

The loading branch, Euler error multipliers, backward-Euler rearrangement,
energy arithmetic, interval bounds and synthetic examples are original
derivations in the lesson. Tests compare them to distinct analytic/invariant
oracles. No claim of physical validation follows. No instrument datasheet was
inspected; all meter/probe values are explicitly hypothetical.
