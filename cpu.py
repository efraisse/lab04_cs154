import pyrtl

i_mem = pyrtl.MemBlock(...)
d_mem = pyrtl.MemBlock(...)
rf    = pyrtl.MemBlock(...)

if __name__ == '__main__':

    pc = pyrtl.Register(bitwidth = 32, name = 'pc');
    opcode = pyrtl.WireVector(bitwidth = 6, name = 'opcode');
    rs = pyrtl.WireVector(bitwidth = 5, name = 'rs')
    rt = pyrtl.WireVector(bitwidth = 5, name = 'rt')
    rd = pyrtl.WireVector(bitdwith = 5, name = 'rd')
    shamt = pyrtl.WireVector(bitwidth = 5, name = 'shamt')
    funct = pyrtl.WireVector(bitwidth = 6, name = 'funct')
    REG_DST = pyrtl.WireVector(bitwidth = 1, name = 'REG_DST')
    BRANCH = pyrtl.WireVector(bitwidth = 1, name = 'BRANCH')
    REGWRITE = pyrtl.WireVector(bitwidth = 1, name = 'REGWRITE')
    ALU_SRC = pyrtl.WireVector(bitwidth = 2, name = 'ALU_SRC')
    MEM-WRITE = pyrtl.WireVector(bitwidth = 1, name = 'MEM_WRITE')
    MEM_TO_REG = pyrtl.WireVector(bitwidth = 1, name = 'MEM_TO_REG')
    ALU_OP = pyrtl.WireVector(bitwidth = 3, name = 'ALU_OP')
    instruction = pyrtl.WireVector(bitwidth = 32, name = 'instruction')
    instruction <<= memory[pc]
    memory[pc] <<= instruction
    mem[pc] = MemBlock.EnabledWrite(instruction, enable = we)



    control_signals = pyrtl.wireVector(bitwidth = 9, name = 'control_signals')
    with pyrtl.conditional_assignment:
        with op == 0x0
            with funct = 0x20
                control_signals |= 0x280
            with funct = 0x24
                control_signals |= 0x281
            with funct = 0x2A
                control_signals |= 0x284

        with op == 0x8
            control_signals |= 0x281
        
        with op == 0xf
            control_signals |= 0x0AA
        
        with op == 0xD
            control_signals |= 0x0A3

        with op == 0x23
            control_signals |= 0x0AD

        with op == 0x2b
            control_signals |= 0x036

        with op == 0x4
            control_signals |= 0x127


    """

    Here is how you can test your code.
    This is very similar to how the autograder will test your code too.

    1. Write a MIPS program. It can do anything as long as it tests the
       instructions you want to test.

    2. Assemble your MIPS program to convert it to machine code. Save
       this machine code to the "i_mem_init.txt" file.
       You do NOT want to use QtSPIM for this because QtSPIM sometimes
       assembles with errors. One assembler you can use is the following:

       https://alanhogan.com/asu/assembler.php

    3. Initialize your i_mem (instruction memory).

    4. Run your simulation for N cycles. Your program may run for an unknown
       number of cycles, so you may want to pick a large number for N so you
       can be sure that the program has "finished" its business logic.

    5. Test the values in the register file and memory to make sure they are
       what you expect them to be.

    6. (Optional) Debug. If your code didn't produce the values you thought
       they should, then you may want to call sim.render_trace() on a small
       number of cycles to see what's wrong. You can also inspect the memory
       and register file after every cycle if you wish.

    Some debugging tips:

        - Make sure your assembly program does what you think it does! You
          might want to run it in a simulator somewhere else (SPIM, etc)
          before debugging your PyRTL code.

        - Test incrementally. If your code doesn't work on the first try,
          test each instruction one at a time.

        - Make use of the render_trace() functionality. You can use this to
          print all named wires and registers, which is extremely helpful
          for knowing when values are wrong.

        - Test only a few cycles at a time. This way, you don't have a huge
          500 cycle trace to go through!

    """

    # Start a simulation trace
    sim_trace = pyrtl.SimulationTrace()

    # Initialize the i_mem with your instructions.
    i_mem_init = {}
    with open('i_mem_init.txt', 'r') as fin:
        i = 0
        for line in fin.readlines():
            i_mem_init[i] = int(line, 16)
            i += 1

    sim = pyrtl.Simulation(tracer=sim_trace, memory_value_map={
        i_mem : i_mem_init
    })

    # Run for an arbitrarily large number of cycles.
    for cycle in range(500):
        sim.step({})

    # Use render_trace() to debug if your code doesn't work.
    # sim_trace.render_trace()

    # You can also print out the register file or memory like so if you want to debug:
    # print(sim.inspect_mem(d_mem))
    # print(sim.inspect_mem(rf))

    # Perform some sanity checks to see if your program worked correctly
    assert(sim.inspect_mem(d_mem)[0] == 10)
    assert(sim.inspect_mem(rf)[8] == 10)    # $v0 = rf[8]
    print('Passed!')
