# Finite inference: attempt independently

Retain your model, intermediate counts, assumptions and a check independent of
the reference algorithm. Use exact fractions before approximate decimals.

1. **Events.** A device chooses modes A,B,C with masses1/2,1/3,1/6. Compute
   P(not A), P(A or B), and P(A and B). Explain why equally weighting the three
   labels would be another model.
2. **Conditional probability.** For a uniform selector1,…,8, find P(even|≥5)
   and P(≥5|even). Give a zero-mass conditioning event and the required API behavior.
3. **Independence.** Enumerate two independent fair bits. Check independence of
   “first bit is1” and “bits differ.” Compare disjointness with independence.
4. **Bayes.** A constructed fault model has prior1/50, sensitivity4/5 and
   false-positive rate1/25. Derive the positive posterior using both a contingency
   table of2,500 items and the probability formula. Repeat with prior1/2.
5. **Moments.** X is−1,0,2 with masses1/4,1/2,1/4. Compute its expectation,
   variance and the expectation/variance of3X+5. State the units if X is volts.
6. **Uncorrelated dependence.** Let X be uniform on−1,0,1 and Y=X². Show
   Cov(X,Y)=0 yet X,Y are dependent. Explain why zero sample correlation cannot
   certify independence.
7. **Binomial derivation.** List all three-bit sequences with exactly two ones.
   Derive their total probability for p=1/3, then compute E[K],Var(K) for n=3.
   Which derivation step fails when every bit is a copy of the first?
8. **Tail evidence.** For n=4,p_null=1/2 and observed K=3, derive the one-sided
   upper-tail p-value. Explain what it does and does not say about the null.
9. **Intervals.** Derive the Wilson quadratic from its score inequality. At
   K=0,n=5, derive both its endpoints and the Wald endpoints. What happens
   to the coverage definition at the true parameters p=0 and p=1?
10. **Coverage experiment.** Enumerate coverage for n=5,p=1/50 under each
    procedure. Explain why labeling a procedure “nominal95%” is not a proof
    of95% coverage at this pair of parameters.
11. **Permutation.** Enumerate all six two-position assignments for pooled
    values[0,0,1,1]. Derive the exact two-sided absolute-mean-difference p-value
    for original groups[0,0],[1,1]. Why are equal values still distinct positions?
12. **Design critique.** Someone compares slow Monday measurements with fast
    Tuesday measurements, permutes the day labels, and announces that a code
    patch caused the speedup. Identify the missing exchangeability/assignment
    assumptions and propose a controlled collection design.
13. **Entropy and loss.** Compute entropy of probabilities(1/2,1/4,1/4) in bits.
    Compare expected log loss when a model predicts this distribution versus
    a uniform distribution over the same three outcomes. What if it assigns
    zero probability to the third outcome?
14. **Multiple selection.** Derive a bound on the chance of at least one false
    rejection among20 tests, each with chance at most.05 under its null. State
    whether independence is needed for that bound. Why does choosing only the
    best-performing model on the test set change what the test set measures?
15. **Reconstruction.** Without opening the implementation, build a finite
    distribution with explicit mass validation, conditioning, exact binomial
    counts and coverage enumeration. Test it against outcome enumeration rather
    than the same PMF formula. Include deterministic endpoint parameters.
16. **Transfer.** Design an experiment comparing iid20-bit records with records
    made by copying one random bit20 times, holding every bit's marginal p=.2
    fixed. Predict the effect on a Wilson interval incorrectly using n=20.
    State the research question, controls, instrumentation, interpretation and
    one limitation of a finite seeded simulation.

Consult [hints](HINTS.md) after an attempt and [solutions](SOLUTIONS.md) afterwards.
Successful reconstruction needs correct mechanisms and explicit model limits.
