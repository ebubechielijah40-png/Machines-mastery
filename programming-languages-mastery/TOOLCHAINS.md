# Toolchain investigation map

[EXPLANATION] Planned vertical route: preprocessing → tokens/lexing → parsing/AST → semantic analysis → intermediate representation → optimization → code generation → assembly → object files → symbols/relocation → linking → loading → runtime. This is an investigation map, not a claim that every compiler has identical passes.

The C exemplar observes an object and disassembly. Later units must inspect LLVM IR, linker scripts, Make, CMake, GDB, objdump, readelf, nm and strace in a pinned local toolchain before teaching commands. Identify which artifact each tool reads/writes. Source variables need not have one-to-one instruction or storage mappings after optimization. Debug information associates source with generated operations but is not the execution mechanism itself.

Language cross-connections: Rust may use an LLVM backend, but language semantics are not LLVM semantics. Zig backend choice is version/target-dependent. Python bytecode and reference counting are implementation questions. JVM bytecode is a specified interface, while JIT decisions are implementation behavior. SQL plans depend on engine, statistics and workload. Shell syntax becomes processes and descriptor relationships, not merely strings printed on a terminal.

Major capstone: C → RISC-V assembly → instruction bits → architectural trace ↔ a matching SystemVerilog/VHDL CPU subset. Compare state after each instruction, not just final output. Support caches, pipelines, hazards, interrupts, exceptions, DMA and memory ordering only after their bounded prerequisite models exist.
