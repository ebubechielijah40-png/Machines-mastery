# Design

The invariant is one stored payload per event identity. INSERT occurs inside a transaction; an injected exception before commit rolls back. Conflicting payload reuse is an error, not a duplicate success. The cache stores account totals and invalidates an account after a successful local write. Inputs are synthetic bounded integers; totals are queried with parameters. The contract assumes one writer through the same Ledger instance whenever caching is enabled. Multiple writers, cross-process idempotency races and distributed consistency need a different reviewed design.
