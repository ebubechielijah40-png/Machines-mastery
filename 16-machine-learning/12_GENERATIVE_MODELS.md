# 12 — Generative models

A generative model learns enough about a data distribution to produce new samples or assign likelihood/score structure.

## Autoregressive models

Factorize a joint distribution into conditional predictions. Strength: exact sequential likelihood factorization. Cost: generation is sequential.

## Variational autoencoders

VAEs introduce latent variables and optimize a lower bound balancing reconstruction with regularization toward a prior. They make latent structure explicit but can trade sharpness against probabilistic structure depending on domain/objective.

## GANs

A generator and discriminator play an adversarial game. GANs can produce sharp samples but training can be unstable and likelihood evaluation is indirect.

## Diffusion models

A forward process progressively corrupts data with noise; a learned reverse process denoises. Training commonly learns to predict noise/score-like quantities. Sampling iteratively reverses corruption, which can be computationally expensive but highly expressive.

## Comparative experiment

On a 2D toy distribution, implement or use minimal versions of an autoregressive density model and a denoising process. Compare what each objective actually teaches the model. Do not compare only sample aesthetics; inspect likelihood/coverage/mode behavior where meaningful.
