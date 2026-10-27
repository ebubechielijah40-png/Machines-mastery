# Hints

1–4. Ownership follows the acquired buffers, not the byte values. Both defer
forms end at their declaring scope; their trigger conditions differ.

5–6. Allocate in order, register each acquired resource's cleanup before the
next fallible operation, and transfer responsibility only on successful return.

7–9. Separate descriptor mutability, element mutability and backing-storage
lifetime. The fixed allocator's free function checks whether the block is last;
a logical lifetime can end without its underlying bytes being immediately reused.

10–11. Close the reference. Draw who releases each buffer before writing syntax.
A borrowed parser cannot outlive or mutate against its backing input policy.
