# Optional exact-timing decoder lab

Reference solution: inspect only after your own trace or implementation attempt. Original assistant-written instructional code based on the unit's explicitly limited model; not source code from the book. No dependencies beyond Python 3.10+ standard library. Four-space Python indentation; standard `unittest`, tests in `test_decoder.py`. No installation or physical apparatus required.

From the repository root, run:

```sh
python3 -m unittest discover -s books/code-petzold/generated/chapters/01/lab -v
```

For an interactive trace:

```sh
cd books/code-petzold/generated/chapters/01/lab
python3 -c 'from decoder import encode, decode; events = encode("N E", 2); print(events); print(decode(events, 2))'
```

The output is a computation on supplied integers, not measured light behavior. Tests cover independently specified traces, all letter strings up to length four with every word-boundary placement at three scales, an independent duration formula, ambiguous scales, gap corruption and invalid inputs. Round trips alone could hide matching encoder/decoder bugs; the fixed traces and cost checks provide additional independent checks.

Text uses only E/T/A/N with single spaces between words. ON is 1, OFF is 0. Positive integer τ and durations share a chosen unit. Events alternate, start/end ON, and EOF terminates the final character. Empty input is valid. Exact timings and 6τ word gaps follow this unit's book-local idealization; no external standard, noise tolerance or timing calibration is claimed. See [formal analysis](../06_FORMALISMS.md) for correctness and complexity limits.
