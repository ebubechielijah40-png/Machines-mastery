# Hints

1. Copy adds an allocation; move changes its owner without adding one. Destructors
   of empty moved sources have nothing to release.
2. Two owners of the same pointer cannot independently satisfy exactly-once release.
3. The parameter is constructed before swap. Follow all three fields, including ID.
4. A reference does not extend the lifetime of this heap allocation. Replacement
   and bounds checks concern different obligations.
5. Trigger failure before committing any target mutation. Use a controlled exception,
   not unreliable assumptions about exhausting real machine memory.
6. The member owner already supplies destruction and copy/move behavior. Avoid a
   second manually managed pointer shadowing it.
7. A resource wrapper's empty and failure states are part of its contract. File
   handles need a deliberate copy/duplicate policy rather than array copying.
