# Progressive alignment hints

1–2. A gap consumes a symbol on only one side. The empty-prefix row must pay for every symbol on the other side.

3. Read the final column, then erase it. Which prefix remains? A two-gap column makes no progress.

4. Identical A symbols make the match location ambiguous. Trace from the last cell with diagonal priority.

5. Global must consume all symbols. Local is allowed to choose the empty interval.

6. First label prefixes, then compute diagonals/up/left separately. Store the selected predecessor, not just a number.

7. Python slices exclude their right endpoint. The shared motif starts after two symbols and contains four.

8. Compute 2g and compare with q. The algorithm's admissible objects were defined before optimization.

9. Check reversal, coordinates, and the mapping from direction to emitted column separately. Rescore without reading the DP table.

10. A path ending inside a gap needs only an extension cost; a path ending with a paired column must pay an opening cost.

11. Before overwriting a cell, save the old diagonal. Only score is requested; a traceback needs information that is being discarded.

12. Keep strings, match, and mismatch fixed while changing gap. A conditional permutation test fixes composition, not evolutionary history.

13. Start by asking whether all input must be consumed. The same recurrence cannot decide this requirement for you.
