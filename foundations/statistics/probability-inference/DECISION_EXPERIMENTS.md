# Exact decision experiments: executed observations

The current [raw integrated run](evidence/decision-observed-integrated-2026-10-25.json)
contains actual UTC time,Python/platform,all exact fraction numerators/denominators,
decimal displays,operating curves,each inspected sample size,first-crossing and
survivor masses,and five executable source hashes. The
[full unit test log](evidence/decision-tests-integrated-2026-10-25.txt) records
**27 tests PASS**,including14 new decision tests and13 probability tests
(12 preserved cases plus the new extreme-target coverage regression).
The earlier [initial decision run](evidence/decision-observed-2026-10-25.json)
retains its original hashes rather than being relabeled as the revised code.
The original2026-10-23 evidence also remains untouched.

These observations are executed **exact calculations on a synthetic iid
Bernoulli model**. They are not sampled factory observations,Monte Carlo
confidence estimates or physical validation. No random seed is needed because
no sampling RNG is used. Decimal displays are summaries; exact fraction fields
are authoritative,including for a probability too small for a floating display.

## Operating curve under a declared effect

Question: for an upper-count test calibrated atp₀=.5,α=.05,how does detection
change with the truep? Hypothesis: rejection probability increases withp for
the same fixed threshold,but can have jumps when changingn changes the threshold.
Hold the iid model family,null,direction,budget and tail convention fixed;
vary sample size and actualp. Instrument critical count,actual null size and
exact rejection probability. The null-size calculation is separate from
alternative power; the composite-null coupling proof is in the lesson.

| n | Critical count | Actual size atp=.5 | Power atp=.6 | Power atp=.7 | Power atp=.8 |
| --- | --- | --- | --- | --- | --- |
| 5 | 5 | .0312500 | .0777600 | .1680700 | .3276800 |
| 6 | 6 | .0156250 | .0466560 | .1176490 | .2621440 |
| 10 | 9 | .0107422 | .0463574 | .1493083 | .3758096 |
| 20 | 15 | .0206947 | .1255990 | .4163708 | .8042078 |
| 40 | 26 | .0403452 | .3174252 | .8074482 | .9920841 |
| 80 | 48 | .0464559 | .5483666 | .9788607 | .9999885 |

All reported null sizes respect the declared bound. The5→6 power drop confirms
that monotonicity in the truep does not imply monotonicity at every integern.
This refutes binary search based on that latter assumption. It does not refute
the general value of collecting more information or demonstrate a practical
loss optimum. Follow-ups can compare other declared directions or a randomized
boundary,with new calibration arguments and unchanged source/model provenance.

## Bounded minimum-n planning

Question: what is the smallest inspectedn providing at least.8 power at a
specifiedp₁? Holdp₀=.5,α=.05,one-sided threshold family andmax_n200 fixed;
vary only the declared alternative. Search every integern upward and retain
every failed earlier operating point. Prediction: a smaller deviation from the
null generally requires more information in this family.

| Alternativep₁ | Effectp₁-p₀ | Minimum inspectedn | Critical count | Actual size | Power |
| --- | --- | --- | --- | --- | --- |
| .6 | .1 | 158 | 90 | .0472373 | .8056549 |
| .7 | .2 | 37 | 24 | .0494359 | .8070957 |
| .8 | .3 | 18 | 13 | .0481262 | .8670837 |

The raw report retains all earlier failures,so these are minimal in1..selectedn
under the implemented rule. A search capped at4 finds no solution forp₁=.7;
that is a bounded no-hit outcome,not evidence that no larger design works.
Alternative explanations such as a monotone-search skip are excluded by the
ascending search and independent tail/path tests. These sample sizes are
conditional mathematical designs,not recommendations for a real fault process.
Unknown dependence,missingness,process drift or the wrong target effect can
make the real design inadequate. Follow-ups should vary one of those model
assumptions explicitly instead of silently retaining the old power interpretation.

## Fixed looks versus optional stopping

Question: does applying a nominal5% test repeatedly make an overall5% procedure?
Holdp₀=actualp=.5,α=.05 and a fixed horizonN constant. Compare only three
predeclared policies: final-only,repeatα at every prefix,and spendα/N per look.
Hypothesis: repeated selection inflates the union probability; spending respects
the budget but can be conservative. Instrument first-hit masses,survival and
transition counts; require exact first-hit+survival=1 at every look.

| HorizonN | Final-only false rejection | Repeatedα ever rejects | α/N spending ever rejects |
| --- | --- | --- | --- |
| 10 | .0107421875 | .0507812500 | .0039062500 |
| 20 | .0206947327 | .0986785889 | .0051002502 |
| 50 | .0324543235 | .1578822453 | .0043344741 |
| 100 | .0443130401 | .2020580979 | .0035400179 |

AtN10,the hand-derived13/256 repeated-look probability agrees with the DP.
AtN100,more than20% of null paths ever reject under repeatedα,while each
fixed-look test separately has size≤5%. Spending's below-budget result is
compatible with its conservative union-bound proof. Actual transition counts
forN100 are10100(final),6234(repeat),7268(spend),bounded byN(N+1)=10100.
Removing rejected paths explains why the latter count-state computations visit
fewer active transitions. All reported conservation totals are exactly1.

Independently enumerated complete binary paths at small horizons agree with
the DP's entire first-hit vector and survivor mass. This check uses a different
representation and also tests degeneratep=0/1. It reduces the alternative
explanation of a mass-merging/double-counting bug; it does not prove correct
behavior for every possible rational input. The causal or practical validity of
a real data collection process is not measured by this synthetic contrast.
Valid sequential methods can use other predeclared proofs; they are not
disproved by this example. Extending the horizon or choosing an analysis after
seeing outcomes needs a new error-accounting argument.

## Reproduction and historical output protection

```bash
python3 -m unittest discover -s foundations/statistics/probability-inference -v
python3 foundations/statistics/probability-inference/decision_experiment.py --output /tmp/decision-new-run.json
```

The output path must be new; the program refuses to overwrite an existing
record. Omit--output to print a fresh record to stdout. Compare exact numerator/
denominator fields and policy definitions,not timestamps or code hashes after
changes. The code uses Python3.10+ standard library with no account,download,
external dataset or instrument requirement. Exact arithmetic has growing bit
costs; bounded state transitions are not a hard runtime guarantee.
