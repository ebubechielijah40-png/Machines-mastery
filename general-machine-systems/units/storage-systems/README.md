# Storage Systems — mechanism, failure, and reconstruction

## Why this machine exists
Storage systems preserve bits across time while exposing block/object/file abstractions.

## Energy and information path
Host requests → controller/protocol → cache/translation → physical medium → redundancy/error correction → durable representation.

## Mechanism
SSDs map logical blocks to flash pages through an FTL; disks use mechanical positioning; distributed storage adds replication/erasure coding and consensus/metadata.

When studying a real example, first draw the boundary and label energy input, useful output, losses, state, control, and interfaces. Then descend into the component that limits behavior instead of cataloguing parts.

## Failure modes
bit errors, wear, controller failure, power loss, latent corruption, rebuild overload

A failure is evidence about mechanism. Record symptom → competing hypotheses → measurement → result → revised model. Do not jump from symptom directly to replacement.

## Experiment
Benchmark sequential vs random access and small vs large requests on a safe local device/file; explain results via medium/cache.

Before measuring, predict the direction and approximate magnitude of the effect. Record units, uncertainty, and what the experiment cannot establish.

## Reconstruction challenge
Design a storage path for durable records and specify integrity, backup and recovery tests.

After studying, hide the reference and redraw the functional block diagram from memory. Your reconstruction passes only if another person could use it to predict behavior under a changed load or failure.
