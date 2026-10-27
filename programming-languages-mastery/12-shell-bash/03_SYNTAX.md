# Bash source syntax constructs a process argument list

The [argument-boundaries build](units/argument-boundaries/README.md) makes quoted
versus unquoted expansion observable in a controlled temporary directory. A process
receives separate strings; Bash source parsing and expansion construct them first.
Quotes are syntax, not characters passed to the target.

Quoted `"$@"` preserves separate positional arguments, including empty values,
spaces, newlines and literal wildcards. Quoted `"$*"` joins them into one string.
Unquoted expansion can split fields, drop an implicit empty field and expand a
glob according to directory contents/options. With inputs ["two words","","*.txt"],
the actual unquoted lab output is["two","words","alpha.txt","two words.txt"].
A matched filename with spaces remains a filename at that expansion stage.

[Seven actual tests](units/argument-boundaries/tests.txt) check boundaries and
controlled status behavior, not only visually plausible echo output. Reconstruct
a wrapper forwarding an argument array without joining it into source text, then
explain the separate option grammar of the called program. The source map records
current GNU web-manual retrieval as BLOCKED; only installed-version observations
and inspected builtin help are claimed. Job control, traps and redirections remain
outside this developed slice.
