# Twelve mechanism tasks

1. Trace buckets for a,e,ab at capacity4. Explain why equal hashes still need equality.
2. Insert/overwrite/delete a key storing None. Specify absence without a sentinel collision.
3. Derive a geometric bound on rehashed entries and a quadratic constant-hash comparison count.
4. Explain why doubling fails against a constant hash; propose a hostile-key policy.
5. Derive zero-based heap relatives and trace priorities5A,2B,2C through all pops.
6. Prove one-path heap repair and the linear bottom-up construction bound.
7. Build a stable heap for unorderable payload objects. Explain serial lifetime and overflow choices in a fixed-width port.
8. Explain why a heap cannot provide ordered range queries with its root alone.
9. Trace rank7 and select4 for the nine-key tree in the lesson.
10. Delete its root and repair every affected size. Construct a stale-size failure that lookup alone misses.
11. Derive sorted-insertion work, compare shuffled order, and explain why iteration does not balance a tree.
12. Reconstruct all three structures without dict/heapq/sorted inside them; test against those independent oracles and propose a balanced or durable extension.
