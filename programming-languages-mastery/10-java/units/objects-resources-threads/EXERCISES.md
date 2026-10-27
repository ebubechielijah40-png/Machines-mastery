# Exercises

1. Draw array identities for the broken and copied Packet constructors.
2. Explain why final byte[] does not imply immutable bytes.
3. Break ownership through an accessor, then repair it without changing callers.
4. Contrast mutating an argument's object with rebinding a local parameter.
5. Trace resource initialization/use/closing when the body and both closes throw.
6. Change the body to return normally while both closes fail. Predict which
   exception is primary, then test the extension before recording actual results.
7. Trace two volatile read/write increments with the barrier. Why is result1
   compatible with volatile semantics?
8. Repair the whole operation with an atomic update and with one monitor.
9. Explain what a successful join establishes and what an interrupt request does not.
10. Inspect bytecode for copying and bounds, then distinguish it from JIT assembly.
11. Add an initializer-failure case and verify which prior resource closes.
12. Reconstruct all three mechanisms without copying and keep an intended failure
    for each mistaken rule: final means deep freeze, GC means prompt close,
    volatile means compound atomicity.
