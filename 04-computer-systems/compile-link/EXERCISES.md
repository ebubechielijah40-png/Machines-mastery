# Exercises — predict before compiling

1. What can a function declaration establish that a definition supplies differently?
2. Predict `nm`'s classification for `sum_bytes` in caller and implementation objects.
3. Calculate the output for bytes0,255,1. State the pointer/length obligations.
4. Why is null data with zero length permitted while null output is not?
5. If the header is present but the implementation object omitted, which stage fails?
6. Explain the observed `lea`/`add` arithmetic without claiming a memory load.
7. Why can a stack-frame drawing disagree with optimized assembly without either
   executable producing a different answer on valid inputs?
8. Design a valid test that detects writing the output before input validation.
9. Which additional specification details would a three-argument floating-point
   or structure-return function require beyond this observed two-integer example?
10. Experiment: remove the implementation object, then restore it; retain both logs.
11. Transfer: build a separate checksum routine, caller and test executable with
    unsigned bytes, a caller-supplied output and an explicit failure-atomic contract.
12. Close all reference code and rebuild the two-unit example. Deliver a hand trace,
    both object inspections, a deliberate failure and a defended limitation.
