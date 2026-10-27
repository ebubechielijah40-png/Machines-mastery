# Exercises — attempt before opening solutions

Save working, units, assumptions and any code under your own notes.

1. **Basic:** Convert 0.25 ms to s. A displacement of 0.006 m occurs in that
   interval. Calculate average velocity, with units.
2. **Basic:** Expand `(x+h)^3-(x-h)^3` without using a derivative rule.
3. **Basic:** Derive the forward quotient for `f(x)=4x²-3x+2` and take its limit.
4. **Basic:** For `[1,2,3]` ms, compute mean, sample variance and SEM by hand.
5. **Basic:** What happens to mean, variance and SEM when every reading changes
   units from ms to s? Distinguish value from physical quantity.
6. **Application:** At x=2, find the exact central quotient error of x³ for
   h=0.2 and h=0.1. Explain the ratio rather than reporting it alone.
7. **Application:** A speed estimate uses 20 m / 4 s, standard uncertainties
   0.2 m and 0.08 s, and ρ=0. Calculate its standard uncertainty.
8. **Application/debugging:** Why does variance from subtracting raw squares
   fail for large-offset samples? Compare to the exact Fraction calculation.
9. **Reasoning:** A central quotient of |x| at zero returns zero. Give the
   conflicting one-sided quotients and the conclusion.
10. **Reasoning:** A sensor with a common +0.1 s offset collects a million
    independent noise samples. What shrinks, what remains, and what extra
    observation would identify the offset?
11. **Challenge:** For y=a+b where uncertainties are u_a=u_b=1 and correlation
    -1, the linear variance is zero. Construct a random-variable example where
    this is exactly correct. Contrast it with merely assuming correlation -1.
12. **Experiment:** Predict and run the step sweep. Identify at least one
    rejection or reversal of improvement; explain why another Python/platform
    need not yield the same last decimal. Preserve the output.
13. **Transfer/reconstruction:** Close this repository and rebuild the three
    numerical mechanisms and their checks. For an RC time constant τ=RC,
    derive the first-order uncertainty including covariance. State the units,
    independence assumption and a case in which linearization fails. Passing
    requires an original test with different values and a defended limitation.
