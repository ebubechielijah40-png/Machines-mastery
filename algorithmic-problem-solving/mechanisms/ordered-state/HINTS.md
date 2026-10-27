# Hints

1–4: Hashes choose candidate buckets; equality chooses records. The new capacity
changes the modulus. Sum powers of two for relocation, and0+1+…+(n−1) for
constant-hash insertion comparisons. Keys and hash callbacks must be stable.

5–8: Compare(priority,serial), never payload. After a root replacement only its
path can violate order. Most nodes in a complete tree are near leaves, where
repair is short. A sibling subtree can contain an arbitrary range of priorities.

9–12: Size counts the node itself. Moving right skips the entire left subtree
and current node. A two-child successor has no left child but can have a right
one. Recompute metadata upward from its old location. A sorted insertion path
has one more node each time; replacing recursion changes stack use, not height.
