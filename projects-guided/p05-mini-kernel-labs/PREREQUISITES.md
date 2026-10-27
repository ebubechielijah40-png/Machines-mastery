# Prerequisites and bridges

Complete these in order:

1. [Compile, link and inspect a C program](../../04-computer-systems/compile-link/README.md):
   distinguish source contract, object symbols and observed machine instructions.
2. [Byte-interval allocator](../p04-memory-allocator/README.md): trace ownership,
   half-open intervals and conservation before adding translation.
3. [OS mechanisms lesson](../../05-operating-systems/SELF_CONTAINED_GUIDE.md):
   derive response/turnaround/waiting and quotient/remainder address fields.
4. [Local shell](../p02-shell/README.md): launch actual processes and account for
   descriptor ownership, so the host experiment has an understood mechanism.

These links are a dependency route, not a requirement that every preceding
broad domain be complete. For this model project you need Python lists,
dictionaries, deque, dataclasses, integer arithmetic, exceptions, and unittest.
Use [the Python guide](../../programming-languages-mastery/08-python/README.md)
for syntax reference, then trace a queue and dictionary manually before coding.

Entry assessment: compute VPN/offset for 45 with page size 16; draw the q=2
trace for A(0,5), B(1,2), C(2,1); explain why a TLB hit still requires a permission
check. The worked lesson supplies each missing bridge. Python 3.12+ is sufficient;
no VM, root access, emulator or external package is needed for this bounded build.
