# Hints

1. Modes are mutually exclusive outcomes; an event can contain several modes.
2. Draw the retained outcomes for each denominator; the two conditionals need
   not have the same denominator even if they happen to agree here.
3. Use four labeled pairs, each with mass1/4. For the second event, keep01 and10.
4. At prior1/50, the constructed batch has50 faults. Count positives separately
   within faulty and nonfaulty groups before adding them.
5. Find E[X] and E[X²] exactly, then use Var(aX+b)=a²Var(X).
6. E[X]=E[X³]=0. Conditional on Y=0, X cannot be±1.
7. Positions110,101,011 are distinct paths. Multiplying marginal probabilities
   along a path uses independence.
8. Include the observed statistic and all larger counts under the predeclared
   direction. A posterior needs a prior over hypotheses.
9. Multiply the score inequality out before applying the quadratic formula.
   At K=0 it factors as p*((n+z²)p−z²)≤0.
10. Check exactly which counts' intervals contain.02. The binomial probability
    of K=0 is(49/50)^5.
11. There are two ways to obtain absolute difference1; the other four split
    the zeros and ones evenly across groups.
12. A shared change in load or temperature can align with day. Randomize patch
    order or block by collection period and keep raw outcomes.
13. Use−log₂(1/2)=1 and−log₂(1/4)=2. A uniform predictor charges log₂3 bits
    for every outcome. Positive mass times infinite log loss stays infinite.
14. Use P(union of false-rejection events)≤sum of their probabilities. This
    is an upper bound and can be weak.
15. Mutate the caller's input dictionary after construction; the model should
    retain its own masses. Include a zero-probability conditioning event.
16. The copied record only has possible counts0 or20. Compare both returned
    intervals with the true parameter.2 before simulating.
