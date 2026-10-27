# Bash: preserve argument boundaries before running commands

A process receives an ordered list of argument strings. A shell first interprets
source text and expansions to construct that list. Losing a boundary can change
which files or options a program sees even when no shell syntax is executed.
This unit makes those transformations observable in a temporary local directory.
Prerequisites: strings, lists and [Python entry](../../../../02-programming/python-entry/README.md).
Python here prints argv as JSON; Bash performs the expansions being studied.

## Separate source syntax from data

A quoted literal `"two words"` in shell source is one argument. An empty quoted
literal `""` is one empty argument. The quote characters control parsing and are
not part of the resulting strings. Expansion substitutes values into parsed
words; unquoted results can undergo word splitting and filename expansion.
A glob such as `*.txt` then depends on files in the working directory, so testing
only in an empty directory can hide a broken wrapper.

The lab controls three temporary files: alpha.txt, two words.txt and other.bin.
It passes positional parameters `"two words"`, `""`, `"*.txt"` using Python's
subprocess argument list. In Bash, the useful forwarding form is:

```bash
"$python" "$helper" "$@"
```

`"$@"` preserves one argument per positional parameter, including embedded spaces,
empty strings and literal glob characters. With zero positional parameters it
contributes zero arguments. A Bash array uses the corresponding
`"${items[@]}"` form. A string containing a reconstructed command line cannot
reliably preserve arbitrary original boundaries; retain a list/array instead.

## Derive the three observed outcomes

In the same controlled directory, quote choice changes only the expansion rule:

| Forwarding form | Actual helper arguments |
|---|---|
| `"$@"` | `["two words", "", "*.txt"]` |
| unquoted `$@` | `["two", "words", "alpha.txt", "two words.txt"]` |
| `"$*"` | `["two words  *.txt"]` |

For unquoted expansion, the space in the first parameter splits it. The implicit
empty field vanishes. The pattern matches two filenames; the matched filename
with a space remains a single expanded filename at that stage, rather than being
split a second time. `"$*"` joins all positional parameters using the first IFS
character (space in this controlled default), then presents that combined string
as one argument. The doubled space preserves evidence of the empty original
parameter, but no longer preserves a reversible list boundary encoding.

The lab clears inherited shell startup/option variables and sets LC_ALL=C so
filename ordering is reproducible for these ASCII names. Actual filenames may
contain newlines and other characters. Quoted forwarding preserves the newline
case in the tests; formatting argv with plain echo would obscure its boundaries.
A shell argument cannot contain a NUL byte, a separate process-interface limit.

## Metacharacters in data and option semantics

A parameter value containing `$(touch marker)` or `a; b` does not become newly
parsed shell syntax merely because it is expanded. The quoted experiment passes
those exact strings; no marker is created. Evaluating constructed source with
eval or invoking another `sh -c` interpretation would add a new parsing boundary,
which this wrapper deliberately does not perform. This local observation does
not establish that an arbitrary command using the resulting data is safe.

Even correctly quoted `--leading-option` may be interpreted as an option by the
called program. Quoting controls the shell's boundaries, while the program defines
its option/value grammar. Use the program's documented end-of-options mechanism
where supported. Do not claim that double quotes solve arbitrary command semantics,
SQL injection, path authorization or filename race conditions.

Command substitution removes trailing newline characters from its captured output:
`value=$(printf 'a\n\n')` produces'a' in this experiment. Quoting `$value`
protects its resulting single boundary but cannot recover already removed trailing
newlines. Choose a file/stream or a stated encoding if exact arbitrary byte data
must cross a command boundary.

## Pipelines have an independent failure boundary

For the controlled pipeline `false | true`, default Bash reports the final
command's status0. With `set -o pipefail`, the pipeline reports the rightmost
nonzero status, here1. The script captures those actual values. A wrapper that
checks only the default status can mistake a failed producer for complete success.
This is separate from argument quoting. This unit does not teach `set -e` as a
universal error-handling strategy; explicit status contracts are easier to test.

## Execute and interpret

```sh
python3 -m unittest discover -s programming-languages-mastery/12-shell-bash/units/argument-boundaries -v
python3 programming-languages-mastery/12-shell-bash/units/argument-boundaries/lab.py
```

[tests.txt](tests.txt) records seven passing methods. [observed.json](observed.json)
records actual Bash5.2.21/Python3.12.14, the three forms above, empty/newline data,
metacharacter preservation, no marker, trimmed substitution and pipeline statuses.
The experiment changes one expansion/status form while holding inputs/files/runtime
fixed. Its measurements are exact argv/status values, not performance timings.
Directory contents, IFS, options and locale could produce different unquoted
outcomes; those are explicit controlled variables, not alternative explanations
left hidden. The robust forwarding invariant is exact preservation of the input
argument list, independently asserted for multiple cases.

Attempt [EXERCISES](EXERCISES.md), then [HINTS](HINTS.md) and [SOLUTIONS](SOLUTIONS.md).
[SOURCES](SOURCES.md) records that the current GNU web manual could not be retrieved;
its full-source verification remains blocked. The local experiment and inspected
builtin help support only the declared version/scope. Signal handling, redirections,
job control, traps, POSIX portability and production shell tooling remain incomplete.
