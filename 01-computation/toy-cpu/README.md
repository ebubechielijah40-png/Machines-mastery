# From a full adder to a running stored program

This unit constructs an original, deliberately small computer. Its entire
architectural state fits on paper: sixteen memory bytes, one accumulator, a
four-bit program counter, carry and halt bits, and a cycle count. You can derive
every result without trusting the simulator. This is an abstract interpreter,
not a timing-accurate HDL processor or an implementation of Hack or RISC-V.

Prerequisites: integer place value, Boolean AND/OR/XOR, lists and loops in Python.
If you are meeting bit representation for the first time, work the first two
sections before reading `cpu.py`. After this unit, continue to the architecture
and assembly tracks; the physical implementation requires clocking, propagation
delay, setup/hold constraints and reset circuits that this atomic model omits.

## 1. A representation becomes useful through operations

An eight-bit word represents the unsigned integer
\(a=\sum_{i=0}^{7}a_i2^i\), where every \(a_i\) is zero or one. The same
word can be interpreted as data or an instruction. Nothing in a bare memory
byte marks its purpose: the program counter determines which byte is decoded.
That explains both the flexibility of a stored program and accidental execution
of data. Signed interpretation is a separate convention. In two's complement,
255 represents −1; addition still uses the same eight wires.

A full adder accepts bits \(a,b,c\), where \(c\) is carry from the previous
column. Its sum bit is \(s=a\oplus b\oplus c\); its carry is
\(d=(a\land b)\lor(c\land(a\oplus b))\). Why? An odd number of input ones
gives a one in the current column; at least two ones require a carry. The
checkable invariant is \(a+b+c=s+2d\), true for all eight triples.

Connect eight such mechanisms from least to most significant bit. Inductively,
the low \(k\) output bits plus \(2^k\) times the outgoing carry equal the
sum of the low \(k\) input bits. At eight bits,
\(a+b=r+256c_{out}\). The result is therefore \((a+b)\bmod256\). The
simulator implements this ripple, then tests it against Python's independent
unbounded integer arithmetic for **all65,536** input pairs.

Worked overflow: 255+1 gives low byte00000000 and carry1, because256=0+256×1.
Unsigned carry does not mean signed overflow. Interpreted as signed integers,
−1+1=0 is representable;127+1=−128 wraps without an unsigned carry. Adding a
signed-overflow flag would require a new architectural specification.

## 2. State, instruction encoding and invariants

Each byte has high nibble opcode and low nibble operand: `word=16*opcode+operand`.
Addresses are0–15. Sequential execution uses `(pc+1)%16`. Accumulator arithmetic
wraps modulo256. Carry persists across instructions except ADD; it is not a
general zero/negative status register. JZ tests the current accumulator directly.

| Mnemonic | High nibble | Operation in one abstract cycle |
| --- | --- | --- |
| NOP | 0 | Advance PC; low nibble must be0 |
| LDI n | 1 | A←n, immediate limited to0–15 |
| ADD a | 2 | A←(A+M[a])mod256; carry←overflow beyond255 |
| LDA a | 3 | A←M[a] |
| STA a | 4 | M[a]←A |
| JMP a | 5 | PC←a |
| JZ a | 6 | PC←a if A=0, otherwise advance |
| HLT | F | Advance PC, set halted; low nibble must be0 |

Unsupported opcodes and reserved operands raise `DecodeError` without changing
architectural state. A successful cycle increments the cycle count exactly
once. A halt prevents another step. `CPU` copies its input memory so execution
does not mutate the caller's program list. Public mutable state is revalidated
before each step; the educational interface is not a sandbox for untrusted code.

Inside `step`, fetch reads the old PC, decode separates the nibbles, execution
computes proposed register values and an optional memory write, then commit
updates the state. This staging explains precise decode failure. It does not
model parallel hardware or a real CPU's speculation, exceptions or memory bus.

## 3. Hand-execute an entire program

Place these six words at addresses0–5 and zeros elsewhere:

