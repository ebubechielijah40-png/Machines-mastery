# Solutions and independent checks

1. P(not A)=1/2, P(A or B)=5/6, intersection0. Uniform thirds would replace
   the specified mechanism, not simplify its arithmetic. Validate total mass
   before computing; an incomplete total should not be silently normalized.
2. Retained≥5 outcomes are5,6,7,8, two even:1/2. Retained even outcomes are
   2,4,6,8, two≥5:1/2. Agreement in this example does not make conditioning
   symmetric. P(even|>8) is undefined by this finite rule; raise ValueError.
3. The first-bit event contains10,11; differing bits contains01,10. Intersection
   is10 with probability1/4, the product of1/2 and1/2. They are independent
   despite overlapping. Positive-mass disjoint events have intersection0 and
   cannot have a positive product, so cannot be independent.
4. There are50 faults with40 positives, and2,450 nonfaults with98 positives.
   Posterior40/138=20/69≈.289855. The formula uses evidence
   (1/50)(4/5)+(49/50)(1/25), giving the same ratio. At prior1/2 the posterior
   is(.5·.8)/(.5·.8+.5·.04)=20/21≈.952381. These are exact constructed
   proportions; no empirical detector performance is being reported.
5. E[X]=−1/4+2/4=1/4. E[X²]=1/4+4/4=5/4, so variance=19/16.
   E[3X+5]=23/4 and variance=9·19/16=171/16. If X is volts and3 is a
   dimensionless gain, the offset5 must also be volts; variance is volts².
   Adding an offset changes expectation, not variability about that expectation.
6. E[X]=0,E[Y]=2/3,E[XY]=E[X³]=0, so covariance0. Yet P(X=0|Y=0)=1
   while P(X=0)=1/3. This explicit conditional change proves dependence.
   A correlation statistic summarizes a particular linear relationship, not
   every possible dependence or collection defect.
7. Paths110,101,011 each have mass(1/3)²(2/3)=2/27, totaling2/9.
   E[K]=1 and variance=3·(1/3)(2/3)=2/3. Copied bits only allow000 or111;
   the path probabilities no longer multiply independently. Although the
   marginals still have p=1/3 and E[K]=1, variance becomes9·(2/9)=2.
8. P(K≥3)=choose(4,3)/16+choose(4,4)/16=5/16. Under the predeclared
   null process, that tail event is not rare at the usual.05 threshold. This
   is neither a posterior probability for the null nor proof that it is true.
   A real decision also requires effect size, collection design and consequences.
9. Expanding gives(n+z²)p²−(2K+z²)p+K²/n≤0. Its roots give the Wilson
   endpoints. At K=0 they are0 and z²/(5+z²)≈.43448 for the stated z.
   Wald returns[0,0]. At true p=0, only K=0 occurs; at true p=1, only K=n
   occurs. Wilson must include the corresponding exact endpoint so coverage
   is1. Floating formulas can otherwise round an endpoint inward; this bug
   was independently discovered and has an explicit regression test.
10. For Wilson, only K=0 includes.02 at this n, so coverage=(49/50)^5
    =282475249/312500000≈.9039208. For the clipped Wald procedure, counts
    1 and2 include.02, while0,3,4,5 do not. Coverage is the binomial mass
    of{1,2}, approximately.09600. Use the exact [executed record](evidence/observed-2026-10-23.json)
    to check the full rational sum. The normal-score approximation improves
    this boundary example greatly but still does not give universal95% coverage.
11. Positions(0,1) and(2,3) place both zeros or both ones in A, giving absolute
    mean difference1. The four other pairs give difference0. Thus p=2/6=1/3.
    Equal values can arise from different assigned units. Deduplicating them
    changes assignment multiplicities and hence the randomization distribution.
12. Day may correlate with workload, hardware temperature, input mix or caching.
    Under such changes, shuffling labels does not describe the actual assignment
    or guarantee exchangeable outcomes. Define a workload and metric, randomize
    patched/unpatched order within comparable blocks, retain every result,
    and record warmup, failures and environmental measurements. Even a well
    controlled local benchmark has limits on transfer to another deployment.
13. Entropy=.5·1+.25·2+.25·2=1.5 bits. Correctly predicting p has expected
    log loss1.5 bits. Uniform predictions give log₂3≈1.584963 bits. Assigning
    q₃=0 where p₃=.25 yields infinite expected log loss; a zero predicted
    probability forbids an outcome that the declared data model can produce.
    These ideal expectations do not imply that a finite test-set loss estimates
    the intended deployment expectation without sampling assumptions.
14. The union bound gives at most20·.05=1, a valid but uninformative upper
    bound here. No independence is needed. If these rejection events were
    independent with probability exactly.05 each, the chance would be
    1−.95²⁰≈.6415. Selecting the best model using the test set adapts to that
    set's noise and makes it part of selection. A fresh evaluation is then
    needed for an independent assessment of the selected procedure.
15. Keep exact rational masses, validate their sum and reject a zero conditioning
    denominator. Enumerate binary sequences independently to check binomial
    counts. Verify moments, conditioning, deterministic endpoint coverage,
    invalid inputs and caller-mutation behavior. Passing tests establish
    the checked implementation behaviors, not the adequacy of a physical model.
16. For copied records, K is0 with probability.8 or20 with probability.2.
    At n=20 the Wilson upper endpoint for0 is≈.1611 and lower endpoint for20
    is≈.8389, so neither includes.2: coverage is exactly0 for this incorrectly
    assumed iid procedure. Controls include n, each marginal p, interval method
    and replication count; vary only dependence. Instrument count distributions
    and interval inclusion. Compare with exact iid coverage and both possible
    copied counts. A finite seeded simulation has sampling error and cannot
    certify an arbitrary dependent process, although this particular copied
    process also admits an exact two-outcome calculation.
