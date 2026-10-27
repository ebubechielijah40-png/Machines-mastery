# Source verification — 2026-10-22

| Inspected source | Scope used | Limits |
| --- | --- | --- |
| Noam Nisan and Shimon Schocken's official [Nand2Tetris Project2: Boolean Arithmetic](https://www.nand2tetris.org/project02) | Project page's half/full adder, ripple addition, ALU and staged test descriptions | Full book Chapter2, HDL source and simulator files were not thereby inspected. No source code copied |
| Same authors' official [Project5: Computer Architecture](https://www.nand2tetris.org/project05) | Project page background and contract: connect ALU/register/memory to CPU/computer and check programs in stages | This local ISA is original8-bit/16-address, not Hack. No hardware/HDL test or full book reconstruction claimed |

The bitwise equations are derived locally from the eight-row truth table; the
adder invariant, ISA, multiplication proof, hand programs, code and fault
experiment are original instructional work. These public source pages motivate
the bottom-up progression, not evidence that our simulator is physical hardware.
No copyrighted chapter or original HDL implementation is redistributed. Source
licensing for reuse of their artifacts would require a separate review.
