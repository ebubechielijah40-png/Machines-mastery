# Actual executable test route

From repository root, Python 3.10+, no third-party dependencies:

```sh
python3 -m unittest discover -s 18-computational-biology/code -p 'test_alignment.py' -v
python3 18-computational-biology/code/test_sequence_lab.py
python3 -m unittest discover -s projects-guided/p14-bioinformatics/tests -v
```

The new alignment suite has 9 test methods. Within them it checks 675 global and 147 local sequence/scoring cases against an independent exhaustive path/interval oracle; these counts are cases, not test-method counts. It checks exact worked matrix, reconstruction, independent rescoring, empty inputs, local no-positive match, deterministic ties, symmetry of score, opposing-gap behavior, and resource/type contracts.

The CLI suite has 4 test methods exercising subprocess execution, SHA-256 provenance, local spans, global score, malformed FASTA, invalid DNA, record count, duplicate names, empty records, byte/cell caps, positive gap rejection, and literal N semantics. Each subprocess has a 5-second test timeout. Temporary input files are removed by the test harness.

On 2026-10-22 all 13 new test methods passed, and the existing sequence test script printed `sequence_lab: PASS`. Complete stdout/stderr and exit codes are captured in [validation.json](../../18-computational-biology/alignment/evidence/validation.json). These checks concern a bounded educational implementation, not production readiness, biological validity, or learner mastery.

Add a regression before fixing any demonstrated failure. Do not replace independent reconstruction/oracle checks with assertions that call the same optimizer twice. For your unaided implementation also test line-order preservation: a reversed traceback can keep the additive score while reconstructing the wrong sequence order.
