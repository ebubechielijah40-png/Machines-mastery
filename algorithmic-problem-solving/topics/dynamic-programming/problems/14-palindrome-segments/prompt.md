# Cut a reversible-symbol log into palindromes

Partition a Unicode string into nonempty palindromic substrings with minimum cuts. Return(cut_count,half-open ranges). Empty input needs0 cuts and no pieces. Substrings must remain consecutive; a subsequence is insufficient.

## Worked contract examples

"aab" →1 cut: "aa"|"b". "abba" needs0. Empty returns(0,()).

Integers are exact; practical work uses bounded inputs. Predict an ordinary run,
an empty/minimal run and an impossible or adversarial run before coding. Input
objects must remain unchanged. State the exact objective and return contract.

[Hints](hints.md) and [the separated derivation/reference](solution.md) are for
after the initial attempt. For transfer, change one declared constraint and
identify the first broken argument.
