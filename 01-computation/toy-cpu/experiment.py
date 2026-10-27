import json
import platform
import sys
from cpu import CPU,instruction,multiplication_program


def main():
    cpu=CPU(multiplication_program(3,4));trace=cpu.run()
    altered=CPU(multiplication_program(3,4));altered.memory[9]=instruction('JMP',9)
    try:altered.run(100)
    except TimeoutError:status='budget exhaustion: branch at9 repeatedly jumps to9'
    else:status='unexpected termination; inspect the trace'
    print(json.dumps({'kind':'abstract software CPU model, no HDL timing/hardware claim',
        'environment':{'python':sys.version,'platform':platform.platform()},
        'program':'original 8-bit accumulator ISA, repeated addition3*4',
        'final_accumulator':cpu.accumulator,'cycles':cpu.cycles,'trace':trace,
        'fault_injection':{'changed_address':9,'old_word':instruction('JMP',2),
            'new_word':instruction('JMP',9),'outcome':status,'cycles_observed':altered.cycles,'pc':altered.pc,'memory':altered.memory}},indent=2))

if __name__=='__main__':main()
