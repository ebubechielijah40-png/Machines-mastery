# Hints after an attempt

1. Rejected attempts must not advance either sequence or count. The tip changes only for an accepted entry.
2. XOR each key byte independently with 0x36 and 0x5c. Hash a long key before zero padding.
3. Stream, units, transform version and identity affect meaning even when the numeric value stays fixed.
4. In Python, `isinstance(True,int)` and `True==1` both hold. The protocol uses `type(x) is int`.
5. A valid prefix is itself a valid history unless another authority supplies the expected end.
6. Errors communicate uncertainty about effects, not an assurance of no effects. Reopen from durable bytes before retrying.
7. A function argument can model an established principal only when callers cannot choose arbitrary identities.
8. Keep producer and processor authority separate. Read the reference only after drafting your state transitions.
9. Authentication concerns origin under key assumptions, not specimen selection, instrument calibration or interpretation.
