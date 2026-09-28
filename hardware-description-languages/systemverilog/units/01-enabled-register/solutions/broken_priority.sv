`timescale 1ns/1ps
module enabled_register (
    input logic clk, reset, enable,
    input logic [3:0] d,
    output logic [3:0] q
);
    always_ff @(posedge clk) begin
        if (enable) q <= d;
        else if (reset) q <= 4'b0000;
    end
endmodule
