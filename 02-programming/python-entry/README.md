# Python entry: from values to an independently tested program

This bridge starts at syntax and builds one complete mechanism. It prepares you
for the repository's mathematical experiments, graph algorithms and small language
project without requiring an external Python tutorial first. Read the arithmetic
and function introduction in [mathematics core](../../foundations/mathematics/core/README.md)
alongside this unit; basic whole-number addition/comparison is enough to begin.
Later mathematical formalism and this introductory programming practice can be
learned together. Full programming-language mastery remains incomplete.

## 1. Run a file; distinguish source, value and output

A Python source file is plain text ending in.py. Save the following as a learner
file, then run `python3 your_file.py` in a terminal. Do not type Markdown fences
or a `>>>` prompt into the file.

```python
capacity = 20
used = 12 + 7
print(used)
print(capacity - used)
```

The first line binds the name capacity to integer20. `12 + 7` evaluates to19,
then used is bound to that value. `print` is a function call that displays its
argument. Expected output is19 then1 on separate lines. Assignment `=` binds;
comparison `==` tests equality. `used = used + 1` first evaluates the old binding
on the right, then changes the binding on the left. Reading an unbound name
raises NameError; it does not silently mean zero.

Values have types defining supported operations: `20` is int; `20.0` is float;
`"20"` is str (text); `True` and `False` are bool; `None` represents absence by
convention. `20+1` yields21 while `"20"+"1"` joins text into"201". Mixing text
and integer with+ raises TypeError. Python integer addition is exact within
available resources; arbitrary integers consume growing memory. `/` on integers
produces a float, while `//` is floor division. The budget below needs only exact
nonnegative integer byte counts, so it does not introduce rounding decisions.
A comment starts with# outside a string and documents a choice without executing.

## 2. Branches express a decision; indentation is structure

```python
used = 19
size = 5
capacity = 20
if used + size <= capacity:
    used = used + size
else:
    print("packet does not fit")
print(used)
```

`<=` produces a Boolean. A colon starts each branch block; four spaces indent
its statements. Exactly one branch runs. The final print is outside both blocks
and here prints19, after the message. Moving it into the first branch would
change which inputs produce output. Whitespace is therefore syntax, not decoration.
`and`, `or` and `not` compose conditions; `!=` means unequal. Parentheses can make
comparisons and arithmetic grouping explicit.

## 3. Lists and loops represent repeated state transitions

`sizes = [12, 7, 5]` creates an ordered list. sizes[0] is12; sizes[1] is7;
len(sizes) is3. Indices start at0. sizes[3] is outside this list and raises
IndexError. `sizes[:2]` creates the first two entries as a new list. Empty list
`[]` has length0. `sizes.append(9)` changes the list by adding one entry at its
end; it does not return a newly populated list to assign back.

```python
used = 0
for size in [12, 7, 5]:
    used = used + size
print(used)
```

The for loop binds size to each entry in order, executing its block once per
entry. used evolves0→12→19→24. It then prints24. With an empty list the block
runs zero times and used remains0. `range(3)` generates0,1,2 for counted repetition;
its stop bound is excluded. You usually do not need numeric indices when the
loop only needs each value.

A while loop repeats while its Boolean condition is true. For `i=0; while i<3`
you must increment i inside the block or the same state repeats forever. `break`
exits the innermost loop immediately; `continue` skips the rest of its current
iteration. The next build uses break because the requirement is an ordered prefix,
not a scan that skips inconvenient items.

## 4. Turn the requirement into a contract and trace

We have a logical payload budget20 **bytes** and ordered packets with payload
sizes12,7,5 bytes. Accept the longest consecutive prefix whose total fits; stop
at the first packet that would exceed capacity. Do not reorder or skip packets.
These integers describe application payloads. They do not measure the storage of
Python integer/list objects, packet headers or actual network memory usage.

State is accepted=[] and used=0. Input size12 fits because0+12≤20, so append12,
used=12. Input7 fits because12+7≤20, so append7, used=19. Input5 would yield24>20,
so stop. Return accepted[12,7] and used19. Remaining capacity is1 byte.

Invariant before each considered packet: used equals the sum of accepted; accepted
is a prefix of the original sequence;0≤used≤capacity. Initially all hold. Accepting
a packet preserves prefix/order and the guarded bound, and increases used by its
size. Stopping at the first failure produces the longest fitting prefix because
all sizes are nonnegative, so including that packet or any later prefix cannot
reduce the cumulative total. The finite list also guarantees termination even
with zero-size packets. Negative sizes would invalidate that argument and are
rejected. This connects programming state to [loop proofs](../../foundations/mathematics/core/02_PROOFS_DISCRETE.md).

