# Build a bounded local shell: words, pipes, ownership

This project builds the mechanism that turns a command line into cooperating
processes. The runnable reference implements its own lexer and pipeline
lifecycle in Python, using the OS process interface for execution. It is a
bounded teaching shell, with an explicit grammar, rather than a POSIX shell.
The original suggested C/Rust implementation remains a transfer challenge.

Read [prerequisites](PREREQUISITES.md), attempt the checkpoints in order, and
consult [hints](HINTS.md) only after writing a failing example. Keep
[solutions](SOLUTIONS.md) closed during that attempt. The [OS lesson](../../05-operating-systems/SELF_CONTAINED_GUIDE.md)
explains the descriptor and process state used here.

## 1. Why a shell exists

A program consumes an argument vector, a current directory, environment, and
open input/output handles. A person usually supplies text. The shell must decide
which characters describe data and which request structure, then arrange those
resources before the program runs. Parsing and launching are separate decisions:
`'a|b'` is one argument containing a pipe character; `a|b` requests two programs.

The state in [minishell.py](code/minishell.py) has three layers:

| Layer | Input | Persistent state | Output |
| --- | --- | --- | --- |
| Lexer | One string | Quote/escape state during that parse | List of argument vectors |
| Shell | Argument vectors | Logical current directory | Builtin action or pipeline |
| Runner | Argument vectors and input bytes | Owned child handles during the call | Captured bytes and all exit codes |

The runner never sends the input text to another shell. An argument containing
`;`, `*`, or `$(...)` stays an argument. That prevents a second shell from
interpreting those characters, but the selected program still decides what its
arguments mean. Passing untrusted text to an interpreter's `-c` option remains
code execution. This local lab executes only programs you authorize.

## 2. Derive the lexer from a concrete trace

Consider this input:

```text
prog 'two words' "a|b" x\ y ''
```

Its result is the single vector `['prog', 'two words', 'a|b', 'x y', '']`.
A split on whitespace would break `two words`. Splitting on every `|` would
break `a|b`. Deleting quotes and then splitting loses the information that
protected those characters. Therefore the parser must inspect each character
while remembering the context in which it occurs.

The lexer maintains `quote` (none, single, double), `escape`, a character buffer,
an argument list, and a command list. It also maintains `active`: an empty quoted
word is an argument even though its buffer has length zero. Without this bit,
`prog ''` and `prog` would become indistinguishable.

| Context and input | Transition |
| --- | --- |
| Escape pending, any next character | Append it literally; clear escape |
| In single quotes, single quote | Leave quoted state |
| In single quotes, anything else | Append literally, including backslash |
| Outside single quotes, backslash | Set escape pending |
| In double quotes, double quote | Leave quoted state |
| In double quotes, anything else | Append literally |
| Unquoted quote | Enter that quoted state; mark word active |
| Unquoted whitespace | Finish the active word |
| Unquoted pipe | Finish word and command |

These are this project's rules. In particular, its backslash handling inside
double quotes is simpler than POSIX shell rules. An unfinished quote or escape
is an error, not a request to read another line. Empty arguments are valid;
an empty executable name or a missing command between pipes is invalid.

A single scan is O(n) time with O(n) output storage. Limits of 4096 input
characters, eight commands, and 128 arguments per command bound this parser's
work. They do not bound the work performed by a child program.

## 3. Launch one process before composing processes

With an argument vector such as `['python', '-c', 'print(3)']`, `Popen` asks the
OS to create a child and run the selected program. `wait()` collects its
termination status. Success is a policy decision: code zero conventionally
indicates success, but an ordinary nonzero exit is still a successfully
observed process termination. A launch failure, such as a missing executable,
has no child exit code for that stage.

The reference keeps the exit code of every stage. A producer can fail while a
consumer still exits zero after reading partial input. Looking only at the
last stage would hide that failure. The command-line entry point returns the
last stage's code for familiarity; the API preserves all codes for diagnosis.

Run from the repository root, with Python 3.12 or newer on a Unix-like host:

```bash
python projects-guided/p02-shell/code/minishell.py -c 'python -c "print(3)"'
python -m unittest discover -s projects-guided/p02-shell/code -p 'test_*.py' -v
```

The first command assumes `python` names your intended interpreter. In a
programmatic lab use `sys.executable`, as the tests do, to pin that choice.
No package installation is needed.

## 4. Why pipelines need resource ownership

For `producer | consumer`, connect the producer's stdout to the pipe's write
end and the consumer's stdin to its read end. Pipes are finite byte streams.
If the producer fills the pipe before the consumer starts, the producer can
block. Waiting for the producer before launching the consumer can therefore
create a deadlock: each is waiting for an event that the current control flow
will never cause. Start all stages, then wait.

A second failure persists even when the data is correct. The consumer knows
that a stream has ended only after every writer handle is closed. A parent
that accidentally retains a writer can keep the consumer waiting forever.
The reference closes each parent-held intermediate read object after handing
it to the next child. The OS-level writer/EOF experiment is in the
[phase experiment](../../05-operating-systems/EXPERIMENTS.md).

The first input and final output use temporary files. This lets the final
stage finish without the parent simultaneously draining a stdout pipe. Each
stderr also uses a separate temporary file. This is a deliberate lab tradeoff:
it simplifies concurrent draining but consumes temporary disk space. The
1 MiB returned-output cap is checked **after** execution and bounds bytes
loaded into Python memory; it does not cap bytes written to disk while a child
runs. A production hostile-command service needs a different resource boundary.

## 5. Cleanup is part of the algorithm

A pipeline can fail halfway through launch. Its first children already exist,
so propagating an exception alone is insufficient. The runner's `finally`
block kills still-running direct children, waits to collect each one, closes
remaining pipe objects, and closes temporary files. A shared monotonic deadline
is used across all waits; assigning a fresh timeout to every stage would let
total waiting time grow with the pipeline length.

The current implementation manages direct children only. Descendants created
by those children can outlive them. It also cannot guarantee an interruptible
process creation call. See [limits](LIMITS.md) before transferring this design
to other environments.

## 6. A builtin has to affect the state that survives

Running a separate `cd` process cannot change the current directory of a
future sibling. This implementation stores a logical directory in its `Shell`
object and passes it as `cwd` when launching each child. `cd child` changes that
object while leaving the Python host process's directory alone. This permits
two Shell instances to maintain independent directories in one process.

Only `cd path` is supported: there is no implicit home-directory lookup, `-`
shortcut, environment expansion, or builtin pipeline stage. Relative paths
resolve against the stored logical directory; resolution follows symlinks.
A directory can disappear between validation and launch, which remains an OS
error. The parser cannot prevent that filesystem race.

## Deliverable and evidence

Submit your lexer and runner, a descriptor ownership table for a three-stage
pipeline, failure tests, a raw run record, and an explanation of a deadlock you
constructed and fixed. Follow the concrete [checkpoints](CHECKPOINTS.md),
[tests](TESTS.md), and [experiments](EXPERIMENTS.md). Sources and their inspected
claim scopes are in [SOURCES.md](SOURCES.md).

This bounded build is STRONG when its evidence gates pass. The larger shell
project remains PARTIAL: C-level fork/exec reconstruction, signals, terminal
ownership, redirection, interactive job control, and portable POSIX semantics
are unimplemented.
