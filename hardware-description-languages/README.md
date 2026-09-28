# Hardware descriptions

HDL source describes a model of hardware structure and transitions. A simulator executes a model of events; a synthesizer translates a supported subset into a logic network. Elaboration resolves parameters/generics and hierarchy before those later stages. Placement/routing and physical timing/power require a target and constraints. Passing a testbench proves none of those physical properties.

Use [SystemVerilog/Verilog](systemverilog/README.md) or [VHDL](vhdl/README.md) when digital hardware gates are met. They share project specifications and comparison criteria, not blindly translated syntax. Gate → arithmetic → register → memory → ALU → datapath → controller → CPU remains linked to J-01 and the planned RISC-V capstone. Language introductions live in programming-languages-mastery; prepared RTL lives here to avoid duplicate lessons.
