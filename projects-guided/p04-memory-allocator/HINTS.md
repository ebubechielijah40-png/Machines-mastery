# Hints after an attempt

A1: Carry an `end` offset while scanning. Require `block.offset == end`, then
advance by a positive bounded size. This checks order and coverage together.

A3: First find the chosen interval. If it has a remainder, shift from the end
before writing the new entry. The payload array never moves.

A4: A release can join a free neighbor on both sides. Recheck the same position
after merging and compacting. Comparing pointer equality to known starts avoids
subtracting an unrelated pointer to compute an index.

A5: Tests should retain their own list of live regions and expected payload
bytes. If the test derives expectations solely from allocator metadata, a
shared metadata bug may fool both implementation and oracle.

A6: Count total free space and largest contiguous hole separately. A request
needs the latter to meet its rounded size.

Transfer: Changing alignment requires more than editing a rounding expression.
Check arena base alignment, capacity divisibility, metadata bounds, overflow
preconditions and the declared storage-type contract.
