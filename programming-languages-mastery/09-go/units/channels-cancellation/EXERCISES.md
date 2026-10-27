# Exercises

1. Trace slice length/capacity/backing storage through the two append probes.
2. Explain why a channel send of a slice does not establish deep ownership.
3. Prove the input bound makes squaring safe for int64.
4. Trace[3,-2,5] with worker completion order2,0,1; rebuild ordered output.
5. Identify every channel's senders, receiver and sole closer.
6. Remove each send's cancellation branch in turn; design a bounded failing test.
7. Explain why putting cancellation first in select does not prioritize it.
8. State what a streaming consumer must do when it abandons partial output.
9. Distinguish a channel synchronization guarantee from an observed race-free run.
10. Rebuild the bounded stream and test cancellation after one result without
    using a sleep as the sole reason to believe all workers exited.
