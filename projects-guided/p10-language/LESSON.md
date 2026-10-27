# From characters to meaning without host eval

## The problem and a deliberate small language

A calculator that splits on spaces cannot parse `2+3*4` or variables reliably.
Letting the host language execute the string silently imports its entire syntax,
object model and authority. We instead define a small language whose valid text,
meaning, error behavior and resource bounds are inspectable. Its grammar is an
original design; no established language compatibility is claimed.

Grammar, with `*` after a group meaning zero or more repetitions:

```text
program    = statement* EOF
statement  = "let" NAME "=" expression ";" | expression ";"
expression = term (("+" | "-") term)*
term       = unary (("*" | "/") unary)*
unary      = ("+" | "-") unary | INTEGER | NAME | "(" expression ")"
```

Integers are ASCII decimal digits; names contain ASCII letters, digits and
underscores, starting with a letter or underscore. `let` is a reserved token.
Whitespace separates tokens but does not change arithmetic. `#` begins a comment
through the line ending. Every statement requires `;`, including the last one.
There are no strings, calls, attributes, arrays, loops, functions or imports.
A negative number is unary minus applied to an unsigned integer token; keeping
that distinction makes `1-2` and `1--2` unambiguous.

## Tokenization preserves evidence of the original text

Scan the next unconsumed character. Skip whitespace or a whole comment. Otherwise
recognize an integer, name or one-character operator/delimiter, record its kind,
text and source offset, then advance. Every successful step consumes characters,
so scanning terminates for finite bounded source. Append an explicit EOF token.
For ` 12 + x;`, token starts are1,4,6,7 and EOF8. A diagnostic must point to an
actual source location, rather than guessing from the order of valid tokens.

The reference uses regular-expression matching for these finite token classes,
not a host-language parser. Because it passes a suffix slice to the regex, worst
case character-copy work can be quadratic in source length; a position-anchored
scanner is a measured optimization exercise. The source limit bounds that cost
here. Recognizing `letx` as one NAME rather than `let` then `x` follows maximal
matching of the identifier pattern, followed by an exact reserved-word check.

## Derive precedence by interfaces, not operator folklore

`expression` consumes complete additive expressions. Each operand is a complete
`term`, so multiplication/division must finish before addition/subtraction.
`term` similarly delegates signed atoms and parentheses to `unary`. Each parser
method returns an AST and leaves the next unconsumed token available to its
caller. That token-position invariant allows composition.

Trace `2+3*4;`:

1. term parses number2 and sees `+`, so returns it without consuming `+`.
2. expression consumes `+` and asks for another complete term.
3. that term parses3, consumes `*`, parses4 and constructs `('*',3,4)`.
4. expression constructs `('+',2,('*',3,4))`; statement then consumes `;`.
5. evaluation multiplies3×4=12, then adds2=14.

The AST nodes actually tag literals as `('number',n)`. These abbreviated trees
show structure, not a second executable format. Parentheses `(2+3)*4` force the
inner expression to return first, producing `('*',('+',2,3),4)` and result20.
The punctuation itself need not survive in the AST once grouping is captured.

The loop builds left-associated trees. `8/4/2` becomes `(8/4)/2=1`, not
`8/(4/2)=4`; `7-3-1` becomes3, not5. Unary recursion gives `--x` two nested signs.
A parser that recursively parses the whole right expression for every operator
can accidentally make subtraction/division right-associated.

## Syntax is not evaluation

Parsing accepts variable names without requiring a binding. The evaluator later
looks them up in its local environment. `missing;` is syntactically well-formed
but has an unbound-name error. `1+;` fails earlier because a term cannot begin at
semicolon. `1/0;` parses into a valid division AST and then fails when evaluating
the denominator. Treating all three as a generic "invalid input" loses the
mechanism and makes debugging harder.

Define evaluation recursively. A number returns its exact rational value. A name
returns the value bound in the environment. A unary node evaluates its operand
and applies the sign. A binary node evaluates the left subtree, then right, and
applies the selected arithmetic operation. For a finite AST this terminates
because each recursive call descends to a smaller subtree. The reference also
has a depth/step guard; finite does not mean affordable.

Rationals are numerator/denominator pairs reduced by the host standard-library
Fraction implementation. `1/3+1/6=1/2` exactly; this is an explicitly chosen
language semantic, not an assertion that hardware represents all real numbers.
A zero denominator is an error. Big integers avoid fixed-width wraparound but
consume growing time/memory; result numerator/denominator bit limits are checked.

## Statements and transactional state

The environment maps names to values. `let x=2; let x=x+3; x/2;` evaluates the
second right-hand side using x=2, replaces the binding with5, and produces5/2.
A let statement itself emits no output. Expressions emit one value in program
order. Rebinding changes one dictionary entry, not the value of an already
created rational object. There are no lexical nested scopes in this language.

To make program failure atomic, copy the caller's environment, parse the whole
program, and evaluate every statement in that private mapping. Only after all
succeed does the evaluator replace the caller's mapping. Starting with x=2,
`let x=9; 1/0;` leaves external x=2. Updating the external dictionary as each
statement runs would leave x=9 despite the failed program. Atomicity is an
explicit local contract here, not durable database transactions or isolation
between threads.

Outputs are also returned only after complete success. No print operation exists
inside the language, so rollback does not need to undo external I/O. Adding file
writes or network calls would fundamentally change that guarantee; a copied
dictionary cannot roll back irreversible external effects.

## Defend a boundary honestly

Reject unsupported characters before parsing. Limit source characters/tokens,
parser/evaluation nesting, evaluation steps and rational bit lengths. A long
left-associated chain can have shallow grammar nesting but a deep AST; separate
evaluator depth checking is therefore necessary. Limits reject programs and do
not silently truncate their syntax or change their answer.

These checks do not establish a hardened execution sandbox. Parsing uses Python
objects, regex and recursion; host resource scheduling, memory quotas, process
isolation and dependency vulnerabilities are outside the guarantee. The caller
also supplies a trusted ordinary dictionary and values, not arbitrary objects
with adversarial Python methods. A network service must validate/limit requests
before accepting work and independently isolate execution.

## Test the meaning independently

The tests enumerate small expression triples and arithmetic operator pairs,
calculate expected Fraction results with direct arithmetic, and compare source
program outcomes. A separate explicit AST check catches precedence. They test
unbound names, syntax, division by zero, offsets, comments, rollback, source and
resource limits. This checks more than comparing parser output with its own
printer. It still does not prove every possible source correct.

The experiment varies only grouping/association or failure position on declared
synthetic programs and retains actual trees/outputs/environments. After explaining
those observations, add exponentiation or block scopes as an extension. Define
its grammar, associativity and error cases first; copying host behavior without
stating it is not a language specification.
