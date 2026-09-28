# Attempt before solution

Easy 1: compute [0,1]. Easy 2: compute [1,0]. Easy 3: name the two valid indices. Easy 4: explain each parameter. Easy 5: predict n=1 with output initially 99.

Intermediate 6: prove the largest result fits. Intermediate 7: give three independent defects in a cast-based implementation. Intermediate 8: design sentinel tests for failure paths.

Hard 9: derive a four-octet version with an explicitly chosen result type and overflow preconditions; explain why blindly multiplying in unsigned int may fail on some targets.

Experimental 10: predict whether -O0 and -O2 must produce identical instruction text versus identical valid-input results; compile, inspect and record both. Then implement this unit's two-octet function independently, run tests, and alter one byte-order assumption to verify a test detects it.
