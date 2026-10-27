# Compiler/runtime exercises

Record predicted output, state and reason before running the reference. Use
[hints](HINTS.md) after an attempt and [solutions](SOLUTIONS.md) to check reasoning.
Exercises1–6 establish representations,7–12 derive the verifier,13–17 debug and
measure,18–20 transfer/reconstruct. Passing author tests is not learner evidence.

1. Classify `print 1`, `print missing;`, `print 1/0;`, and a sum loop that adds2
   to its index. Which stage detects each problem? Which can pass the verifier?
2. Predict `print 2+3*4;print 20-6-3;print 3<2<1;`. Explain a wrong parse for
   each expression and why the declared precedence/association rule excludes it.
3. Derive the results of-7/3,7/-3,-7/-3 without floats. Explain both failures in
   `print -2147483648;` and `print (-2147483647-1)/-1;`.
4. For source `# λ\nprint 2+3;` with an actual newline, find the character offset
   of2 and its UTF-8 byte offset. Why must a debugger distinguish them?
5. Emit stack instructions for `(2+3)*(4-1)` and trace every stack. What is its
   maximum operand depth? Which values must SUB consume in which order?
6. Compile `if(0){print 9;}else{print 4;}`. List absolute target indices, both
   control-flow paths and actual output. Do not count source tokens as targets.
7. Derive stack `(pops,pushes)` for CONST,STORE,ADD,JZ,NEG,HALT. Why does every
   instruction in a statement sequence normally return to an empty stack?
8. Give a raw program whose two paths reach HALT with different stack heights.
   Explain why choosing the larger incoming height is an unsound repair.
9. A path storesx and another bypasses it before LOADx. Show the initialized
   sets and their correct merge. What error would union introduce?
10. Does `CONST1; JZ target` let this verifier discard the branch? Explain the
    precision/cost tradeoff and one valid but conservatively rejected program.
11. Prove termination of the worklist with a backward edge. Separate that proof
    from termination of the executed source program.
12. Construct one shape error in unreachable code and one unreachable HALT in
    otherwise valid code. Explain why the contract treats them differently.
13. Trace `let x=8;print x;x=x/(x-8);` through the fault. Report pc,stack,locals,
    output,steps and source character offset. Which effects would a whole-program
    rollback erase that this VM deliberately preserves?
14. Pause at pc2 in `let x=3;x=x+2;print x;`. Call until twice with breakpoint2.
    Then step once and run. Predict every observed binding/output and why the
    first immutable Snapshot stays unchanged.
15. Count instructions for `print 1;` at budgets1,2,3. Why can output exist when
    halted is false? Test a zero output limit separately.
16. For the counted sum in EXPERIMENTS, derive13n+11 executed instructions and
    n(n-1)/2 output. Check n=0,5,30 without timing the interpreter.
17. Change i=i+1 to i=i+2 when n=5. State what the verifier, closed-form test and
    runtime observe. Design a negative control that tests another layer.
18. Propose safe validation for manually supplied Program records: Booleans as
    operands, duplicate names, mutable code list, unknown opcode, negative target,
    source offset beyond text, stack underflow and oversized stack. Why should
    checking only compiler-generated programs leave a testing gap?
19. Design CALL/RETURN: identify caller continuation, frame/operand boundaries,
    arguments/result, recursion/fuel limits and verifier state changes. Label
    this a design extension, not an implemented feature. Give one invalid return.
20. Without reference code, reconstruct scanner→arithmetic→slots→if/while→verifier
    →step debugger. Self-check sum n=0..10 against a closed form, a division fault,
    incompatible join and a fuel-limited loop. Explain one remaining limitation
    and compare the machine's instructions with actual native compilation.
