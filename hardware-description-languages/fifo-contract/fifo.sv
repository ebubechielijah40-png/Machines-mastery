module fifo #(parameter integer DEPTH=3, WIDTH=4)
 (input logic clk, reset, push, pop,
  input logic [WIDTH-1:0] din,
  output wire [WIDTH-1:0] dout,
  output wire full, empty,
  output integer count);
  logic [WIDTH-1:0] memory [0:DEPTH-1];
  integer rd, wr;
  wire pop_fire = pop && (count > 0);
  wire push_fire = push && ((count < DEPTH) || pop_fire);
  assign full = (count == DEPTH);
  assign empty = (count == 0);
  assign dout = empty ? {WIDTH{1'b0}} : memory[rd];
  function automatic integer next_ptr(input integer pointer);
    next_ptr = (pointer == DEPTH-1) ? 0 : pointer+1;
  endfunction
  always @(posedge clk) begin
    if (reset) begin rd<=0; wr<=0; count<=0; end
    else begin
      if (push_fire) begin memory[wr]<=din; wr<=next_ptr(wr); end
      if (pop_fire) rd<=next_ptr(rd);
      case ({push_fire,pop_fire})
        2'b10: count<=count+1;
        2'b01: count<=count-1;
        default: count<=count;
      endcase
    end
  end
endmodule
