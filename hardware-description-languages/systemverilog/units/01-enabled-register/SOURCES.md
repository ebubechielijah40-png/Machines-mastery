# Evidence

[SOURCE] [AMD UG901 Always Procedures](https://docs.amd.com/r/en-US/ug901-vivado-synthesis/Always-Procedures), 2026.1 page, combinational and flip-flop process examples; [Icarus command flags](https://steveicarus.github.io/iverilog/usage/command_line_flags.html), SystemVerilog generation selection; [Yosys Verilog support](https://yosyshq.readthedocs.io/projects/yosys/en/latest/using_yosys/verilog.html), supported constructs and synthesis limitations. Inspected 2026-09-27. Full IEEE scheduling standard not locally inspected; no comprehensive scheduling tutorial is claimed.

[EXPLANATION/DERIVED] The four-bit synchronous-reset contract, diagrams, priority proof, RTL, testbench and mutant are original teaching work. Actual Icarus simulation checks the bounded event behavior; no synthesis or hardware result is inferred.
