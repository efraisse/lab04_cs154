import pyrtl

rf_out1 = pyrtl.WireVector(bitwidth = 32, name = 'rf_out1')
rf_out2 = pyrtl.WireVector(bitwidth = 32, name = 'rf_out2')
writeReg = pyrtl.WireVector(bitwidth = 32, name = 'writeReg')
writeData = pyrtl.WireVector(bitwidth = 32, name = 'writeData')

def update():
    ins <<= i_mem[pc]
    pc.next <<= pc + 1

    opcode <<= ins[-6:]
    rs <<= ins[-11:-6]
    rt <<= ins[-16:-11]
    rd <<= ins[-21:-16]
    funct <<= ins[0:6]
    imm <<= ins[0:16]

    control_signals = controller(opcode, funct)
    reg_dst <<= control_signals[9:10]
    branch <<= control_signals[8:9]i
    regwrite <<= control_signals[7:8]i
    alu_src <<= control_signals[5:7]
    mem_write <<= control_signals[4:5]
    mem_to_reg <<= control_signals[3:4]
    alu_op <<= control_signals[0:3]
    
    
def mux_alu_src(input1, input2, select):

    result = pyrtl.WireVector(bitwidth = 32, name = 'result')
    result <<= input2

    with select == 0:
        return input1
    with select == 1:
        return result
    with select == 2:
        result <<= imm.zero_extended(32)
        return result

def mux_reg_dst(rt, rd, reg_dst):
    with reg_dst == 0:
        return rt
    with reg_dst == 1:
        return rd

def mux_mem_to_reg(readData, aluOut, memToReg):
    with memToReg == 0:
        return aluOut
    with memToReg == 1:
        return readData

def mux_branch(pc1, addAlu, branch):
    with branch == 0:
        return pc1
    with branch == 1:
        return addAlu + pc1

def add_alu(immed, pc1):
    return immed + pc1

def alu(input_src_1, input_src_2, zero, alu_op):
    zero = 0
    with alu_op == 0:
        return input_src_1 + input_src_2, zero
    with alu_op == 1:
        return input_src_1 & input_src_2, zero
    with alu_op == 2:
        return input_src_2, zero
    with alu_op == 3:
        return input_src_1 | input_src_2, zero
    
    with alu_op == 4:
        result = input_src_1 - input_src_2:
            with result < 0:
                zero = 1
                return result, zero

            with result >= 0

                return result, zero
                
    with alu_op == 5:
        result = input_src_1 - input_src_2:
            with result == 0:
                zero = 1
                return result, zero

            with result != 0:
                return result, zero
    


def controller(opcode, funct):
    with pyrtl.conditional_assignment:
        with opcode == 0:
            with funct == 0x20:
                control_signals |= 0x280
            with funct == 0x24:
                control_signals |= 0x281
            with funct == 0x2a:
                control_signals |= 0x284
        with opcode == 0x08:
            control_signals |= 0x0a0
        with opcode == 0x0f:
            control_signals |= 0x0aa
        with opcode == 0x0d:
            control_signals |= 0x0c3
        with opcode == 0x23:
            control_signals |= 0x0a8
        with opcode == 0x2b:
            control_signals |= 0x030
        with opcode == 0x04:
            control_signals |= 0x125

    return control_signals

def cpu(pc, i_mem, d_mem, rf, ins):

    pc = pyrtl.Register(bitwidth = 32, name = 'pc');
    rf  = pyrtl.MemBlock(bitwidth = 32,  addrwidth = 32, asynchronous = True)
    d_mem = pyrtl.MemBlock(bitwidth = 32, addrwidth = 32, asynchronous = True)
    i_mem = pyrtl.MemBlock(bitwidth = 32, addrwidth = 32)

    ins = pyrtl.WireVector(bitwidth=32, name='ins')
    opcode = pyrlt.WireVector(bitwidth=6, name='opcode')
    rs = pyrtl.WireVector(bitwidth=5, name='rs')
    rt = pyrtl.WireVector(bitwidth=5, name='rd')
    rd = pyrtl.WireVector(bitwidth=5, name='rd')
    imm = pyrtl.WireVector(bitwidth=16, name='imm')
    funct = pyrtl.WireVector(bitwidth=6, name='funct')

    REG_DEST = pyrtl.WireVector(bitwidth=1, name='REG_DEST')
    BRANCH = pyrtl.WireVector(bitwidth=1, name='BRANCH')
    REG_WRITE = pyrtl.WireVector(bitwidth=1, name='REG_WRITE')
    ALU_SRC = pyrtl.WireVector(bitwidth=2, name='ALU_SRC')
    MEM_WRITE = pyrtl.WireVector(bitwidth=1, name='MEM_WRITE')
    MEM_TO_REG = pyrtl.WireVector(bitwidth=1, name='MEM_TO_REG')
    ALU_OP = pyrtl.WireVector(bitwidth=3, name='ALU_OP')

    control_signals=pyrtl.WireVector(bitwidth = 10, name='control_signals')

    read_reg_1 = pyrtl.WireVector(bitwidth = 5, name = 'read_reg_1')
    read_reg_2 = pyrtl.WireVector(bitwidth = 5, name = 'read_reg_2')
    writeReg = pyrtl.WireVector(bitwidth = 5, name = 'writeReg')
    read_data_1 = pyrtl.WireVector(bitwidth = 5, name = 'read_data_1')
    read_data_2 = pyrtl.WireVector(bitwidth = 5, name = 'read_data_2')

    address = pyrtl.wireVector(bitwidth = 32, name = 'address')
    writeData = pyrtl.wireVector(bitwidth = 32, name = 'writeData')
    readData = pyrtl.wireVector(bitwidth = 32, name = 'readData')
    dataMemory = pyrtl.wireVector(bitwidth = 32, name = 'dataMemory')
    
    opcode <<= ins[-6:]
    rs <<= ins[-11:-6]
    rt <<= ins[-16:-11]
    rd <<= ins[-21:-16]
    funct <<= ins[0:6]
    imm <<= ins[0:16]

    control_signals = controller(opcode, funct)
    REG_DST <<= control_signals[9:10]
    BRANCH <<= control_signals[8:9]
    REG_WRITE <<= control_signals[7:8]
    ALU_SRC <<= control_signals[5:7]
    MEM_WRITE <<= control_signals[4:5]
    MEM_TO_REG <<= control_signals[3:4]
    ALU_OP <<= control_signals[0:3]
 
    read_reg_1 <<= rf[rs]
    read_reg_2 <<= rf[rt]

    reg_dst_result = mux_reg_dst(rt, rd, REG_DEST)

    writeReg <<= rf[reg_dst_result]

    read_data_1 <<= read_reg_1
    read_data_2 <<= read_reg_2

    alu_src_result = (read_data_2, imm, ALU_SRC)

    alu_op_result = (rs, alu_src_result, zero, ALU_OP)

    with pyrtl.conditional_assignment:
        with MEM_WRITE == 1:
            d_mem[alu_op_result] <<= read_data_2

        with MEM_READ == 1:
            readData <<= d_mem[alu_op_result]

    mem_to_reg_result = mux_mem_to_reg(readData, alu_op_result, MEM_TO_REG)

    rf[reg_dst_result] <<= mem_to_reg_result


   #implement the branch instruction with this and then you'll be pretty much done. 







if __name__ == '__main__':



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
