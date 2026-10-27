# Model and platform limits

This is a local educational command runner. It has no interactive terminal,
signals/job control, process groups, redirection, environment/variable/glob
expansion, command substitution, command history, or POSIX-compatible grammar.
Double-quoted backslash semantics are intentionally simplified. cd takes one
explicit path and cannot appear in a pipeline.

The grammar caps input characters, command count, and arguments. Input and
returned stdout are at most 1 MiB; returned stderr is truncated to 65,536 bytes
per stage. Temporary files may grow beyond those memory caps during execution.
Child CPU, disk, address space, open descriptors, network use, and descendant
count are not bounded by this runner. The timeout covers waits using a shared
deadline, not hard real-time process creation or termination guarantees.

Cleanup kills and reaps direct children. Grandchildren may survive. This is
not a sandbox, authorization system, or hostile-code service. A safe production
service needs externally enforced resource and privilege boundaries.

Observations were made on the Linux environment identified in raw evidence.
No portability claim is made for Windows, remote hosts, or other Python
implementations. Temporary paths and elapsed times are expected to vary.
