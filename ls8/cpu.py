"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256 # memory to hold 256 bytes 
        self.gp_register = [0] * 8 # empty general purpose register 
        self.pc = 0 # Program Counter, address of the currently executing instruction - counter for running process 

    def ram_read(self, address):
        # accepts the address to read and return the value stored there.
        return self.ram[address]

    def ram_write(self, value, address):
        # accepts a value to write, and the address to write it to.
        self.ram[address] = value

    def load(self):
        """Load a program into memory."""

        if len(sys.argv) != 2:
            print("usage: comp.py filename")
            sys.exit(1)

        try:
            # counter for loading process 
            address = 0

            run_file = sys.argv[1]

            with open(run_file) as f:
                for line in f:
                    t = line.split('#')
                    n = t[0].strip()

                    if n == '':
                        continue

                    try:
                        # change string into binary integer 
                        n = int(n, 2)
                    except ValueError:
                        print(f"Invalid number {n}")
                        sys.exit(1)

                    # adding the binary value to the ram (memory)
                    self.ram[address] = n
                    address += 1

        except FileNotFoundError:
            print(f"File not found: {sys.argv[1]}")
            sys.exit(2)

        # address = 0

        # # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000, # the slow we want to load into 
        #     0b00001000, # the value we want to load 
        #     0b01000111, # PRN R0
        #     0b00000000, # the slot we want to print 
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "MULT":
            self.gp_register[reg_a] *= self.gp_register[reg_b]
        elif op == "ADD":
            self.gp_register[reg_a] += self.gp_register[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        HLT = 0b00000001 # halt, stop the program 
        LDI = 0b10000010 # sets a specified register to a specified value
        PRN = 0b01000111 # Print numeric value stored in the given register
        MULT = 0b10100010 # multiply value at operand_a by value at operand_b and put that into slot at operand_a

        running = True 

        while running:

            instruction_register = self.ram_read(self.pc)

            operand_a = self.ram_read(self.pc + 1) # the slot we want to load into 
            operand_b = self.ram_read(self.pc + 2) # the value we want to load 

            # dynamically coding in how far to move counter (pc)
            number_of_operands = (instruction_register & 0b11000000) >> 6
            how_far_to_move_pc = number_of_operands + 1

            if instruction_register == HLT:
                running == False
                self.pc += how_far_to_move_pc 
            
            elif instruction_register == LDI:
                self.gp_register[operand_a] = operand_b
                self.pc += how_far_to_move_pc 
            
            elif instruction_register == PRN: 
                print(self.gp_register[operand_a])
                self.pc += how_far_to_move_pc

            elif instruction_register == MULT:
                # set the value at gp_register[operand_a] equal to gp_register[operand_a] * gp_register[operand_b]
                # self.gp_register[operand_a] = self.gp_register[operand_a] * self.gp_register[operand_b]
                self.alu("MULT", operand_a, operand_b)
                self.pc += how_far_to_move_pc 


	# pc += how_far_to_move_pc
            
