# Privacy engineering: from collection to bounded disclosure

Begin with the developed [count-release lesson](count-release/LESSON.md). It derives sensitivity, real-valued Laplace noise and additive privacy cost, implements the inspectable finite-float model and exact integer budget gate, and executes synthetic utility/repetition experiments. It explicitly distinguishes mathematical privacy from an uncertified finite implementation. Required mathematics, exercises, separate hints/solutions and inspected primary scopes are linked inside.

## A pseudonym does not define the disclosure threat

Use this entirely synthetic table: `(A, east, 09:00)`, `(B, east, 10:00)`, `(C, west, 09:00)`. Removing names leaves three rows, but an observer who already knows that a particular person was the only west participant at09:00 can still associate that row. A stable pseudonym also permits joining the same label across releases. This is a logical counterexample to the claim that removing direct names automatically prevents linkage; it is not a measured population reidentification rate.

Minimization asks whether the service needs exact time and region at all. If only a daily total is necessary, retaining detailed rows creates additional linkable state without serving that particular requirement. Retention/deletion design must include raw input, derived datasets, logs, caches and backups; deleting one visible table does not show that other copies vanished. This repository has no executed deletion/backup system for that scope yet.

## Define the protected change and the release

For the count unit, each row contributes zero or one and neighboring datasets differ by adding/removing one row. Sensitivity is one. That is person-level protection only with one bounded row per person; accepting unlimited rows silently changes the protected unit. A real operator must also decide who may query, which population shares a budget and how repeated/overlapping queries compose.

At ε=.5 the ideal sensitivity-one Laplace count has scale2, expected absolute noise2 and variance8. Repeating it100 times and averaging lowers variance to.08 but spends conservative total ε=50. The actual synthetic computation measures these quantities, while a known-seed counterexample shows how predictable noise can disclose the exact count. Utility alone cannot certify privacy.

## Connect integrity and privacy without conflating them

The [provenance pipeline](../security-cryptography-mastery/provenance/LESSON.md) can authenticate a record and reject unauthorized writes, but its stored records remain plaintext. Conversely, a private aggregate can be based on erroneous or fabricated data. A complete system must separately validate input meaning, enforce collection/access authority, retain appropriate evidence and analyze released information.

The in-memory `Budget` object charges microepsilon before noise generation and denies overspending. Restarting, using another object, or making queries through two accounts bypasses any intended shared persistent policy; population identity, transactions and crash recovery are absent. The floating sampler is not certified against all output events and finite-precision support issues. This unit makes those limitations explicit rather than labeling a noise function a privacy service.

Entry assessment: derive Δ=1 for bounded bits. Exit assessment: reconstruct the density-ratio proof, derive the repeated-release tradeoff, demonstrate known-seed failure and design the durable authority the accountant lacks. Domain status remains PARTIAL. Retention/deletion implementation, unlinkability studies, contribution enforcement, production mechanisms and shared privacy accounting need further work.
