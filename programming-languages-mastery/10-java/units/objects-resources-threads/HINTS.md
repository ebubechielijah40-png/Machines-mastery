# Hints

Track object identity separately from reference variables. Try mutating both the
original input and the returned snapshot. Exception flow retains a primary failure
plus suppressed cleanup failures. For concurrency, write separate read and write
events and mark the barrier before reasoning about a lock or atomic replacement.
The compiler module and runtime are distinct capabilities; inspect actual outputs.
