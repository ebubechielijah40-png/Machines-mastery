`timescale 1ns/1ps
module tb;
    logic clk = 0;
    logic reset = 1;
    logic enable = 0;
    logic [3:0] d = 0;
    wire [3:0] q;
    integer old_q, data_in, r, e;
    logic [3:0] expected;
    enabled_register dut(clk, reset, enable, d, q);
    task tick;
        #5 clk = 1;
        #1;
        #4 clk = 0;
    endtask
    initial begin
        tick();
        if (q !== 0) $fatal(1, "reset did not establish zero");
        for (old_q=0; old_q<16; old_q=old_q+1)
            for (data_in=0; data_in<16; data_in=data_in+1)
                for (r=0; r<2; r=r+1)
                    for (e=0; e<2; e=e+1) begin
                        reset=0; enable=1; d=old_q;
                        tick();
                        if (q !== old_q[3:0]) $fatal(1, "setup load failed");
                        reset=r; enable=e; d=data_in;
                        #1;
                        if (q !== old_q[3:0]) $fatal(1, "changed without rising edge");
                        if (r) expected=0;
                        else if (e) expected=data_in;
                        else expected=old_q;
                        tick();
                        if (q !== expected)
                            $fatal(1, "transition old=%0d d=%0d reset=%0d en=%0d got=%0d expected=%0d", old_q,data_in,r,e,q,expected);
                    end
        $display("PASS: 1024 transitions, synchronous reset, hold and no-edge stability");
        $finish;
    end
endmodule
