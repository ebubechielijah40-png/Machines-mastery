# Exercises before looking at code

1. Distinguish a locus, allele, DNA base, diploid individual and gene copy. For
   N10 ideal diploid individuals and allele count5, compute m and p.
2. Derive the binomial row from ordered draws. Enumerate the m4,i2 row by hand.
3. Derive conditional mean and variance of next frequency from Bernoulli sums.
4. Compute next expected H for m4,p.5. Explain how mean can remain.5 while H falls.
5. Derive multi-generation frequency variance from the H recurrence. Compare
   m10 vs40 at t10 starting.5 without interpreting the mean as a typical path.
6. Prove eventual neutral fixation probability p0. Give its immediate one-step
   counterpart and explain which source notation must be handled carefully.
7. Derive q for relative copy fitness1+s. At p.25,s1, compute q; explain why a
   diploid dominance model needs a different derivation.
8. Calculate likelihood for m4,count path2→3→1 under neutral sampling. Then add
   a transition0→1 and explain its likelihood without adding arbitrary epsilon.
9. Why does a neutral trajectory favoring negative s on a finite likelihood grid
   fail to establish selection? Specify one observation-model improvement.
10. Derive JC69 distance and its sensitivity to mismatch fraction. Calculate d
    for f.25; explain rejection at f.75 and why units are not years.
11. Trace UPGMA for AB2,CD4,all cross6 and verify every reconstructed distance.
12. Derive cluster-size weighting. If |A|2,|B|1,d_AC4,d_BC10, compute merged distance.
13. Reconstruct the nonclock additive counterexample's six distances and UPGMA
    merges. Which biological premise, rather than arithmetic, fails?
14. Rebuild exact propagation, a Bernoulli simulator and tree construction from
    memory. Add a declared mutation mechanism and new independent endpoint tests.
