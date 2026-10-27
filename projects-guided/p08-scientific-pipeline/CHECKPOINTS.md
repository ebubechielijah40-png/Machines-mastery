# Scientific checkpoints

Use A0–A6 in the [build guide](README.md). Acceptance requires exact arithmetic and interpretation together.

1. Hand result: corrected mean24990 milli-Celsius and combined variance79/3 milli-Celsius squared for the supplied example.
2. Parser: exact unit/header, contiguous order, at least two samples and a final newline; reject floats and oversized input.
3. Statistics: independent pairwise-difference identity agrees with centered sample variance.
4. Correction: shifting calibration changes mean, while zero scatter does not remove a nonzero calibration uncertainty.
5. Reproduction: input/config/source identity is recorded and repeated execution agrees; content identity is not authentication.
6. Investigation: shared calibration variance approaches25 as n grows, while independently redrawn calibration variance shrinks as29/n.
7. Reconstruction: explain why neither copied rows nor sequence numbers establish independent observations over time.
