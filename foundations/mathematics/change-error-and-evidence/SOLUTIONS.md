# Checkable solutions

1. 0.25 ms =0.00025 s; 0.006/0.00025=24 m/s.
2. The odd terms survive subtraction: 6x²h+2h³. Dividing by 2h gives 3x²+h².
3. Numerator =8xh+4h²-3h. Quotient =8x+4h-3; derivative =8x-3.
4. Mean 2 ms; centered sum of squares 2 ms²; sample variance 1 ms²; SEM
   1/√3≈0.57735 ms. The sample does not establish independent sampling.
5. Mean and SEM divide by 1000; variance divides by 10^6. Physical quantities
   are unchanged because their units changed too.
6. Errors 0.04 and 0.01, respectively. Halving h quarters h²; this exact
   algebra ignores finite arithmetic and holds for this cubic.
7. v=5 m/s. Distance contribution =0.2/4=0.05 m/s; time contribution
   =20*0.08/16=0.1 m/s. u_v=√0.0125≈0.111803 m/s. It is not a coverage interval.
8. Raw squares are about 10^18, while the numerator variance term is about
   five. Small errors in the large sums can consume that difference. For
   [10^9+1,...,+4], exact mean is 10^9+2.5 and variance is 5/3. The tests
   compute a rational oracle independently. Do not demand one particular
   incorrect result from a different float implementation.
9. For h>0, (|h|-0)/h=1; for h<0 it is -1. Their unequal limits preclude a
   derivative. Symmetry forces central zero despite nondifferentiability.
10. Estimated random uncertainty of the mean decreases under the assumptions;
    bias remains +0.1 s. A calibrated reference or second measurement method
    could identify it, subject to its own uncertainty. More repeats alone cannot.
11. Choose Z=+1 or -1 with equal probabilities. a=Z,b=-Z have variance one,
    covariance -1, and a+b=0 every draw. Merely setting ρ=-1 in a calculation
    does not supply evidence that actual measurements have this relation.
12. Compare your run with RESULTS; the interpretation is assessed, not a
    memorized last decimal. Report rejections as failures of representability.
13. τ perturbation is CΔR+RΔC+ΔRΔC. Neglect the product for small relative
    uncertainties: u_τ²=C²u_R²+R²u_C²+2RC Cov(R,C). Units are s² since Ω·F=s.
    If independent, covariance is zero; independence requires a measurement
    argument. Large component uncertainties can make the neglected product
    significant. Rebuilding reference code is insufficient: show a new hand
    case, input rejection, numerical-oracle test and limitation.
