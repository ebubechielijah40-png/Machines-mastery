# Problems

Easy 1: identify rd,rs1,imm in addi x2,x3,4. Easy 2: find the bit positions of rd. Easy 3: interpret immediate 0xFFF. Easy 4: explain x0. Easy 5: predict pc after two accepted instructions from zero.

Intermediate 6: derive the word for addi x1,x0,1. Intermediate 7: trace addi x5,x5,-1 from x5=0. Intermediate 8: describe why casting instruction bytes to a host integer can misread the word.

Hard 9: prove the invariant including rd=rs1 and rd=0; then describe exactly what must change for a different instruction without pretending to know its encoding.

Experimental 10: derive five boundary immediate encodings before comparing with GNU as. Keep actual object bytes and explain disagreements. Implement an independent decoder before consulting the solution.
