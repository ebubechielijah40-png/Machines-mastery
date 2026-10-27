# First independent attempts

1. Predict values/types of20,20.0,"20",True,None; distinguish `x=3` and `x==3`.
   Run a three-line file that increments a binding and prints the old/new values.
2. Hand-trace used after each addition of[4,0,7]. Repeat with an empty list. Write
   a while loop for three increments and identify its termination measure.
3. Build choose_prefix for valid data from the contract before opening budget.py.
   Trace[4,0,7] with capacity4, [0,0,1] with capacity0, and[6,1] with capacity5.
4. Add validation of the entire input. Why must[100,-1] with capacity0 still be
   rejected under the reference contract even though selection stops at100?
5. Return a new accepted list and demonstrate that appending to it leaves input
   unchanged. Then deliberately alias the input in a learner copy and record the
   failing behavior/test before repairing it.
6. Write a unittest for exact fit, first packet too large and invalid size. Explain
   the difference between a failed expected result and a module import error.
7. Change the requirement to at most3 packets as well as a byte budget. State a new
   invariant and add tests for zero-size packets and the packet limit. Do not claim
   the original implementation already enforces it.
8. Reconstruct function, validation, module guard and three tests from a blank file.
   Explain each state update and the distinction from maximum-sum subset selection.
