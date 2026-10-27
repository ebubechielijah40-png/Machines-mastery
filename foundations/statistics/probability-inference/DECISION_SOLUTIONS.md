# Checkable decision solutions

1. One trial might be one predeclared test execution,bit1 if its recorded fault
   criterion fires. K counts faults,p is the modeled per-trial fault probability,
   H₀:p≤p₀,H₁:p>p₀. Omitting crashed executions, changing inputs adaptively or
   sharing an unmodeled state across trials can break the intended iid model.
2. Counts are1,5,10,10,5,1 over32, either by Pascal's recurrence or enumerating
   labeled positions. T(3)=16/32,T(4)=6/32,T(5)=1/32,T(6)=0.
3. Atα=1/4,c=4,size3/16. Atα=1/20,c=5,size1/32. Available masses are discrete;
   no upper threshold has exactly the budget here. Equality is not required for
   an upper bound. Randomizing a boundary would change the mechanism.
4. {K≥c+1}⊆{K≥c}; probability and power cannot increase when outcomes are
   removed. Therefore the smallest allowedc has greatest power among these
   deterministic upper-threshold rules, without claiming optimality over all tests.
5. Give categories probabilities.3,.2,.5. LetX=1 in category1,Y=1 in1or2.
   ThenX≤Y,P(X=1)=.3,P(Y=1)=.5. Independent copies preserve pathwise count
   order. For anyp≤p₀,use masses(p,p₀-p,1-p₀) to obtainP_p(K≥c)≤P_p₀(K≥c)≤α.
   This uses the iid Bernoulli sampling model, not a proof that real trials satisfy it.
6. A p-value integrates extreme outcomes under the null boundary given an
   observed statistic; size averages a rule atp₀; power averages it atp₁.
   A posterior instead conditions parameter probability on data using a prior.
   Low power permits frequent nonrejection even when a meaningful alternative is true.
7. Power=(7/10)⁵=16807/100000=.16807,miss probability.83193,effect size.2.
   A differentp₁ changes the distribution averaged under the same decision rule.
8. Power=(7/10)⁶=.117649<.16807 because the new critical count becomes6.
   Binary search on an unproved monotone-in-n predicate can skip a smaller
   feasible size; ascending search explicitly checks minimality under the bound.
9. For eachn derive its threshold underp₀/α,then power underp₁,stopping at the
   first≥target. Retain(n,c,size,power) for every checkedn. Atmax_n4 no feasible
   rule here means only none among1..4, not no feasible larger size.
10. Exact tails atn37 givec24,size.04943587479647249,power.8070956916527875
    atp₁=.7. Earlier evaluated sizes all have power<.8. The saved rational
    numerators/denominators support exact comparisons; rounded decimals alone
    are not minimality proof. This establishes the bounded model design, not
    actual independence, fault costs or a validated physical deployment.
11. Atp₀=0 all null mass isK=0; choosingc1 has exact size0 and can detect
    any observed1. Atp₀=1 all mass isK=n,soα0 requiresc=n+1. These reveal
    endpoint and empty-rejection handling without asymptotic approximations.
12. A data-dependent direction rejects in more cases than a fixed upper-tail
    procedure. Picking the best metric, subset or checkpoint after inspecting
    outputs similarly changes the selection event; its error behavior must include
    that selection rather than reuse the single-analysis interpretation.
13. Five initial ones contribute1/32. Atlook8,new7-of8 paths have their one
    zero among positions1..5,contributing5/256. At6or7 a crossing requires an
    all-one prefix already crossed at5. At9or10 the higher boundary's paths
    already crossed at5or8. Total13/256=.05078125. Equivalently at8 use
    P(first5ones)+P(K8≥7)-P(both)=1/32+9/256-1/64.
14. Ten initial ones reject at5,6,7,8,9,10. Adding fixed tails counts that
    path repeatedly. Those events share prefix bits, so a product formula based
    on independent looks has no justification. First-crossing categories are disjoint.
15. Bₜ(k)=(1-p)Aₜ₋₁(k)+pAₜ₋₁(k-1);hₜ=Σk≥cₜBₜ(k);keepAₜ(k)=Bₜ(k)
    fork<cₜ. Each old mass splits into exhaustive0/1 cases, then into disjoint
    hit/survive. ThusΣj≤thⱼ+ΣkAₜ(k)=1 by induction. Removing hits makes them
    unavailable for later double counting.
16. Loop over2⁸ labeled bit strings,compute masspᵏ(1-p)⁸⁻ᵏ,scan prefixes until
    the first crossing,then accumulate that category or survival. This differs
    structurally from merging active count states. Exponential path counts need
    a small cap; the test oracle rejectsn>12.
17. Each predeclared look has null chance≤α/N;P(union)≤ΣP(look)≤α regardless
    of dependence between look events. Coupling bounds each probability also
    forp≤p₀. The union bound can be loose because events overlap and count
    thresholds may spend much less than their assigned amount.
18. AtN100: final-only.0443130400570,repeatedα.202058097868,spending.00354001788693.
    Modelp₀=.5,overall budget.05 and horizon remain fixed; only testing schedule
    and thresholds change. Spending's conservatism is not proof of wrong arithmetic;
    it trades detection probability/thresholds for the stated error bound.
19. Extending after inspection adds rejection events not covered by the original
    allocation. The originalN-look sum bound does not automatically certify new
    looks. A valid predeclared extensible scheme needs its own summable allocation
    or sequential proof; none is silently added by this API.
20. At mostN(N+1) bit transitions,O(N) active count states and recorded totals;
    boundaries/planning inspect quadratically many binomial terms. Rational
    numerators/denominators grow withN,so arithmetic cost is not constant per
    operation. Input bit caps bound otherwise enormous exact-arithmetic requests;
    they do not sandbox arbitrary object construction before validation.
21. P(K≥1)=1-P(K=0)=31/32,despite the manually claimedsize0. Range validation
    prevents invalid indexing; calibration is established only by the factory's
    exact tail derivation or independent recomputation, not by record membership.
22. UseFraction(1,20). Fraction(.05) preserves the rounded binary float and
    need not equal1/20. For a boundary test chooseα equal to an exact tail and
    verify inclusion by≤; also test a rational amount immediately below it,
    which must require a stricter count if the tail mass is positive.
23. A good protocol fixes trial generator/version,reset policy,fault definition,
    inclusion of crashes,direction,p₀,p₁,α,power target and stopping rule. Measure
    correlated runs or missing logs independently. Randomized assignment and
    control of alternative explanations are separate causal-design evidence;
    exact binomial arithmetic does not supply them.
24. Acceptance requires fresh code,an exact worked count table,a separate
    complete-path oracle,actual JSON provenance and a deliberately wrong overlap
    calculation with a path witnessing its error. A passed finite test suite
    cannot prove real iid sampling,causality,global correctness for all inputs
    or the validity of a post hoc analysis choice.
