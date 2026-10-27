# Actual validation and interpretation

Executed on2026-10-23 with the environment recorded in evidence/stack.json:

```sh
python3 projects-guided/computational-biology-stack/run_stack.py
python3 -m unittest discover -s projects-guided/computational-biology-stack -p 'test_*.py' -v
```

The integration test passed. It checks the hand alignment score10, independently
expressed JC inverse, neutral mean/diversity identity, exact root height and
manifest structure. The underlying population/phylogeny suite has twelve passing
mechanism tests; the alignment project's independent path oracle and CLI tests
are preserved in their existing units. The stack test does not replace them.

All three examples are synthetic. No population history or four-taxon tree is
inferred from the two-record fixture. Interpretation requires the model boundaries
stated in README.md. Source hashes change after code edits; regenerate the runner
output after changes rather than copying a previously reported hash. Reconstructing
from memory is a learner deliverable, not an author-observed result.