| Address | Assembly | Encoded byte | A after execution | Visible change |
| --- | --- | --- | --- | --- |
| 0 | LDI3 | 0x13 | 3 | immediate enters register |
| 1 | STA14 | 0x4e | 3 | M[14]=3 |
| 2 | LDI4 | 0x14 | 4 | old accumulator replaced |
| 3 | ADD14 | 0x2e | 7 | memory operand, not literal14 |
| 4 | STA15 | 0x4f | 7 | M[15]=7 |
| 5 | HLT | 0xf0 | 7 | PC=6; halted=true; cycles=6 |

The common incorrect implementation treats ADD14 as `A+=14`. The hand result
would then be18, so this example distinguishes immediate and indirect memory
operands. The tests also verify that the original input list still has M[15]=0.

## 4. Derive multiplication without a multiply instruction

For unsigned `a` and positive `b`, keep product `p=0` and counter `c=b`.
Repeatedly set `p=(p+a)%256`, then `c=(c-1)%256`, stopping at zero. The invariant
after \(k\) iterations is \(p\equiv ka\pmod{256}\), \(c=b-k\).
For1≤b≤255, before the final iteration c>0, so the counter does not wrap.
Termination gives p≡ab. The program uses memory[12]=255 so ADD12 subtracts one
without adding an ISA operation.

Read `multiplication_program` beside its address list. Addresses12–15 hold −1,
product, multiplicand and counter. Addresses2–9 form the loop. Each nonfinal
iteration takes8 instructions, the final one takes7 because JZ skips JMP.
Initialization takes2 and final load/halt2: total **8b+3**. For3×4 this is35
cycles, ending with accumulator12. This count is an algorithmic operation count,
not a measured hardware execution time. b=0 requires an entry zero check and
currently is rejected: silently accepting it would enter a wraparound loop.

## 5. Run, inspect and break the machine

From the repository root, Python3.10+ and the standard library suffice:

```bash
cd 01-computation/toy-cpu
python -m unittest -v test_cpu
python experiment.py
```

The executed JSON in [evidence/cpu-experiment.json](evidence/cpu-experiment.json)
records environment, all35 transitions and a controlled fault. The fault changes
the JMP at9 from target2 to target9. After the first product update, the PC stays
at9. The100-cycle budget is exhausted with PC9 and a retained state for diagnosis.
This actual observation supports the predicted self-loop for this program. It
does not show that arbitrary nontermination is decidable: a finite execution
budget can stop a slow correct computation as well as an infinite one.

Research question: does a single branch-target error change termination while
leaving opcode validity intact? Hypothesis: this self-loop does. Controlled
variables: ISA, initial a=3/b=4, memory except address9,100-cycle bound. Instrument:
transition logs, PC, memory, cycle count. Alternative explanation for a timeout
would be an insufficient budget; the unmodified program's35-cycle trace and
the stable PC9 distinguish that case here. Follow-up: change JMP9 to JMP0 and
predict the terminating but incorrect result before executing it.

When a result fails, locate the **first** transition differing from a hand trace.
Check word encoding, operand interpretation, memory aliases, PC increment and
flag lifetime in that order. A final wrong accumulator alone hides causality.
Unified memory intentionally permits STA to overwrite a later HLT; execution
then changes. Real systems use memory protection and privilege mechanisms
outside this model. Limit cycle budgets when exploring malformed programs.

## 6. Transfer and honest completion boundary

The executable mechanism covers combinational addition, machine state,
instruction decoding, addressing, branching, wraparound, self-modification,
tracing and bounded fault injection. Its tests include independent mathematical
oracles, exhaustive tiny input spaces, invalid-state atomicity and hand programs.
It does not implement interrupts, a stack, I/O, pipelining, caches, an assembler,
an ABI, clocked HDL or transistor-level behavior. Those remain domain work.

Attempt [EXERCISES.md](EXERCISES.md), open [HINTS.md](HINTS.md) only when needed,
then compare [SOLUTIONS.md](SOLUTIONS.md). The [guided CPU build](../../projects-guided/p01-logic-cpu/README.md)
uses milestones that let you reconstruct this mechanism before reading the
reference solution. [SOURCES.md](SOURCES.md) distinguishes inspected sources from
original design and unperformed hardware work.
