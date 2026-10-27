# Model limits

The implementation represents normalized pure states, ideal local unitary gates, CNOT and computational-basis projective measurement. It is a classical dense-vector simulation with exponentially growing storage. `norm()` means squared norm for backward compatibility. Sampling means many fresh preparations; measuring means modifying one conditional state.

No device, pulse, cooling system, electronics, noise channel, density-matrix engine, general POVM, tomography, error-correcting code, logical-qubit overhead, quantum compiler or research algorithm speedup is implemented here. A Bell computational-basis correlation can also arise from a classical mixture; the XX comparison distinguishes the specified preparations within the adopted model but is not a physical Bell inequality experiment.

Normalization tolerance and binary floating point permit roundoff and underflow; no rigorous long-circuit error bound is supplied. The n<=20 guard bounds a typical single state, not total process memory or parsing of arbitrarily large supplied iterables. Untrusted remote execution would require additional isolation and resource controls. See [production considerations](PRODUCTION.md).
