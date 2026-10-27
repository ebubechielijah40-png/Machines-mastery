# Source scope and original mechanism

Primary inspection2026-10-23: Leslie Lamport, “Time, Clocks, and the Ordering
of Events in a Distributed System,” *Communications of the ACM*21(7),558–565,
July1978, [author-hosted primary paper](https://lamport.azurewebsites.net/pubs/time-clocks.pdf).
Inspected the strict happened-before definition, clock condition and logical
implementation rules, printed pp559–560. Supports only the causal-order/clock
portion of this unit. The repository's [paper dossier](../../research-paper-reconstruction/domains/distributed-systems/01_lamport_clocks_1978.md)
has a separate broader inspection/reconstruction record.

The keywise maximum rule, immutable record API, Envelope distinction,
counterexamples, finite schedule experiment, code and exercises here are
original. Their convergence argument follows from the displayed maximum
identities under the stated valid-history premise. No consensus or published
CRDT benchmark is claimed as reproduced.

The INRIA report endpoint`https://hal.inria.fr/inria-00555588/document` returned
an access-denied page during this inspection. Its contents were not used as
verified evidence. This does not block the elementary original max proof, but
does block claiming that report was inspected or reconstructed here.
Primary-paper copyright remains with ACM; the linked paper is not bundled and
no substantial source prose, figures or code are reproduced.
