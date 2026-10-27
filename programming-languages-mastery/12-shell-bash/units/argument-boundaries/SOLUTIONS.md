# Checkable reasoning

1. Quoted-at returns the original three strings in both directories. Quoted-star
   returns one joined string under default IFS. Unquoted-at splits'a b', drops the
   empty field and leaves an unmatched '*' literal under the lab's default Bash
   glob options in an empty directory; with file'x y', it expands '*' to one
   filename'x y'. Changing nullglob/failglob would change the unmatched case.
2. The essential invocation is `target "$@"`, where target is fixed or separately
   trusted/quoted. Assert equality of input/output lists, not a pretty printed line.
3. Word splitting occurs before filename expansion; the filename's characters
   are not reparsed as source or split again in this experiment.
4. The shell constructs argv; the target parses option/value syntax. A quoted
   leading-hyphen argument retains its characters and may still be an option.
   A documented `--` or explicit option-value field can resolve that target grammar.
5. `false | true` returns0 by default,1 with pipefail in the recorded local run.
   Inspect statuses independently of whether the consumer printed plausible output.
6. Changing IFS changes unquoted field splitting and quoted-star joining. It does
   not make quoted-at collapse already separate positional parameters. Preserve
   the original list for the most direct independently checkable invariant.
