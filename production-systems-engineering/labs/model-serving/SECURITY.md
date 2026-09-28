# Security: Robust ML Inputs and Abuse Prevention

## Threat Vectors
1. **Adversarial Poisoning / Malformed Inputs:** Crafting vectors containing extreme numeric magnitudes, NaNs, or Infinities to induce crashes, overflow, or undefined behavior.
2. **Denial of Service via High-Dimensionality:** Submitting vectors with millions of dimensions to exhaust server memory and CPU during vector multiplication.
3. **Model Extraction / Abuse:** Scraping model decision boundaries via rapid, automated query bursts.

## Mitigations
- **Strict Dimension Enforcement:** Inputs must strictly equal `expected_dim`; extra or fewer dimensions are rejected immediately.
- **Range Clamping & Type Checking:** Every element must be an instance of `(int, float)` and bounded within $[min\_val, max\_val]$.
- **Token Bucket Rate Limiting:** Enforces maximum request burst size and sustained refill rate per client.
