# Source inspection and original design

Inspected 2026-10-23. Grammar, tokens/ASTs, code, examples, rollback contract and
exercises are original repository designs, with no compatibility claim for Python
or an established language. No third-party parser or copied source is bundled.

| Primary resource | Inspected scope | What it supports |
|---|---|---|
| Python Software Foundation, [Python3.12 Fraction documentation](https://docs.python.org/3.12/library/fractions.html) | Fraction constructors, numerator/denominator and rational operations | The host library used for exact arithmetic. It does not specify this mini-language's grammar or rollback. |
| Python Software Foundation, [Python3.12 full grammar](https://docs.python.org/3.12/reference/grammar.html) | Grammar introduction and expression productions | Comparison showing that a real host grammar is a separate artifact. This interpreter does not invoke that grammar or claim its features. |

Python documentation is under the PSF documentation license with its stated
terms; no documentation passages are copied here. Source references verify only
the stated host facts. Actual local test/experiment evidence is stored separately,
not attributed to external documentation. A lexer/parser security proof or entire
compiler textbook reconstruction has not been performed.
