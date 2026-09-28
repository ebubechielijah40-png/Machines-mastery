# Reference answers

1: clk/reset/enable/d are inputs, q is state/output. 2: 7. 3: 4 after the next rising edge if reset is low. 4: zero after edge. 5: rising clk in this model. 6: the lesson shows a worked trace; derive a different one. 7: assert reset between edges and observe whether q changes before the next edge. 8: 16*16*2*2. 9: nonblocking assignments to both registers sample old values; reset must take priority. 10: reset=1,enable=1,d=1 distinguishes the provided mutant. The [RTL](register.sv) and [broken RTL](broken_priority.sv) are separate. No learner execution is implied.
