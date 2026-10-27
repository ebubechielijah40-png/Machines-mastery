# Historical model-serving execution evidence

The retained [raw benchmark](../../../research/model-serving-benchmark.json)
contains the actual finite serial-chunk and synthetic drift observations. The
original five-test suite covers model accuracy on synthetic data, selected schema
rejections, serial batch predictions, a chosen shift and single-thread rate
limiting. Passing those contracts does not establish dynamic batching, security
against all malformed inputs, concurrent limiter safety or public reliability.

The October25 reader identified the mismatch between these actual mechanisms
and earlier dynamic-batching/constant-memory claims. Corrected teaching now
states the serial/helper, accumulated-success-sample and unbounded-retention
boundaries. Historical raw numbers are preserved; no broader test is invented.
