# Controlled graph experiments and actual evidence

## Question and prediction

Does BFS cost track vertices alone or the number of adjacency entries? A chain
with n vertices stores n−1 entries. A dense DAG with edges i→j whenever i<j
stores n(n−1)/2. Both are reachable from0, but scanning the latter requires
quadratically more entries. Prediction: increasing n raises work approximately
linearly on chains and quadratically on dense DAGs in an adjacency-list model.
Elapsed time need not follow a smooth exact ratio on small inputs.

## Procedure and instrumentation

Run `python3 algorithmic-problem-solving/topics/graphs/code/experiment_graphs.py`
from repository root. The script constructs deterministic synthetic graphs at
48,96,192,384 vertices, counts stored adjacency entries, runs five BFS trials per
case with `time.perf_counter`, and records all timings and median. Graph creation
is outside the timed call; the public BFS's validation/copy is inside it. Controls
are Python process, implementation, source0, machine and repeat count. Independent
variables are shape and vertex count; dependent variables are time and last
vertex distance. Environment and raw measurements are in [observed.json](evidence/observed.json).
No external dataset or privileged network is used.

## Executed observations

The retained run used Python3.12.14 on Linux x86-64. At n=48 the chain had47
entries and median0.000021293s; the dense DAG had1128 entries and median0.000116860s.
At n=384 the chain had383 entries and median0.000161616s; the dense DAG had73536
entries and median0.011660470s. The chain's last distance was n−1, whereas the
dense DAG's was1. Shortest distance is therefore not a measure of total traversal
work. All five trials, including variability, remain in the raw JSON.

This is evidence compatible with scanning adjacency entries. It does not estimate
an asymptotic exponent reliably or establish universal speed ratios: allocator
state, validation sets, cache locality, process scheduling and timer noise are
alternative contributors. There is no memory measurement in this experiment;
space complexity in LESSON is a derived model, not measured RSS.

## Semantic counterexamples executed by the same script

For0→1 cost7,0→2 cost2,2→1 cost1, Dijkstra returned `[0,3,2]`. A discovered vertex
must remain improvable; a stale heap entry must be ignored. For a reachable
negative cycle between1 and2 plus isolated3, Bellman–Ford returned
`[0,"-inf","-inf","+inf"]` in JSON notation. Those are distinct conditions.
The unlimited-worker dependency example returned finishes `[2,5,9,10]`.

## Next investigations and interpretation task

1. Before running, predict the effect of changing only adjacency order. Check
   distance invariance separately from timings and parent-route identity.
2. Instrument edge inspections and queue operations, then compare exact operation
   counts with elapsed time. Keep instrumentation overhead out of the claim.
3. Implement a matrix BFS and measure sparse/dense cases with a common contract.
4. Add realistic latency or capacity measurements with provenance; determine
   whether an optimal graph answer remains useful under uncertain/stale inputs.

Do not relabel a predicted outcome as executed. Save a new environment/measurement
record for any extension; the retained file is one actual local run.
