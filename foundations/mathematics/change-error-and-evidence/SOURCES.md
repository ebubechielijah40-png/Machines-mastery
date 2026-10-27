# Inspected sources and claim boundaries

Verification performed 2026-10-22. Original prose/code/derivations in this unit;
no source prose or implementation is copied. Public availability is not a new
license for redistribution. External sources are verification references, not
required tutorials. Inspection scopes below are narrower than full documents.

| ID | Original source | Inspected locator | Supported scope / limit |
| --- | --- | --- | --- |
| S-FLOAT | David Goldberg, “What Every Computer Scientist Should Know About Floating-Point Arithmetic,” ACM Computing Surveys, March 1991, Oracle edited reprint | [Rounding Error; Floating-point Formats; Cancellation](https://docs.oracle.com/cd/E19957-01/806-3568/ncg_goldberg.html), sections with those titles | Finite representation, rounding, and cancellation distinction; edited reprint inspected, not the ACM publisher PDF or a current IEEE standard |
| S-UNCERTAINTY | Barry N. Taylor and Chris E. Kuyatt, NIST Technical Note 1297, 1994 edition, NIST web presentation | [§3](https://www.nist.gov/pml/nist-technical-note-1297/nist-tn-1297-3-type-evaluation-standard-uncertainty), [§5.1–5.2](https://www.nist.gov/pml/nist-technical-note-1297/nist-tn-1297-5-combined-standard-uncertainty), [Appendix A.1–A.5, equations A-1–A-5](https://www.nist.gov/pml/nist-technical-note-1297/nist-tn-1297-appendix-law-propagation-uncertainty) | First-order sensitivities/covariance and uncertainty of independent repeated observations; no blanket normality or confidence coverage claim |
| S-PY-MATH | Python Software Foundation, Python 3.12 documentation | [math.fsum, math.isclose, math.ulp](https://docs.python.org/3.12/library/math.html) | API behavior and precision limitations; runnable evidence uses Python version in results, not necessarily documentation patch version |
| S-PY-STATS | Python Software Foundation, Python 3.12 documentation | [statistics.variance](https://docs.python.org/3.12/library/statistics.html#statistics.variance) | Sample variance definition and distinction from population variance; tests additionally use an exact Fraction oracle |

The attempted BIPM JCGM 100:2008 PDF fetch timed out. No claim is based on
its unseen text. A guessed NIST §4 URL also failed; the inspected §3/§5/Appendix
A suffice for the bounded claims used. Neither source identity nor an API
description verifies a specific experiment; retain the executed evidence.
