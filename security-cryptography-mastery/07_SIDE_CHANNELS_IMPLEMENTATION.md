# Implementation and side channels

Correct mathematics can leak through timing, caches, branches, power, faults, memory reuse, logging, or error messages. Constant-time requirements depend on threat model and implementation. Exercise: write an intentionally early-exit string comparison and measure timing statistically over many trials; contrast with a constant-time comparison primitive, while noting that high-level timing experiments are noisy and do not prove hardware-level resistance.
