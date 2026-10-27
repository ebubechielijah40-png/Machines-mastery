# Hints

1–4. Decide pop_fire from the old queue first. A full queue can accept a push only
when a real old word is consumed. An empty queue does not pass the new word through.
5–8. Pointer range and binary storage width are different. Reset changes logical
membership; erased physical storage is another property. Combine count changes
before assigning a signal. VHDL variables can express local intermediate decisions.
9–12. Check the old head at the active edge before scheduled memory updates.
A changed RAM latency changes the interface contract. Keep the independent deque
model distinct from the implementation's ring-pointer arithmetic.
