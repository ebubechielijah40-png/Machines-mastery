# Fragmentation and representation experiment

Question: can an arena reject a contiguous request while half its bytes are
free? Hypothesis: freeing alternating 8-byte allocations leaves only 8-byte
holes, so a 16-byte request fails despite 128 total free bytes.

Control capacity (256), quantum (8), allocation order, compiler flags, and the
release pattern. Compile `code/experiment.c` through `code/experiment.py`.
Instrumentation walks metadata to record every interval, free total, and largest
hole; it also records actual structure sizes. This is an observation of the
implemented allocator state, not a hardware memory profiler.

Procedure:

1. Initialize and capture one free block.
2. Allocate 7 and 9 and capture the split layout; release both.
3. Allocate thirty-two 8-byte regions; release even indices.
4. Capture free total/largest hole and attempt 16.
5. Release odd indices and capture complete coalescing.

Run from the repository root:

```bash
python projects-guided/p04-memory-allocator/code/experiment.py
```

The actual compiler invocation and stdout are in
[evidence/observed.json](evidence/observed.json). The recorded result has
free total 128, largest hole 8 and a failed 16-byte request, followed by a single
free 256-byte interval. The 7/9-byte layout consumes 24 reserved bytes for 16
requested bytes: 8 bytes of internal fragmentation. Host `sizeof` values vary
with ABI and are observations, not fixed constants.

Alternative explanations: an implementation bug or metadata exhaustion could
also cause failure. The snapshot shows the expected partition, and the current
geometry admits at most 32 blocks while 64 metadata entries are available.
The later successful coalescing check further narrows the explanation, but it
does not prove behavior for every possible request trace.

Follow-up experiments: vary request sizes while holding lifetimes fixed;
compare first fit with best fit on the **same recorded trace**; then vary
lifetimes independently. Measure failed requests, peak live requested/reserved
bytes, largest hole, scan length and metadata movement. A policy comparison
without identical workloads confounds allocator choice with workload choice.
Do not report throughput or cache effects from these state snapshots.
