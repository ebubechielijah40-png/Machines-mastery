# Separate-author review: finite inference STRONG gate

Root read the new decision implementation, tests, design lesson, source map and
all24 solutions. A separate worker authored them. [The executed reader probes](statistics-reader-probes.json)
come from [review_statistics.py](review_statistics.py); reviewed hashes are retained.
This is team review independent of the code author, not external accreditation
or a learner-completion study.

The three-category coupling proves upper-tail control for the composite null
p≤p0 without a hidden independence-across-looks assumption. The active-state DP
removes first-hit mass and conserves hit plus survival probability exactly.
Ascending sample search explicitly avoids the false integer-n monotonicity
assumption. The lesson separates p-values, size, power, posterior probability,
effect size and causal/measurement evidence. Its fixed horizon and predeclared
spending assumptions are part of the procedure, not implementation details.

Two genuine boundary defects were resolved before the gate:

- A manually constructed negative critical count could index a tail from its
  end. Numeric record validation and permanent regressions now reject it. The
  lesson correctly warns that a valid numeric record alone is not calibrated;
  its claimed size must be derived/recomputed.
- Existing coverage converted an exact rational parameter to float. With
  n=1,p=1/2**1100,Wald intervals are only[0,0] or[1,1], so correct coverage is0.
  The old implementation returned1-p after the target underflowed to0. The
  [initial observation](statistics-coverage-initial.json) retains the case.
  Coverage now keeps its Fraction target; both tiny-p and near-one regressions
  pass. Endpoints still approximate the mathematical Wilson interval; exact
  membership against those actual binary endpoints does not remove that limit.

Independent reader calculations include a three-trial polynomial yielding
size7/250 and power27/125, a minimal n=5 against an all-one alternative, and
an eight-look union computed as1/32+9/256-1/64=13/256. Actual DP outputs match:
repeat13/256,final9/256,spend1/256, with survivor243/256. These use hand-derived
events/polynomials instead of copying the active-count recurrence. Invalid
negative thresholds and exact tiny-probability coverage were also executed.

The full finite unit has27 passing tests, including the prior distribution,
Bayes,moment,interval/permutation checks plus14 new decision tests. New actual
exact experiments record operating curves, bounded minimum sample plans and
first-crossing masses; they are synthetic model calculations, not observed
physical faults or historical paper reproductions. The experiment fingerprints
all five executable files and preserves earlier records.

The fixed finite-inference scope has substantial breadth across probability,
sampling,estimation/testing,design and failure analysis.24 new explained exercises,
separated hints/solutions and a six-milestone guided build complement prior
practice. It now meets readiness90.00, all criterion scores≥87.5, actual tests,
meaningful breadth and separate-author review. No critical defect remains in the
reviewed scope. Continuous/asymptotic/causal and general sequential theory remain
in the separate original-mandate PARTIAL domain. No denominator or scope changed.
