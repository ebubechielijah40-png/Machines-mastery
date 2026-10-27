# Source verification and attribution

Original lexer, lifecycle code, traces, exercises and explanations were written
for this repository. Python wraps process creation here; the implementation is
not a copied shell and does not claim conformance to POSIX shell grammar.

| Primary resource | Inspected scope and date | Claims supported |
| --- | --- | --- |
| [Python 3.12 subprocess documentation](https://docs.python.org/3.12/library/subprocess.html) | 2026-10-22; Popen, run, wait, communicate, shell/security notes | Argument-list execution, cwd, status, pipe waiting/deadlock considerations |
| [Linux man-pages pipe(7)](https://man7.org/linux/man-pages/man7/pipe.7.html) | 2026-10-22; DESCRIPTION and pipe capacity; displayed man-pages 6.19 | Finite byte stream, EOF after all writers close, blocking behavior |
| [Linux man-pages dup(2)](https://man7.org/linux/man-pages/man2/dup.2.html) | 2026-10-22; DESCRIPTION | Descriptor copies refer to an open file description; shared offset |
| [Linux man-pages execve(2)](https://man7.org/linux/man-pages/man2/execve.2.html) | 2026-10-22; DESCRIPTION and arguments | Program image replacement and argv interface |

Python docs use the PSF documentation license; Linux man-page license notices
remain with their originals. These are verification references, not vendored
source text. No substantial passages were reproduced. An Open Group POSIX page
was inaccessible during inspection, so formal POSIX conformance is unverified
and unclaimed. [Raw evidence](evidence/observed.json) supports only this local
execution; the resource-limit choices and grammar are original project design.
