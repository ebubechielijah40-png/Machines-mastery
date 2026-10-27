# Abandon a stream and observe whether it joins

Question: does stopping output consumption leave a feeder or worker blocked?
Prediction: with cancellation selectable at every blocking communication, requesting
cancellation then awaiting Done permits all stages to finish in this finite build.
Controls: at most8192 bounded inputs, fixed worker counts, no external I/O. Tests
also separate sequential slice aliasing from actual concurrent race detection.
Procedure: run run.py and retain its exact outputs. The actual Go1.27.3 run passed9
normal and9 race-detector tests plus go vet. The observation printed ordered
[9,4,25] and reported all stages joined after output was abandoned following the
first result. Thirty bounded abandonment trials ran. They do not prove universal
scheduler fairness or shutdown latency; a future blocking network call would need
its own cancellation contract. Follow-up: intentionally remove each cancellation
branch and retain the intended bounded failure in a separate controlled process.
