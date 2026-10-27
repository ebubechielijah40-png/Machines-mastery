# Compiler/runtime hints

1. Parsing/name resolution and structural checking precede concrete execution;
   intended mathematics is a fourth question.
2. Multiplication has higher precedence; equal precedence associates left.
3. First divide magnitudes. The nonnegative literal is scanned before NEG exists.
4. Count Python string characters; the Greek character occupies two UTF-8 bytes.
5. Keep the left multiplication operand while evaluating its right operand.
6. Number emitted instructions from0; JZ pops its condition; emit one skip jump.
7. Distinguish inputs required from net change; NEG requires1 despite net0.
8. One branch should push a value and the other leave the stack empty.
9. Ask what holds on every incoming path rather than on at least one.
10. Our abstract state has no constant values. Use an impossible conditional path.
11. Count finite slots that can be removed from a position's initialized set.
12. Shape checks scan every record; reachability analysis starts only at0.
13. The DIV is at source `/`, after both its operands have been pushed.
14. A breakpoint pauses before its instruction; it is not a command to execute it.
15. CONST,PRINT,HALT each consume one unit of global fuel.
16. Separate initialization, repeated condition/body/back-edge and final exit.
17. A static shape proof cannot know the sum problem's intended set of indices.
18. A public bytecode boundary needs its own contract; raw records bypass parsing.
19. A callee needs its own locals and saved continuation, not a shared flat slot0.
20. Predict before running; independently calculate the expected result first.
