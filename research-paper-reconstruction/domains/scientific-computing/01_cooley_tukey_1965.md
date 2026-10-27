# Fourier transforms: reduce arithmetic by exposing repeated subproblems

James W. Cooley and John W. Tukey, *An Algorithm for the Machine Calculation of
Complex Fourier Series*, Mathematics of Computation19(90),297–301, April1965.
Inspected [original-paper scan](https://www.ece.ucdavis.edu/~bbaas/281/papers/CooleyTukey.1965.pdf),
all five printed pages. [Source verification](../../SOURCE_VERIFICATION_CONTINUATION.json).
**STRONG bounded algorithm reconstruction; historical hardware performance NOT
REPRODUCED.** No paper text, figures or source program is bundled.

## 1. Historical context

[SOURCE CT65,p.297] The paper relates composite-length Fourier calculation to
earlier factored-transform work, including Good. It is not presented as the
first possible observation that structured transforms can reuse arithmetic.

## 2. Unresolved problem

[ORIGINAL] Given n complex samples, calculate n frequency coefficients defined by
a sum. Direct evaluation recomputes many related rotations. At n=1024, over a
million sample/frequency products appear; identifying common structure can
matter more than making one multiplication slightly faster.

## 3. Why it matters

Transforms connect signals, convolution and numerical equation solving. An
algorithmic cost reduction can change feasible input sizes. It does not by itself
solve sampling, aliasing, conditioning, memory locality or measurement validity.

## 4. Previous approaches

[SOURCE CT65,pp.297–298] Direct summation and factored transforms provide the
comparison context. [ORIGINAL] A loop optimized to compute the same n² products
retains quadratic growth. A transform factorization changes the computation's
dependency graph rather than merely its implementation constants.

## 5. Limitations of the baseline

The direct definition remains valuable as an independent oracle for small n.
Discarding it because it is slow removes a clear specification. It also handles
non-power-of-two sizes, which our restricted radix2 implementation rejects.

## 6. Research question

How can a composite transform be decomposed into smaller transforms, with
practical index/storage choices for binary machines? Separate the general
factorization question from the narrower radix2 program developed here.

## 7. Central insight

[SOURCE CT65,pp.298–300] Factorization exposes smaller sums and index-dependent
rotations; binary index structure permits staged paired updates. [ORIGINAL]
The essential economy is reuse: calculate each half-size transform once and
combine it into two related output halves.

## 8. Complete mathematical derivation and hand example

Use the paper's positive-sign convention, with `w_n=exp(2πi/n)`:

\[
X_k=\sum_{j=0}^{n-1}x_jw_n^{jk}.
\]

For even n, split j=2r and j=2r+1. Since `w_n²=w_(n/2)`, define the half-size
transforms E and O of even and odd samples. Then
`X_k=E_k+w_n^k O_k`. For the second half, `w_n^(k+n/2)=-w_n^k`, giving
`X_(k+n/2)=E_k-w_n^k O_k`. These are the two butterfly outputs.

Take `[1,2,3,4]`. Even samples `[1,3]` give E=`[4,-2]`; odd samples `[2,4]`
give O=`[6,-2]`. Rotations for k=0,1 are1 and i. Thus outputs are
`[10,-2-2i,-2,-2+2i]`. For a negative-sign convention the imaginary signs reverse.
Neither output is wrong without first agreeing on the definition.

At each of log2(n) stages there are n/2 butterflies, each one value multiplication
and two additions in our counted code. This yields n*log2(n)/2 such
multiplications. Root generation, data movement and interpreter overhead are
outside that count. The recurrence `T(n)=2T(n/2)+O(n)` gives O(n log n).

## 9. Architecture and index consequences

[Original code](../../../projects-guided/p16-research-reproduction/code/fourier.py)
first bit-reverses indices, then combines spans2,4,8,... to produce natural-order
output. For n=8, reversed three-bit indices are0,4,2,6,1,5,3,7. This arrangement
places each smaller transform's operands together before its stage.

The code copies input and generates root arrays. It is not the historical
program nor a claim to reproduce its exact in-place storage layout. The source's
bit-order discussion motivates this original explicit convention [CT65,p.300].

## 10. Experimental design

[SOURCE CT65,pp.300–301] The article reports IBM7094 transform timings for chosen
array shapes. Our local experiment instead freezes seeded complex arrays, varies
power-of-two length and compares direct definition versus the radix2 mechanism.
Five complete elapsed-time repetitions are retained per length; no cherry-picked
minimum replaces their distribution.

## 11. Baselines and metrics

Direct DFT is the correctness and cost baseline. Metrics are maximum absolute
coefficient difference, specified arithmetic counts and repeated local elapsed
time. Inverse round-trip alone is insufficient: matching mistakes in a forward
and inverse implementation can cancel. Independent hand/DFT/convolution/energy
oracles therefore supplement it.

## 12. Actual reported findings and executed observations

[SOURCE CT65,p.301; reported, not reproduced] The one-dimensional2^11 case is
listed as0.02 minutes and2^12 as0.07 minutes on the stated historical program.
Those values are not modern Python targets and do not establish current speedups.

[EXECUTED HERE] [Raw JSON](../../../projects-guided/p16-research-reproduction/evidence/fourier.json)
retains all local timings and discrepancies for n=8 through256. At n=256 the
direct definition has65,536 value multiplications; the local radix2 loop counts
1,024 butterflies. Inspect the actual discrepancy/time fields rather than
equating those operation counts with a wall-clock ratio.

## 13. What the evidence supports

The algebra establishes the factorization in exact arithmetic. Tests check a
specific finite implementation against direct summation, analytically known
signals, a nested-loop convolution oracle and Parseval's identity. Observed
timings characterize this runtime and workload only.

## 14. What it does not establish

No historical source code, IBM7094 run, real measured spectrum, universal
floating-point error bound or optimal modern FFT implementation was reproduced.
An FFT coefficient has no physical frequency unit until sampling interval is
specified. A clean spectrum cannot prove the original sensor was calibrated.

## 15. Limitations

Radix2 restricts n to powers of two. Padding changes transform size and frequency
grid; it does not manufacture additional observed signal duration. The model
caps input at4096 points and keeps complex arrays in Python memory. NaNs/infinity
are rejected. Roundoff order differs from the direct sum and can depend on scale.

## 16. Subsequent developments

Mixed-radix, prime-length and hardware-tuned transforms are relevant extensions,
but their original papers/benchmarks were not inspected here. They remain
**UNVERIFIED — verification required** rather than attributed retrospective
achievements of this paper. The local input guard is an honest algorithm boundary.

## 17. Reproduction requirements

The mechanism requires Python3.10+ only. Historical performance would require
the exact machine, program, compiler, numeric format, layout and timing method;
those artifacts are not supplied. Modern numerical reproduction should declare
sign, normalization, shape, dtype and input generation before comparison.

## 18. Implementation exercises

Derive the four-point result without code, rebuild butterfly stages and test
the negative-sign mismatch deliberately. Prove the circular-convolution identity
by substituting the finite sums. See [project exercises](../../../projects-guided/p16-research-reproduction/EXERCISES.md)
and separated hints/solutions. Do not consult the reference until predictions exist.

## 19. Connections

The transform is a structured [linear map](../../../foundations/mathematics/README.md).
Complex phase carries information that probabilities alone discard, also visible
in the [quantum interference lesson](../../../20-quantum-computing/10_STATEVECTOR_MEASUREMENT.md).
Those mathematical connections do not imply an FFT simulation is quantum computation.

## 20. Open questions

Which cost dominates first as n grows: arithmetic, root generation, allocation
or cache behavior? How does an alternative permutation schedule change it?
Can a length with prime factors outside2 be handled without hiding a direct
quadratic fallback? Build and measure one declared extension; preserve accuracy
checks alongside its performance evidence.
