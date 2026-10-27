# Finite serial-inference benchmark

`benchmark.py` groups200 generated vectors into chunks of1,4,16,64 and calls the
serial helper. It records wall time, request counts and success-only inference
percentiles. The historical raw file is
[model-serving-benchmark.json](../../../research/model-serving-benchmark.json).
This is not dynamic dispatch, a queued network workload or a scalable serving
benchmark. It has no independent arrival schedule, repeat-trial uncertainty or
client waiting-time measurement.

A second synthetic case compares baseline features with deliberately shifted
features. Its PSI difference supports sensitivity to that chosen shift, not a
calibrated alarm, production drift attribution or an accuracy-loss guarantee.
Keep the raw observations and rerun with a new output filename; do not project
one host's observed rates into a production capacity claim.
