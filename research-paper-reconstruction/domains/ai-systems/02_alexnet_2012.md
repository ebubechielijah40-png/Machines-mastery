# ImageNet Classification with Deep Convolutional Neural Networks (2012)

**Classification: SCAFFOLDED.** Source identity verified at [the primary source](https://papers.nips.cc/paper_files/paper/2012/hash/c399862d3b9d6b76c8436e924a68c45b-Abstract.html); full technical/results reconstruction is **UNVERIFIED — verification required**. The preserved prompts below do not establish a completed reconstruction. See [verification records](SOURCE_VERIFICATION.json).

## Problem that created the work
Can deep CNNs trained with GPUs substantially improve large-scale image classification?

## Core idea
Combine deep convolutional representation learning, ReLU nonlinearities, regularization/data augmentation, and GPU computation.

## How to reconstruct the mechanism
Do not begin with the paper's conclusion. Write the baseline system, identify its bottleneck, implement the smallest version of the proposed mechanism, and measure the quantity the method claims to improve. Separate architecture change, data change, compute change, and evaluation change.

## Evidence and interpretation
Large improvement on ImageNet helped establish deep learning as a practical large-scale vision approach; hardware and data were part of the result.

## Questions to answer
1. What exact baseline is being improved?
2. Which assumption is most important?
3. What measurement would falsify the central claim?
4. Which result is architecture-specific versus likely transferable?
5. What production constraint appears only at larger scale?

## Reproduction task
Create a toy reproduction capturing the central mechanism rather than attempting the original scale. Record deviations from the original setup and never claim numerical reproduction without matching data/compute/configuration.
