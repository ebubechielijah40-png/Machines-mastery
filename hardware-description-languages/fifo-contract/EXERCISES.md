# Queue construction exercises

1. Trace empty push+pop and full push+pop, naming old and new heads.
2. Prove occupancy bounds for all boundary/interior fire combinations.
3. Derive the acceptance equations from the stated full-replacement contract.
4. Trace DEPTH3 for push1,push2,push3,pop,push4,pop,pop,pop.
5. Explain why pointer bit truncation can address a nonexistent cell at depth3.
6. Explain why resetting pointers/count need not reset memory for queue correctness,
   and why that does not promise secure erasure.
7. Find the bug in two independent count<=count+1/count<=count-1 assignments.
8. Port the same contract to VHDL using variables for fire decisions. Explain the
   different effects of := and <= without calling one language “sequential.”
9. Add a consumed-word scoreboard and identify the exact sampling event.
10. Test DEPTH1 and DEPTH5 with an independently generated bench; retain actual
    results only after running them. What assumptions in the present bench need change?
11. Add a registered-read interface. Specify latency before editing implementation.
12. Reconstruct the queue from a blank file and supply a wrap trace, a boundary
    counterexample, both invariants and one intended mutant failure.
