# Learning representations by back-propagating errors (1986)

**Classification: SCAFFOLDED.** Source identity verified at [the primary source](https://www.cs.toronto.edu/~hinton/absps/naturebp.pdf); full technical/results reconstruction is **UNVERIFIED — verification required**. The preserved prompts below do not establish a completed reconstruction. See [verification records](SOURCE_VERIFICATION.json).

## Problem that created the work
How can multilayer networks assign credit to internal weights efficiently?

## Core idea
Use the chain rule backward through composed differentiable operations so each parameter receives its contribution to output error.

## How to reconstruct the mechanism
Do not begin with the paper's conclusion. Write the baseline system, identify its bottleneck, implement the smallest version of the proposed mechanism, and measure the quantity the method claims to improve. Separate architecture change, data change, compute change, and evaluation change.

## Evidence and interpretation
The paper demonstrated learning useful hidden representations on small tasks; the lasting contribution is the efficient credit-assignment procedure, not modern scale.

## Questions to answer
1. What exact baseline is being improved?
2. Which assumption is most important?
3. What measurement would falsify the central claim?
4. Which result is architecture-specific versus likely transferable?
5. What production constraint appears only at larger scale?

## Reproduction task
Create a toy reproduction capturing the central mechanism rather than attempting the original scale. Record deviations from the original setup and never claim numerical reproduction without matching data/compute/configuration.
