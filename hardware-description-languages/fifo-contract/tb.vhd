library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use std.textio.all;
use std.env.all;
entity tb is end entity;
architecture test of tb is
  signal clk,reset,push,pop : std_logic := '0';
  signal din,dout : unsigned(3 downto 0) := (others=>'0');
  signal full,empty : std_logic;
  signal count : natural range 0 to 3;
  function bit_value(v : integer) return std_logic is
  begin if v=0 then return '0'; else return '1'; end if; end function;
begin
  dut: entity work.fifo generic map(3,4) port map(clk,reset,push,pop,din,dout,full,empty,count);
  process
    file vectors : text open read_mode is "vectors.txt";
    variable row : line;
    variable r,pu,po,d,expected_count,expected_head : integer;
    variable stable_count,stable_head,n : natural := 0;
  begin
    while not endfile(vectors) loop
      readline(vectors,row);read(row,r);read(row,pu);read(row,po);read(row,d);
      read(row,expected_count);read(row,expected_head);
      clk<='0';reset<=bit_value(r);push<=bit_value(pu);pop<=bit_value(po);din<=to_unsigned(d,4);
      wait for 2 ns;
      if n>0 then assert count=stable_count and to_integer(dout)=stable_head
        report "state changed without clock" severity failure; end if;
      clk<='1';wait for 2 ns;
      assert count=expected_count and to_integer(dout)=expected_head
        and empty=bit_value(boolean'pos(expected_count=0))
        and full=bit_value(boolean'pos(expected_count=3))
        report "queue transition mismatch vector=" & integer'image(n) severity failure;
      stable_count:=count;stable_head:=to_integer(dout);n:=n+1;
      clk<='0';wait for 2 ns;
    end loop;
    report "PASS: " & integer'image(n) & " FIFO vectors";
    finish;
  end process;
end architecture;
