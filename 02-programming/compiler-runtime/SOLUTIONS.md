# Explained compiler/runtime solutions

1. `print 1` lacks a semicolon and is a SourceError. `print missing;` fails name
   resolution during compilation; it does not reach LOAD. `print 1/0;` compiles
   and verifies, then faults at DIV. Adding2 to the index can compile, verify
   and halt yet solve a different sum problem. An independent specification test
   detects that logical error, not the structural verifier.

2. Results are14,11,1. For the first,3*4 is consumed as the right operand of+
   before the enclosing addition emits. For subtraction,20-6 emits before the
   second-3 is combined, giving14-3. For comparison,(3<2) yields0 then0<1 yields1.
   Reading it as a Python comparison chain would change the declared language.

3. Magnitudes give7//3=2. Sign combinations produce-2,-2,2. The first source
   contains a literal2147483648, which violates the scanner's magnitude bound;
   NEG never executes. The second constructs MIN_INT legally, then its quotient
   is2147483648, outside the runtime range. These are separate failure stages.

4. Characters are `#`0,space1,λ2,newline3,p4,r5,i6,n7,t8,space9,2 at10.
   The UTF-8 encoding ofλ is two bytes, so2 is at byte11. A character offset used
   directly as a byte offset would point to the preceding space. Source offsets
   need both an encoding and a coordinate convention when crossing boundaries.

5. Emit CONST2,CONST3,ADD,CONST4,CONST1,SUB,MUL. Stacks become[2],[2,3],[5],
   [5,4],[5,4,1],[5,3],[15]. Maximum depth3. SUB reads left4,right1, replacing
   both with3. Reversing the operands gives-3 and final-15, a useful mutant.

6. Indices are0 CONST0,1 JZ5,2 CONST9,3 PRINT,4 JUMP7,5 CONST4,6 PRINT,7 HALT.
   The then path is0,1,2,3,4,7; the else path is0,1,5,6,7. Actual condition0
   selects the else path and prints4. Both paths reach HALT with an empty stack.
   Patching JZ to4 would enter an unconditional skip and produce no output.

7. CONST=(0,1),STORE=(1,0),ADD=(2,1),JZ=(1,0),NEG=(1,1),HALT=(0,0), with
   HALT additionally requiring height0. An expression leaves one value; assignment
   STORE or output PRINT consumes it. Conditions are consumed by JZ. Every source
   statement therefore preserves its incoming empty boundary if emission is
   correct. Raw bytecode must still be checked instead of assuming this theorem.

8. One example is CONST1,JZ4,CONST9,JUMP4,HALT. One modeled path reaches4 with
   height0 and the other with height1. Taking the larger would pretend a missing
   operand exists on the first path, while HALT's empty-stack contract fails on
   the second. Reject the incompatible merge rather than silently change code.

9. The STORE path contributes{x}; the bypass contributes{}. Intersection is{};
   LOADx is therefore invalid. Union{x} would incorrectly permit reading an
   uninitialized slot after taking the bypass. Initialization is a must property.

10. No: branch propagation uses shape, not known constants. CONST1,JZ4,CONST9,
    STORE0,LOAD0,PRINT,HALT has a modeled path0→1→4 that reads an uninitialized
    local. Real execution's nonzero condition always takes the initialized path.
    Constant propagation could improve precision, but would require a richer
    abstract domain and additional join/transfer rules; it is not present here.

11. Each code position is discovered at most once. After discovery its definitely
    initialized set can only lose members during merges, and at most64 members
    can be removed. Each removal can trigger finitely many successor updates.
    Thus the finite worklist reaches a fixed point or rejects. In contrast,
    JUMP0 keeps executing the same concrete state until its finite fuel fails;
    worklist termination does not imply program termination.

12. Program[JUMP2,UNKNOWN,HALT] must fail the all-record shape pass even though
    UNKNOWN is unreachable. Program[JUMP0,HALT] passes structure: the last record
    is a valid HALT but is unreachable. Its reachable edge is0→0, with no stack
    requirement or falloff. Runtime fuel handles its nontermination. Rejecting
    every unreachable HALT would impose a different contract than this verifier.

13. For exactly that source text, pc8 is DIV at character offset19. Incoming
    stack[8,0],locals[8],output[8],steps8,haltedfalse are preserved in the fault.
    The assignment has not reached STORE. Whole-program rollback would erase
    the earlier successful declaration and PRINT; this VM deliberately preserves
    them. Resuming without changing state repeats the same division-by-zero fault.

14. After CONST3 and STORE0,pc2 has stack[],locals[3],output[]. Both until calls
    pause there. A step executes LOAD0, giving stack[3],pc3; run completes the
    addition/store/output and prints5 with locals[5]. The initial snapshot still
    has None in its slot because its tuples were not mutated by later steps.

15. Budget1 commits CONST1, then faults at PRINT with stack[1],output[],steps1.
    Budget2 commits PRINT as well, so output[1],empty stack,steps2,haltedfalse;
    HALT cannot consume its next unit. Budget3 reaches HALT normally with output1.
    With output_limit0, CONST commits but PRINT faults without popping its operand.

16. Two initializations cost4. Each successful iteration runs four condition
    instructions, eight body instructions and one back jump:13. The final false
    condition costs4, LOAD/PRINT cost2 and HALT costs1. Total=4+13n+4+2+1=13n+11.
    The sum of0…n-1 pairs to n(n-1)/2. n=0 gives0/11steps,n=5 gives10/76steps,
    n=30 gives435/401steps. This cost is the declared VM instruction count, not
    a wall-time prediction: tuples, validation and host runtime add different work.

17. Indices0,2,4 contribute6, theni becomes6 and exits. Stack/init structure
    remains valid. The closed-form expected10 fails, identifying a logical
    mismatch; the runtime itself halts normally. A branch-target-outside-code
    mutant instead tests shape validation, while divisor0 tests concrete values.
    Keeping these distinct makes a failed test explain a particular mechanism.

18. Require exact non-Boolean bounded integers for slots,constants,targets and
    offsets; immutable tuples for code/names; exact known Instruction records;
    unique valid names; opcode-specific operands; reachable stack transfer checks;
    and the declared maximum depth. Compiler-generated successes may never create
    a malformed raw record, so only testing them leaves verifier rejection paths
    and the public manually constructed Program boundary largely unexamined.

19. One design pushes a call frame containing continuation pc, caller frame and
    operand-stack base, creates initialized parameter slots in a fresh callee
    frame, then enters its code. RETURN checks the callee's expected result count,
    removes its frame, restores continuation and transfers the result. Abstract
    signatures must record argument/result shapes and frame boundaries. A return
    with two values for a one-result function is invalid; returning without a
    caller is invalid. Fuel and a finite call-depth policy must constrain recursion.
    Flow currently implements none of these features; this is a design solution.

20. A successful reconstruction explains and re-derives source scanning,
    precedence emission, slot state, target patching, worklist intersection,
    atomic publication and debugger pause behavior, then independently checks
    outputs. Sum n=0..10 should equal0,0,1,3,6,10,15,21,28,36,45. A division fault
    must preserve earlier output and its incoming stack; an incompatible join
    must be rejected; a loop with no progress must exhaust fuel. Native compilation
    later emits CPU code and links symbols, whereas this VM interprets custom
    records inside Python. No fixed learner mastery state follows from reading
    these answers; retain the unaided construction and actual test evidence.
