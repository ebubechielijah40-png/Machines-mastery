# 06 — Convolutional neural networks

CNNs encode a structural assumption: nearby spatial patterns matter and the same detector can be useful at many locations. A convolutional kernel is a small learned filter reused across positions.

A 2D convolution slides a kernel over an image or feature map and computes local weighted sums. **Weight sharing** drastically reduces parameters relative to a fully connected layer and creates translation-related inductive bias.

## Receptive field

Stacking local operations increases the region of input that can influence a later activation. Receptive-field size depends on kernel size, stride, dilation, and depth.

## Experiment

Implement a 2D cross-correlation on a tiny matrix by hand and in Python. Apply an edge-like kernel. Then shift the input pattern and observe how the feature response shifts. Change padding and stride and predict output dimensions before running.

## Limits

CNNs do not automatically understand objects, causality, or 3D geometry. Translation equivariance is approximate in practical networks with boundaries, stride, pooling, and data preprocessing.
