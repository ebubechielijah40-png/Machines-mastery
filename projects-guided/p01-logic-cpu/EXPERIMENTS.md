# Branch-target fault experiment

Question: can a valid opcode with a wrong address break termination while leaving
arithmetic correct? Hypothesis: replace JMP2 at address9 with JMP9, and the PC
will stay9 after the first loop pass. Hold ISA, memory except that byte, a=3,
b=4 and the100-cycle budget fixed. Instrument PC, accumulator, memory and count.

Run `python3 01-computation/toy-cpu/experiment.py` from the root. Actual raw output
is in [cpu-experiment.json](../../01-computation/toy-cpu/evidence/cpu-experiment.json).
The baseline halts with12 in35cycles. The altered machine exhausts100cycles at
PC9. The source records every baseline transition, the exact changed word and
retained fault state. These are software-model observations, not physical timings.

Interpretation: a decoded instruction can have valid syntax but wrong semantics.
A budget alone cannot prove nontermination; here repeated identical PC9 and JMP9
explain the bounded observation. An alternate insufficient-budget explanation is
weakened by the baseline35-cycle trace and direct inspection of the altered loop.

Follow-up: change the target to0. Predict accumulator3 after41cycles, then test.
It restarts product initialization while the counter continues decreasing. This
fault terminates but returns the wrong answer. Compare test strategies that check
only halt, only final result, or every transition. Next vary b across1,2,15,255
and test the8b+3 cycle relation; choose a budget large enough for your prediction.
