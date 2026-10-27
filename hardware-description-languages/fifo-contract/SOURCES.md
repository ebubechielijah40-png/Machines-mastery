# HDL source and execution scopes

Inspected2026-10-23. This queue contract/implementation/vector generator is original.
It is not copied from the sources below. No full language standard, original
lecture deck or library implementation is redistributed.

- MIT6.111 Fall2017 [Lecture4 Sequential Logic](https://web.mit.edu/6.111/www/f2017/handouts/L04.pdf),
  slides10–19 and22–23, supports register sampling, min/max timing, clocked
  nonblocking assignments and simulation/synthesis distinctions. Exact root
  inspection is in the [device source record](../../hardware-electronics-mastery/device-logic/SOURCES.md).
- IEEE P1076 working-group std_logic_1164 package body, copyright2019, as shipped
  in Ubuntu ghdl-common4.1.0+dfsg-0ubuntu2: header and rising_edge implementation
  inspected directly. Its event/current/previous-state test defines the edge
  helper used by VHDL code. The bundled library marks its own Apache2.0 terms;
  those terms are not assigned to the whole educational repository. Installed
  source is available through the official GHDL/IEEE source distribution, not
  included in this project ZIP.
- GHDL4.1.0 actual --help/--version and analyze/elaborate/run commands were inspected
  by execution. The attempted online quick-start URL was unavailable through the
  reader; it is not counted as inspected. Tool behavior is supported by actual
  compiler/simulator logs, not a claimed full VHDL-standard review.
- Icarus Verilog official [command-line documentation](https://steveicarus.github.io/iverilog/usage/command_line_flags.html),
  -g2012 and simulation flag scopes inspected. Current documentation can discuss
  newer releases; observed execution is specifically12.0, with no full-language
  conformance claim.

Native tools were extracted outside the repository from official Ubuntu noble
packages and checked against the HTTPS package-index SHA256 entries. The exact
package records are retained in the root test evidence. Upstream Release
signatures were not independently verified. No tool binary is shipped with the
ZIP. On another machine, install appropriate simulator tools and put them on PATH.
The Python generator does not replace unavailable HDL execution.
