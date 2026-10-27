# Inspected sources and boundaries — 2026-10-22

Original teaching/code/examples; no source passages/figures bundled. Public
availability does not assign redistribution rights. Documents below were actually
inspected, but no complete OS specification or source checkout was audited.

| ID | Source and inspected locator | Scope |
| --- | --- | --- |
| OS-SCHED | Remzi H. Arpaci-Dusseau and Andrea C. Arpaci-Dusseau, original *Operating Systems: Three Easy Pieces*, chapter7 [Scheduling: Introduction](https://pages.cs.wisc.edu/~remzi/OSTEP/cpu-sched.pdf), version1.10 visible in PDF; §§7.1–7.7, equations7.1–7.2, quantum/overhead discussion | Workload assumptions and metric/policy context. Our workload, exchange argument, algorithm and tests are original. This is a selected inspected open chapter, not a complete book reconstruction |
| OS-PAGES | Linux kernel documentation, [Page Tables](https://docs.kernel.org/mm/page_tables.html), opening VA/PFN/page-size explanation, hierarchy rationale, “MMU, TLB, and Page Faults” | Real architecture-dependent mapping/context; our8-bit/two-level teaching geometry is independently specified |
| OS-DUP | Linux man-pages project, [dup(2)](https://man7.org/linux/man-pages/man2/dup.2.html), DESCRIPTION, shared offset and dup2 atomic-replacement discussion; page identifies man-pages6.19 | Descriptor/open-file-description semantics on Linux; Python noninheritability defaults are separate |
| OS-PIPE | Linux man-pages project, [pipe(7)](https://man7.org/linux/man-pages/man7/pipe.7.html), “I/O on pipes and FIFOs” and “Pipe capacity” | Byte stream, blocking, EOF after all writers close, finite-capacity limits; no universal capacity constant assumed |
| OS-EXEC | Linux man-pages project, [execve(2)](https://man7.org/linux/man-pages/man2/execve.2.html), DESCRIPTION and replacement/argument-vector text | Program-image replacement; not a full credential/signal/dynamic-loader reconstruction |
| OS-SUBPROCESS | Python3.12 official [subprocess documentation](https://docs.python.org/3.12/library/subprocess.html), run/Popen, argv/shell distinctions, wait deadlock warning, Security Considerations | API/lifecycle and shell boundary; no complete POSIX compatibility claim |
| OS-PYFD | Python3.12 official [os documentation](https://docs.python.org/3.12/library/os.html), os.dup/os.pipe/os.set_blocking/os.read entries | Python interface and descriptor noninheritability behavior; actual local calls independently recorded |

The Open Group POSIX exec endpoint returned403, so its unseen text is not treated
as inspected. Live documentation is date-scoped; no upstream byte hash is claimed.
No production scheduler behavior, host TLB timing, physical memory content,
privilege escalation or kernel source modification was measured.
