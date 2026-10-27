# Selected original source inspection

Inspection date2026-10-25. The finite threshold algorithm,coupling proof,exact
sample search,first-crossing dynamic program,examples,practice and experiment
are original. No source text,figures,tables,code or worked source example is
redistributed. Sources support the named design concepts; their presence does
not certify a full statistical theory course or a real experiment's assumptions.

| Source | Actual inspected scope | Use and limitation |
| --- | --- | --- |
| NIST/SEMATECH,*e-Handbook of Statistical Methods*,[§7.2.4 Does the proportion of defectives meet requirements?](https://www.itl.nist.gov/div898/handbook/prc/section2/prc24.htm) | Complete short page: binomial model,choice of direction,normal-score statistic,approximation restrictions and interpretation | Motivation for predeclared direction and proportion testing. Its worked calculation uses a normal approximation; our code enumerates exact finite masses. Wording suggesting that nonrejection validates a null is not adopted: low power can explain nonrejection. A sample-size heuristic on that page is not a universal normal-accuracy theorem. |
| Same handbook,[§7.2.4.2 Sample sizes required](https://www.itl.nist.gov/div898/handbook/prc/section2/prc242.htm) | Complete short page: specified effect,significance,power,normal-based sample-size formula and continuity-correction example | Separates an alternative/effect from a false-alarm budget. Printed conditional-probability lines for significance/power are internally inconsistent and are not adopted. Our definitions come from the explicit exact sampling sums. Our ascending exact search is a different mechanism,not reproduction of the page's approximation or its sample size. The cited Fleiss–Levin–Paik book was not inspected. |

The existing [source map](SOURCES.md) supports finite probability/binomial and
interval definitions already taught here. Optional-stopping inflation and
alpha/N spending are established by this unit's displayed finite event/union
algebra and actual exact model calculations; neither is misrepresented as an
independently inspected historical sequential-testing paper. More advanced
likelihood-ratio/anytime-valid methods remain outside this source scope.

Institutional handbook authorship is retained; no individual author or version
date is invented from a live page. Access does not grant a blanket redistribution
license. Exact probabilities describe the assumed iid generator,not physical
observations,causal identification or a learner's demonstrated understanding.
