`timescale 1ns/1ps
module tb;
  logic clk=0, reset=0,push=0,pop=0;
  logic [3:0] din=0;
  wire [3:0] dout;
  wire full,empty;
  integer count;
  integer fd,status,r,pu,po,d,expected_count,expected_head;
  integer vectors=0;
  logic [3:0] stable_head;
  integer stable_count;
  fifo dut(.*);
  initial begin
    fd=$fopen("vectors.txt","r");
    if (!fd) $fatal(1,"missing vectors");
    while (!$feof(fd)) begin
      status=$fscanf(fd,"%d %d %d %d %d %d\n",r,pu,po,d,expected_count,expected_head);
      if(status!=6) $fatal(1,"malformed vector");
      clk=0;reset=r;push=pu;pop=po;din=d;#2;
      if(vectors>0 && (count!==stable_count || dout!==stable_head)) $fatal(1,"state changed without clock");
      clk=1;#2;
      if(count!==expected_count || dout!==expected_head || empty!==(expected_count==0) || full!==(expected_count==3))
        $fatal(1,"queue transition mismatch vector=%0d count=%0d expected=%0d",vectors,count,expected_count);
      stable_count=count;stable_head=dout;vectors=vectors+1;
      clk=0;#2;
    end
    $display("PASS: %0d FIFO vectors",vectors);$finish;
  end
endmodule
