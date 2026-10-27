# Hints

1. Track splitting, disappearance of an implicit empty field and glob expansion
   as separate stages. A quoted empty parameter is retained.
2. A wrapper receives a list already; `"$@"` preserves it. Zero parameters differ
   from one parameter whose value is empty.
3. Expansion stages are ordered; filename results do not restart the entire parser.
4. Shell quoting ends before the called program interprets its own argv. Read that
   program's option contract before assuming it supports `--`.
5. Pipeline status comes from a rule over command statuses, not from output text.
6. Control inherited options/startup variables and locale so the experiment varies
   only the intended IFS/quoting condition.
