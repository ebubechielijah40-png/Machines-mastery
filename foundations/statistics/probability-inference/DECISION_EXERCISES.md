# Exact decisions and repeated looks: exercises

Read [the design lesson](DECISION_DESIGN.md), make an independent attempt, then
use [hints](DECISION_HINTS.md) and [solutions](DECISION_SOLUTIONS.md).

1. For a local fault-injection study, specify the observed bit, statistic,
   population/process parameter, upper-direction null and alternative. Give one
   collection failure that invalidates the intended count model.
2. Derive the five-trial fair-binomial numerators without calling a library.
   Compute upper tails atc=3,4,5,6.
3. Forn=5,p₀=.5, derive critical counts and actual sizes atα=.25 and.05.
   Explain why actual size need not equal the selected budget.
4. Prove tail probability decreases asc increases. Why does the smallest
   calibratedc maximize power within this threshold family?
5. Construct the finite three-category coupling forp=.3,p₀=.5. Prove the
   upper rejection bound for everyp≤p₀, stating the trial assumptions.
6. Distinguish p-value, size, power and posterior probability using their
   denominators. Why does failing to reject not validate the null?
7. Compute exact power atp₁=.7 for then=5,c=5 rule and its miss probability.
   State the effect size; explain what changing that alternative changes.
8. Derive the power ofn=6,c=6 at the same alternative. Explain why a binary
   search assuming power grows at every integern is unjustified.
9. Implement ascending bounded minimum-n search. What must its output preserve
   to substantiate minimality? Interpret a no-hit result atmax_n=4.
10. For the observed minimum37 atp₁=.7,target.8, independently recalculate its
    critical count/size/power and verify every earlier size fails. What does this
    establish, and what physical claim does it not establish?
11. Considerα=0,p₀=0. Derive a possible critical rule with zero false-alarm
    mass. Compare withp₀=1,α=0, and explain why degenerate tests are useful checks.
12. Explain why using an upper tail only after observing a high count changes
    the testing procedure. Give another example of selecting a favorable analysis.
13. For fair bits,α=.05, derive the ten-look13/256 ever-rejection probability
    by identifying first crossings. Why are there no new hits atlooks6,7,9,10?
14. Give a path counted by two fixed-look rejection events. Explain why summing
    those tails is not the probability of any rejection and why treating looks
    as independent is also unjustified.
15. Derive the active-count recurrenceAₜ(k), first-hit masshₜ and conservation
    invariant. Identify the exact line of reasoning that prevents double counting.
16. Enumerate all binary paths through8 looks, compute each path's first hit,
    and compare with the dynamic program. State why an oracle needs a smalln cap.
17. Derive alpha/N spending's overall upper bound without assuming independent
    looks. Does the coupling proof also coverp≤p₀ for this policy?
18. AtN=100, compare final-only,repeatedα andα/N spending from the raw report.
    Explain what was held fixed and why the spending result may be conservative.
19. Explain what changes if horizonN is extended after seeing the outcomes.
    Does the originalα/N allocation automatically certify the extension?
20. State time/state-count bounds for the DP and distinguish rational-operation
    counts from machine-time/bit complexity. Why bound rational input sizes too?
21. A manually constructedUpperTest claimssize0 but usesc=1,n=5,p₀=.5.
    Calculate actual size. Why does a range-valid record not certify calibration?
22. Convertα=.05 into exact Fraction form. Explain the difference between
    Fraction(1,20) andFraction(.05), and design a threshold-boundary check.
23. Transfer the design to a software-error experiment. Specify predeclared
    model, effect, stopping rule and a measurement/dependence check. Explain why
    an exact conditional calculation cannot establish a causal effect.
24. Reconstruct upper-tail calibration and the first-crossing DP from memory.
    Submit a hand example, a fresh implementation, an independent path oracle,
    actual operating curves, a deliberately double-counting implementation and
    an explanation of its failure. State one limit that passing tests cannot remove.
