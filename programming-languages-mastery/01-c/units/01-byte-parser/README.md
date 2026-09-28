# C exemplar: turn two supplied octets into a value

PREPARED; learner NOT STARTED. Begin with [the prerequisite bridge](PREREQUISITE_BRIDGE.md), then [the lesson](LESSON.md), [problems](problems/README.md), hints/retry, experiment, your implementation, tests and mastery. Solutions are separate. Normal study needs no external tutorial.

This unit specifies an original two-octet high-first format; it is not attributed to a network protocol or book. It connects representation, C object access, length checks and compiler output. We do not teach a complete C language in one unit.

## Local commands

Requirements: Python 3.10+, C11 compiler `cc`, GNU objdump/readelf for optional inspection. No package dependencies. From the repository root:

```sh
python3 programming-languages-mastery/01-c/units/01-byte-parser/tests/run.py
```

The runner compiles at -O0 and -O2 with warnings as errors, executes exhaustive two-octet cases and error tests, and runs an undefined-behavior sanitizer build. Artifacts stay in a temporary directory. To inspect a persistent temporary object after your own attempt:

```sh
cc -std=c11 -Wall -Wextra -Werror -O2 -c programming-languages-mastery/01-c/units/01-byte-parser/solutions/parser.c -o /tmp/mm-parser.o
objdump -d /tmp/mm-parser.o
readelf -s /tmp/mm-parser.o
```

These commands inspect the host target, not RISC-V. No specific emitted instruction or timing is promised. Style: four-space C/Python indentation; tests assert the public contract. [Sources](SOURCES.md) and [mastery](MASTERY.md) delimit claims.
