# Boundary exercises

1. Predict helper arguments for positional parameters `"a b"`, `""`, `"*"` under
   each form, first in an empty directory, then with one file named `x y`.
2. Write a Bash wrapper forwarding all arguments without joining them. Verify
   zero arguments, an empty argument, a newline and a literal wildcard.
3. Explain why a filename containing spaces produced by glob expansion remains
   one argument here, while a space inside an unquoted parameter split earlier.
4. Why can `"$value"` preserve a value yet still let a target command treat it as
   an option? State both relevant parsers and a target-specific remedy.
5. Construct a controlled failing producer/successful consumer pipeline. Predict
   status with and without pipefail, then retain actual statuses.
6. Reconstruct the lab from a blank file using only temporary local files. Extend
   it to an unusual IFS value and state exactly which predictions change. Do not
   execute arbitrary supplied shell source to test data forwarding.