Counterexample to the wrong problem: [12,11,9] with budget20 returns[12],used12.
A subset optimizer could choose11+9=20, but that skips the first packet. Another
possible rule could reject everything unless the whole list fits. Neither is
this declared prefix contract. Successful code begins by choosing the right
meaning, not by memorizing a loop.

## 5. Functions make the mechanism reusable

```python
def choose_prefix(sizes, capacity):
    accepted = []
    used = 0
    for size in sizes:
        if used + size > capacity:
            break
        accepted.append(size)
        used = used + size
    return accepted, used
```

This is runnable for the stated valid inputs. `def` creates a function, whose
body runs only when called. `sizes` and `capacity` are parameters: local names
bound to supplied arguments. `choose_prefix([12,7,5],20)` calls it. `return` ends
the call and supplies a result; falling off a function returns None. Here the
comma packs two results into a tuple. `accepted, used = choose_prefix(...)`
unpacks those two values into caller bindings. Printing a result is an I/O effect;
returning it lets tests and other functions use it without parsing display text.

The validated reference [budget.py](budget.py) adds a deliberate API boundary:
sizes must be a list of nonnegative integers and capacity a nonnegative integer.
It validates the whole input before selecting packets. `type(x)` returns a type;
`type(x) is int` deliberately excludes Boolean True, despite Python's numeric
subtype relationship. Do not assume all applications need this strict policy.
Invalid list type raises TypeError; invalid byte counts raise ValueError according
to this API contract. Inputs are never changed and the returned list is new.

## 6. Mutation, aliases and explicit errors

```python
sizes = [2, 3]
alias = sizes
alias.append(4)
print(sizes)  # [2, 3, 4]
```

Assignment alias=sizes creates another binding to the same list, not a copy.
Our accepted=[] is constructed inside each call, so appending to its result does
not append to the caller's sizes. Its integer entries are immutable. Continue
with [objects and aliases](../../programming-languages-mastery/08-python/units/objects-and-aliases/README.md)
before reasoning about nested lists or copied interpreter state.

An empty valid input returns([],0). An invalid negative byte count is a different
condition and must not be disguised as an empty success:

```python
try:
    choose_prefix([12, -1], 20)
except ValueError as error:
    print("invalid byte counts:", error)
```

With the validated reference, raise starts an exception; a matching except handles
it. The remaining body of the failed call does not execute. A SyntaxError such
as a missing colon prevents valid parsing before this execution stage. Read a
traceback from the exception type/message back to the source line; do not catch
all exceptions and silently invent a result. Tests exercise error contracts too.

## 7. Modules, scripts and tests

A.py file is a module. `from budget import choose_prefix` imports that named
function when budget.py is on the module search path. The bottom guard
`if __name__ == '__main__':` runs demonstration I/O only when that file is the
executed main script. Imported tests can call the pure function without triggering
prints. This small separation is why the same mechanism works in experiments,
mathematics scripts and larger projects.

From repository root:

```sh
python3 02-programming/python-entry/budget.py
python3 -m unittest discover -s 02-programming/python-entry -v
python3 02-programming/python-entry/experiment.py
```

The demo's expected first line is `2 packets, 19/20 payload bytes: [12, 7]`.
`-m unittest` runs the standard-library test framework; discover locates test_*.py
under the selected start directory. `-v` prints individual test method names.
No third-party package installation is needed. In the tests, a class groups named
checks, self refers to that test instance, assertEqual compares an actual result
with an expected value, and assertRaises requires a particular error. You can
read each assertion without first mastering every class feature. An assertion
failure shows a behavior mismatch; an error may mean setup/import or an unexpected
exception. A green run does not prove all future programs correct.

[tests.txt](tests.txt) records six passing methods, including an independent
finite oracle enumerating all prefixes for lists of length0..5 over sizes0..3
and budgets0..9. It chooses the longest fitting prefix by definition rather than
copying the greedy loop. [observed.json](observed.json) records five actual semantic
runs and environment. No timing or heap-memory claims are made. The full public
function scans all n entries for validation, then at most n for selection: O(n)
operations and up to O(n) result entries in a constant-word model.

Attempt [EXERCISES](EXERCISES.md), then [HINTS](HINTS.md) and [SOLUTIONS](SOLUTIONS.md).
After the reconstruction gate, proceed to [arrays](../../algorithmic-problem-solving/topics/arrays/README.md),
[graph frontiers](../../algorithmic-problem-solving/topics/graphs/README.md) and
[the expression-language build](../../projects-guided/p10-language/README.md).
Mathematical experiments reuse these same values/functions/loops/modules/tests;
you now have their programming entry bridge.
