# Verification and debugging

From the repository root:

```bash
python -m unittest discover -s projects-guided/p02-shell/code -p 'test_*.py' -v
python projects-guided/p02-shell/code/experiment.py
```

The unittest suite checks exact parsing, empty quoted words, syntax/size
boundaries, real pipes, an argument containing shell metacharacters, all child
exit codes, 200,000-byte output, missing programs, timeout cleanup paths,
output memory cap, finite timeout validation, logical cd, and command-line
exit propagation. The run record is [evidence/validation.json](evidence/validation.json).
These tests do not establish descendant containment or POSIX compatibility.

Add three tests without copying their implementation: a producer that exits 7
after writing a short prefix; a three-stage pipeline; and two independent Shell
instances. For each, assert final bytes **and** relevant intermediate status or
state. A final-output-only test can overlook a failed producer.

Debugging cases:

1. A quoted pipe becomes a stage separator. Inspect lexer quote state at that
   character; subprocess settings cannot repair a tokenization error.
2. Large output hangs while four bytes succeed. Inspect launch/wait order and
   finite pipe buffers before adding larger buffers.
3. Consumer never observes EOF. Inventory all copies of the write end, including
   a deliberately duplicated descriptor in the host observation lab.
4. Host directory changes unexpectedly. Inspect builtin state; the project
   passes `cwd` per launch and does not call global `os.chdir`.
5. Final exit is zero despite producer failure. Inspect the full return-code
   tuple. Decide and document your own pipeline-success policy.

The provided timeout test exercises the cleanup control path. To establish
absence of process leaks independently, add a child that records its PID in an
owned temporary file, trigger a later-stage launch error, and check termination
with bounded polling. PID reuse and platform differences must be accounted for;
`kill(pid, 0)` alone is not an identity proof.
