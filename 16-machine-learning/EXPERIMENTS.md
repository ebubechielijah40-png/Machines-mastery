# ML experiments

1. Fit a linear model to exact data, then add noise and inspect parameter uncertainty qualitatively.
2. Vary learning rate from too small to unstable; plot loss vs step.
3. Train on a narrow x-range and test far outside it to expose extrapolation.
4. Create a leakage feature derived from the label and watch validation appear excellent; then remove it.
5. Create class imbalance and compare accuracy with precision/recall and confusion matrix.
6. Batch inference multiple examples and measure latency/throughput tradeoff.
7. Save model/version/data hash and reproduce a run.
8. Simulate distribution shift and set a monitoring threshold; explain false-positive/false-negative tradeoffs.
