# Attempt before opening solutions

1. Distinguish the name x, its declaration, one runtime frame, a binding and its value.
2. Trace all frames in the registry/block experiment. Predict both lookup modes.
3. Why does assignment to x differ from adding a later shadow declaration of x?
4. Compute lexical distances for x read in its declaring block, a child block,
   and a function body declared in that child block.
5. A function closes over global x=4. A caller parameter is also x and has100.
   Which value does the function return, and which parent pointer determines it?
6. Explain the two states in declare→resolve initializer→define. Why not use
   one dictionary insertion after visiting the initializer?
7. Predict the1,2,1,3 counter sequence, identifying exactly which cells are shared.
8. Change the second factory call to an alias of the first returned closure.
   Predict a(),a(),b(),a() without running it.
9. Write an assignment counterexample where later shadowing changes the wrong
   frame in mutable-chain mode. Include both final outer and inner values.
10. Construct a statically invalid own-initializer use in a branch that runtime
    would not select. State whether a preceding Print is executed.
11. Our globals are dynamic named slots. A function is declared before its global
    x is initialized; compare a call before and after that initializer runs.
12. Explain why function self-reference resolves but a later sibling local
    function declaration is not automatically visible in an earlier body.
13. Two Name('x') nodes occur in different scopes. Why must their table keys use
    occurrence identity? Why does reusing one object for both occurrences fail?
14. Find the off-by-one bug if a function body gets an extra runtime Block frame
    without a matching resolver scope. Give a failing distance1 example.
15. Derive worst-case resolver and runtime-read complexity in nodes n, lexical
    depth h and recorded distance d. Include name-map lookup assumptions.
16. Add multiplication and its exact integer/type/resource contract. Ensure the
    resolver visits both operands, then test an argument containing a captured name.
17. Add a slot-index representation as an extension: record (distance,slot),
    allocate parameter/local slots, and compare traces with the name-map runner.
18. Define a language where local declarations are hoisted. Which resolver,
    initialization and runtime lookup rules must change together? Show one
    program whose meaning differs; do not label one language's choice universal.
19. Give three reasons why steps/call bounds do not turn this host interpreter
    into a secure sandbox. Distinguish language errors from resource policy.
20. Reconstruction challenge: close the reference. Build the late-declaration
    failure, fixed addresses, shared-cell counter and static error checks from
    the stated semantics. Submit predictions, code, independent marker tests,
    actual outputs, one failed design and its correction. Then change one scope
    rule deliberately and update both resolver and runtime so they agree.

Rubric:4 points for correct binding/value/frame distinctions and traces;4 for
matching resolver/runtime invariants and static errors;4 for executable shared
mutation/assignment/recursion checks;4 for independent oracles/failure diagnosis;
4 for source scope, resource/compatibility limits and unaided transfer. A copied
reference with passing tests does not demonstrate the reconstruction criterion.
