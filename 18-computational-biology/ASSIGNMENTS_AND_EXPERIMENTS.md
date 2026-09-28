# Computational biology assignments and experiments

Use synthetic or public non-sensitive data. Record assumptions and raw outputs.

## Sequence fundamentals
1. Write a FASTA parser that handles multiline sequences and rejects invalid headers.
2. Compute GC fraction and explain why GC percentage alone does not identify an organism.
3. Produce reverse complements and verify `revcomp(revcomp(s)) == s` for canonical DNA.
4. Count k-mers for k=1..6 and examine how state-space size grows as `4^k`.
5. Simulate random DNA with different base probabilities and compare observed k-mer frequencies with expectation.

## Alignment
6. Implement global alignment with match/mismatch/gap scores.
7. Change gap penalty and observe how optimal alignments change.
8. Generate sequences with known mutations and test whether alignment recovers the intended correspondence.
9. Compare runtime as sequence length doubles; relate observation to `O(nm)` table size.
10. Add traceback and verify score consistency.

## Population/evolution
11. Simulate allele-frequency drift in populations of different sizes.
12. Repeat 1,000 simulations and visualize outcome distributions.
13. Add selection and distinguish stochastic variation from directional tendency.
14. Test Hardy–Weinberg expected genotype frequencies under random sampling.

## Systems biology
15. Simulate a one-variable expression/degradation ODE with Euler integration.
16. Halve the time step and compare numerical error/stability.
17. Add negative feedback and observe steady-state/time-response changes.
18. Fit a simple parameter from synthetic noisy measurements and discuss identifiability.

## Data reasoning
19. Construct a batch-effect toy dataset that looks separable for the wrong reason.
20. Split by batch vs random split and compare a classifier's apparent performance.
21. Write a provenance record for every transformation.

## Research reconstruction
22. Choose a public computational biology paper with accessible data/code. Reconstruct problem → measurement → method → result → claim. Reproduce one bounded figure/table where licensing and data permit. Record discrepancies instead of forcing agreement.
