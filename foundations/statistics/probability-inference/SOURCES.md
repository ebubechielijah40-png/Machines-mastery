# Verified source scopes

Inspection date:2026-10-23. The finite detector model, coverage/dependence
experiments, exercises, derivations and reference code are original. Resources
below verify named definitions and formulas. No copyrighted source text, tables,
figures or problem solutions are reproduced. An open web page is not evidence
of permission to redistribute a whole book.

| ID | Primary source and inspected locator | Supported claims | Boundary |
| --- | --- | --- | --- |
| P-COND | Hossein Pishro-Nik, *Introduction to Probability, Statistics, and Random Processes*, Kappa Research LLC2014, author-hosted [§1.4.0](https://www.probabilitycourse.com/chapter1/1_4_0_conditional_probability.php), definition, positive-denominator condition and probability chain rule. | Finite conditioning by restricted/renormalized mass and the conditional product identity. | We do not use the page's informal zero-probability wording as a theorem about continuous distributions. |
| P-BAYES | Same author/book, [§1.4.3](https://www.probabilitycourse.com/chapter1/1_4_3_bayes_rule.php), conditional-product derivation and partition denominator. Author/title/publication metadata inspected on [book homepage](https://www.probabilitycourse.com/). | Bayes' rule and total probability. | The faulty-parts example and numbers here are constructed independently and are not a measured detector study. |
| P-VAR | Same author/book, [§3.2.4](https://www.probabilitycourse.com/chapter3/3_2_4_variance.php), centered variance, squared units, standard deviation and expansion to E[X²]−E[X]². | Moment definitions and exact algebra. | Floating stability is separately taught in the repository's numerical unit; exact identities do not make all evaluation orders equally accurate. |
| P-BIN | Same author/book, [§3.1.5, Binomial Distribution](https://www.probabilitycourse.com/chapter3/3_1_5_special_discrete_distr.php), PMF and independent-Bernoulli sum. | Binomial mechanism and assumptions. | Only the binomial/Bernoulli portions were inspected for this unit; no claim to full coursebook reconstruction. |
| P-WILSON | NIST/SEMATECH *e-Handbook of Statistical Methods*, [§7.2.4.1](https://www.itl.nist.gov/div898/handbook/prc/section2/prc241.htm), score inversion, formulas, normal-approximation limits and terminology note. | Wilson versus Wald formulas and approximation boundary. | Wilson1927 original paper and cited later comparative papers were not inspected here; this is direct inspection of NIST's own technical handbook, not verification of every cited publication. No uniform95% coverage asserted. |
| P-ENTROPY | C.E.Shannon, “A Mathematical Theory of Communication,” *Bell System Technical Journal*27,379–423 and623–656, July/October1948; corrected [primary-paper reprint](https://people.math.harvard.edu/~ctm/home/text/others/shannon/entropy/entropy.pdf), introduction/log bases, §6 and Theorem2, reprint pp1 and10–11. Publisher metadata for [PartI DOI](https://doi.org/10.1002/j.1538-7305.1948.tb01338.x) and [PartII DOI](https://doi.org/10.1002/j.1538-7305.1948.tb00917.x) inspected. | Finite entropy and units from logarithm base. | Channel coding theorems, continuous entropy and the entire1948 paper are not reconstructed or reproduced by this unit. |

The coverage sum, covariance/copying counterexample and six-assignment
permutation calculation can be checked directly by finite enumeration.
They are original constructions. The randomization argument is conditional
on the stated assignment/exchangeability model, not a claim to have inspected
Fisher's original work or reproduced a published experiment. Exact rational
arithmetic applies to finite masses and target parameters. Score/Wald endpoints
remain floating approximations to theoretical formulas; membership compares
the exact parameter against the actual binary-floating endpoints without
rounding the parameter first. Entropy logs remain approximate. Tiny positive rational entropy contributions can
fall below floating resolution; the implementation avoids taking log of an
underflowed zero but does not promise arbitrary-precision entropy.
