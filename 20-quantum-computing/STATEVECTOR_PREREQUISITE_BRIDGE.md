# Statevector prerequisite check

This is author preparation; no learner readiness or mastery is asserted. If you cannot perform a row's diagnostic, use the internal bridge and retry. The main lesson introduces the exact complex arithmetic, tensor convention, matrix action and measurement formulas it needs. General prerequisite guides remain partial; passing a filename check is not readiness.

| Domain | Needed now | Diagnostic / internal bridge |
| --- | --- | --- |
| Mathematics | Fractions, square roots, complex conjugate, vectors and matrix multiplication | Compute `(2+i)*(2-i)`; then [math guide](../foundations/mathematics/DEEP_GUIDE.md) and lesson sections 1–4 |
| Statistics/probability | Exclusive outcomes, sums, conditional probability, finite sampling | Explain why the uncertainty of a frequency is not zero after 100 shots; [statistics guide](../foundations/statistics/DEEP_GUIDE.md) and experiment derivation |
| Programming | Python lists, loops, bit shifts, functions, assertions/exceptions | List indices whose bit 1 is zero for n=3; [Python guide](../programming-languages-mastery/08-python/DEEP_GUIDE.md) |
| Prior systems | Representation versus physical device; array index convention | Explain why q0 is the rightmost displayed bit but address 0; lesson section 4 |
| Physics | Scope of an ideal model; no previous quantum mechanics needed | State that the Born rule is adopted, not derived from the simulator. Gate/pulse physics is deferred |
| Electronics | Not required for this mathematical mechanism | No voltage, current or circuit hardware is built. Required later for physical control/readout |
| Chemistry/materials | Not required for this mathematical mechanism | No fabrication/device-material claim is needed; those prerequisites belong to later hardware units |

Reconstruction check before coding: multiply H by `(1,0)`, H by `(1,-1)/sqrt(2)`, and compute the probabilities for `(1/2, i sqrt(3)/2)`. The answers are available in the lesson mechanisms; write an attempt before looking them up.
