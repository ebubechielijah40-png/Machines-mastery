# Progressive workbench hints

**A0:** Parse before aligning; use raw bytes for identity, normalized strings for computation. Distinct headers are a CLI contract, not a FASTA universal law.

**A1:** A prefix of length zero is still a valid subproblem. Every global boundary symbol must pay one gap cost.

**A2:** Record one direction code per cell. During traceback each direction must both emit a column and decrease the corresponding consumed-prefix index. Reverse the collected columns at the end.

**A3:** A local restart adds a fourth choice, zero. The maximum may occur anywhere. The indices where backward traversal stops are the returned start coordinates.

**A4:** Bound byte input before parsing and table size before allocating. Keep pure alignment separate from filesystem/CLI errors. Hash the exact bytes you read, not a reopened file that might have changed.

**B:** A test copying your recurrence can repeat your bug. Exhaustively enumerate all short column paths using the score definition instead.

**C:** Compare direct score -2 with gapped score 6+2g for `ACGT`/`AGCT`. Equal optima expose tie policy.

**D:** Two rows contain enough predecessors for the next score, but not the entire path back from the final cell. Space savings change what can be returned without another algorithm.
