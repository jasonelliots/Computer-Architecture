"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256 # memory to hold 256 bytes 
        self.gp_register = [0] * 8 # empty general purpose register 
        self.pc = 0 # Program Counter, address of the currently executing instruction - counter for running process 
        self.sp = 7 

    def ram_read(self, address):
        # accepts the address to read and return the value stored there.
        return self.ram[address]

    def ram_write(self, value, address):
        # accepts a value to write, and the address to write it to.
        self.ram[address] = value

    def push_value(self, value):
        # Decrement SP
        self.gp_register[self.sp] -= 1

        # Copy the value to the SP address
        top_of_stack_addr = self.gp_register[self.sp]
        self.ram[top_of_stack_addr] = value

    def pop_value(self):
        # Get the top of stack addr
        top_of_stack_addr = self.gp_register[self.sp]

        # Get the value at the top of the stack
        value = self.ram[top_of_stack_addr]

        # Increment the SP
        self.gp_register[self.sp] += 1

        return value

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
        PUSH = 0b01000101
        POP = 0b01000110
        CALL = 0b01010000
        RET = 0b00010001
        ADD = 0b10100000

        running = True 

        while running:
     
            # returns the value in ram at the pc address 
            instruction_register = self.ram_read(self.pc)

            operand_a = self.ram_read(self.pc + 1) # the slot we want to load into 
            operand_b = self.ram_read(self.pc + 2) # the value we want to load 

            # dynamically coding in how far to move counter (pc)
            number_of_operands = (instruction_register & 0b11000000) >> 6
            how_far_to_move_pc = number_of_operands + 1

            print(bin(instruction_register), 'ir')

            if instruction_register == HLT:
                running = False
                # self.pc += how_far_to_move_pc 
            
            elif instruction_register == LDI:
                self.gp_register[operand_a] = operand_b
                self.pc += how_far_to_move_pc 

                print(f'this is ldi{self.gp_register[operand_a]}')
            
            elif instruction_register == PRN: 
                print(self.gp_register[operand_a])
                self.pc += how_far_to_move_pc

            elif instruction_register == MULT:
                # set the value at gp_register[operand_a] equal to gp_register[operand_a] * gp_register[operand_b]
                # self.gp_register[operand_a] = self.gp_register[operand_a] * self.gp_register[operand_b]
                self.alu("MULT", operand_a, operand_b)
                self.pc += how_far_to_move_pc 

            elif instruction_register == ADD:
                # set the value at gp_register[operand_a] equal to gp_register[operand_a] * gp_register[operand_b]
                # self.gp_register[operand_a] = self.gp_register[operand_a] * self.gp_register[operand_b]
                self.alu("ADD", operand_a, operand_b)
                self.pc += how_far_to_move_pc 

            elif instruction_register == PUSH:
                # Decrement SP - stack pointer 
                self.gp_register[self.sp] -= 1

                # Get the reg num to push

                # Get the value to push
                value = self.gp_register[operand_a]

                # Copy the value to the SP address - corresponds to an index in ram 
                top_of_stack_addr = self.gp_register[self.sp]
                self.ram[top_of_stack_addr] = value

                self.pc += how_far_to_move_pc

                print(f'this is push{self.gp_register[operand_a]}')

            elif instruction_register == POP:
                # Get reg to pop into

                # Get the top of stack addr - corresponds to index in ram 
                top_of_stack_addr = self.gp_register[self.sp]

                # Get the value at the top of the stack
                value = self.ram[top_of_stack_addr]

                # Store the value in the register
                self.gp_register[operand_a] = value

                # Increment the SP
                self.gp_register[self.sp] += 1

                self.pc += how_far_to_move_pc

                print(f'this is pop{self.gp_register[operand_a]}')

            elif instruction_register == RET:
                # pop the return address off the stack
                top_of_stack_add = self.gp_register[self.sp]
              
                return_address = self.ram[top_of_stack_add]
                self.gp_register[self.sp] += 1
                # store in the PC
                self.pc = return_address

                # self.pc = self.ram[self.sp]
                # self.sp += 1
            
            elif instruction_register == CALL:

                # return_address = self.pc + 2
                # self.sp -= 1
                # register = self.ram[self.pc + 1]
                # self.ram[self.sp] = return_address
                # self.pc = self.gp_register[register]
                # print(self.gp_register)
                # # Compute the return addr
                # return_addr = self.pc + 2

                # # Push return addr on stack
                # self.push_value(return_addr)

                # # Get the value from the operand reg
                # reg_num = self.ram[self.pc + 1]
                # value = self.gp_register[reg_num]

                # # Set the pc to that value
                # self.pc = value

                # print("sp", self.sp)
                # print("pc", self.pc)
                # print("reg", self.gp_register)

                # push command after CALL onto the stack
                
                return_address = self.pc + 2
              
                # push if on the stack
                # decrement stack pointer
                self.gp_register[self.sp] -= 1
                top_of_stack_add = self.gp_register[self.sp]
                # put return address on the stack
                self.ram[top_of_stack_add] = return_address
                # set the PC to the subroutine address
                subroutine_address = self.gp_register[operand_a]
                self.pc = subroutine_address



            
