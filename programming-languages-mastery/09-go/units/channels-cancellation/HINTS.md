# Hints

Track array identity separately from each slice window. Attach the index to the
job rather than assuming completion order. Closing is an ownership decision.
Every unbuffered send can block even if the arithmetic always terminates.
Done should signal a join, not merely that cancellation was requested. A timeout
is a failing bound, not the successful synchronization mechanism.
