# Entry checks and bridges

Before writing the runner, complete the descriptor section of the
[OS guide](../../05-operating-systems/SELF_CONTAINED_GUIDE.md) and run its
[host observations](../../05-operating-systems/code/experiment.py). Explain why
`dup` shares an offset while a fresh `open` has its own offset. Explain why an
empty pipe with an open writer differs from an empty pipe with no writers.

For Python, use [the language guide](../../programming-languages-mastery/08-python/README.md)
as a reference, then implement these tiny bridges locally: append characters
to a list and join them; raise and catch ValueError; close a file in `finally`;
construct an immutable result object; launch a child with an argument list.
The runnable reference uses standard-library dataclasses, pathlib, subprocess,
tempfile, time, and math. No knowledge of a third-party process library is
assumed.

Your entry artifact is a hand trace of `prog '' 'x y'|next` and a table naming
who owns each stdin/stdout handle. If you cannot produce it, revisit sections
2–4 of [the project lesson](README.md) before looking at the reference code.
Python 3.12+ and locally authorized child programs are required. Windows pipe
and process semantics have not been validated by this unit.
