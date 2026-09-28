# Reverse engineering unfamiliar systems — deep handbook

Reverse engineering is disciplined inference under incomplete information. The goal is not to guess a hidden implementation; it is to build the simplest model that explains observations, then design experiments that force competing models to make different predictions.

## 1. Choose the boundary

A “system” is whatever boundary you choose. For a web service the boundary might include client+server or only the API. For a motor it might include the controller or only the electromechanical device. Boundaries change which quantities are inputs, outputs, hidden state, and disturbances.

Write the boundary before testing. Otherwise you will silently move unexplained behavior outside the system.

## 2. Inventory observable interfaces

List every input/output channel you can observe safely: files, network messages, return values, LEDs, sound, current draw, motion, temperature, timing, logs, bus traffic, command-line arguments, error codes. For each interface, record units/encoding, timing, valid range, and uncertainty.

## 3. Search for state

Two identical inputs can produce different outputs only if the environment differs, randomness exists, or hidden state changed. Reset the system if possible, repeat identical trials, then vary history. State can live in memory, disk, caches, counters, mechanical position, charge, temperature, fluid pressure, or remote dependencies.

## 4. Build competing models

Do not settle on the first explanation. Example: a service slows after 1,000 requests. Possible models include memory growth, connection leakage, cache eviction, rate limiting, thermal throttling, or a remote quota. Each predicts different secondary observations.

## 5. Design discriminating experiments

A good experiment changes one relevant factor and yields different predictions under competing models. If both models predict the same output, the experiment does not discriminate them.

Use a table:

| hypothesis | intervention | predicted observation | actual observation | update |
|---|---|---|---|---|

## 6. Trace flows

For computational systems trace **control, data, and state**. For physical machines also trace **energy, forces, material flow, heat, and feedback**. For cyber-physical systems trace all of them together.

## 7. Instrument before optimizing

Use logs, counters, traces, profilers, packet capture on authorized local systems, debuggers, oscilloscopes/multimeters when trained and safe, sensors, or simulation. If you cannot observe a claimed mechanism, label it inference rather than observation.

## 8. Reproduce behavior

Build the smallest replica that matches a selected behavioral contract. A replica proves only that your mechanism can generate the observed behavior, not that the original uses the same internals. Add withheld tests to reduce overfitting.

## 9. Descend abstraction layers

When stuck, ask which lower layer could explain the observation. A Python slowdown may descend into object allocation, OS scheduling, page faults, cache misses, I/O, or hardware throttling. A robot instability may descend into sensor noise, latency, actuator saturation, mechanical backlash, or control gains.

## 10. Reconstruct from constraints

Instead of memorizing architecture, derive it. If a CPU must retain state across cycles, it needs storage. If instructions address memory, an address representation and path must exist. If a network can duplicate messages, a once-only business action needs an idempotency strategy or stronger protocol. Constraints often force architecture families.

## 11. Failure is information

Intentionally test boundaries: empty input, maximum input, invalid input, lost dependency, latency, reduced memory, restart, stale cache, dropped message, sensor saturation. Failures reveal hidden assumptions faster than happy-path observation.

## 12. Know what cannot be inferred

Black-box observations may be compatible with multiple internal implementations. Cryptographic protection, compression, proprietary hardware, or inaccessible timing can make exact reconstruction impractical. Report the equivalence class of surviving explanations rather than inventing certainty.

## 13. Reconstruction drill

After studying a system, close the reference and draw: components, interfaces, state, data/control/energy flows, invariants, failure modes, and one minimal implementation. Compare against the reference, classify each error as memory failure, conceptual gap, or unjustified assumption, then repeat a week later.
