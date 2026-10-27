# FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness (2022)

**Classification: SCAFFOLDED.** Source identity verified at [the primary source](https://arxiv.org/abs/2205.14135v2); full technical/results reconstruction is **UNVERIFIED — verification required**. The preserved prompts below do not establish a completed reconstruction. See [verification records](SOURCE_VERIFICATION.json).

## Problem that created the work
Why is standard attention slow/memory-heavy even when arithmetic count is understood?

## Core idea
Reorder/tile exact attention computation to reduce expensive memory traffic between accelerator memory levels while preserving mathematical result.

## How to reconstruct the mechanism
Do not begin with the paper's conclusion. Write the baseline system, identify its bottleneck, implement the smallest version of the proposed mechanism, and measure the quantity the method claims to improve. Separate architecture change, data change, compute change, and evaluation change.

## Evidence and interpretation
Demonstrated that hardware-aware algorithm design can dramatically improve attention speed and memory use without approximate attention.

## Questions to answer
1. What exact baseline is being improved?
2. Which assumption is most important?
3. What measurement would falsify the central claim?
4. Which result is architecture-specific versus likely transferable?
5. What production constraint appears only at larger scale?

## Reproduction task
Create a toy reproduction capturing the central mechanism rather than attempting the original scale. Record deviations from the original setup and never claim numerical reproduction without matching data/compute/configuration.
