library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
entity fifo is
  generic (DEPTH : positive := 3; WIDTH : positive := 4);
  port (clk, reset, push, pop : in std_logic;
        din : in unsigned(WIDTH-1 downto 0);
        dout : out unsigned(WIDTH-1 downto 0);
        full, empty : out std_logic;
        count_out : out natural range 0 to DEPTH);
end entity;
architecture rtl of fifo is
  type memory_type is array (0 to DEPTH-1) of unsigned(WIDTH-1 downto 0);
  signal memory : memory_type;
  signal rd, wr : natural range 0 to DEPTH-1;
  signal count : natural range 0 to DEPTH;
  function next_ptr(pointer : natural) return natural is
  begin
    if pointer=DEPTH-1 then return 0; else return pointer+1; end if;
  end function;
begin
  full <= '1' when count=DEPTH else '0';
  empty <= '1' when count=0 else '0';
  dout <= (others=>'0') when count=0 else memory(rd);
  count_out <= count;
  process(clk)
    variable take_pop, take_push : boolean;
  begin
    if rising_edge(clk) then
      if reset='1' then rd<=0; wr<=0; count<=0;
      else
        take_pop := pop='1' and count>0;
        take_push := push='1' and (count<DEPTH or take_pop);
        if take_push then memory(wr)<=din; wr<=next_ptr(wr); end if;
        if take_pop then rd<=next_ptr(rd); end if;
        if take_push and not take_pop then count<=count+1;
        elsif take_pop and not take_push then count<=count-1;
        end if;
      end if;
    end if;
  end process;
end architecture;
