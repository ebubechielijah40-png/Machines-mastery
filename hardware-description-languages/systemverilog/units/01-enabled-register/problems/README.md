# Attempt before RTL reveal

Easy 1: list input and state. Easy 2: predict hold from q=7. Easy 3: predict enable with d=4. Easy 4: predict simultaneous reset and enable. Easy 5: identify which event changes q.

Intermediate 6: hand-draw a load/hold/reset waveform. Intermediate 7: distinguish synchronous from asynchronous reset with one observation. Intermediate 8: derive the 1024 transition count.

Hard 9: design a two-register swap with enable and reset and explain old/new-value semantics without using sequential-software intuition.

Experimental 10: write a table-based testbench before opening the reference. Inject the priority bug, predict a failing input, simulate and preserve the failure. Add a width parameter as a modification only after the fixed-width version is understood.
