"""Class for dealing with registers in Assembly Code"""

class Registers:
    """Class for dealing with registers in Assembly Code"""

    def __init__(self):
        """Initialize member variables"""

        # Registers in MIPS are denoted by $8 to $23
        self.registers = ['$8', '$9', '$10', '$11', '$12', '$13', '$14', '$15']
        self.registers += ['$16', '$17', '$18', '$19', '$20', '$21', '$22', '$23']

        self.register_descriptor = dict((elem, 0) for elem in self.registers)

        # stores the line number where the register was last used
        self.last_use = dict((elem, -1) for elem in self.registers)

    def print_register_descriptor(self):
        """Prints register descriptor"""
        print(self.register_descriptor)

    def get_next_use(self, line_no, symbol_table):       #returns register with maximum next use
        """Gets register with maximum next use"""
        max_next_use = 0
        register = ''

        for key in self.register_descriptor:
            curr_next_use = symbol_table.next_use[self.register_descriptor[key]][0][line_no-1]
            if curr_next_use > max_next_use and self.last_use[key] < line_no:
                max_next_use = curr_next_use
                register = key
        return register

    def free_register(self, line_no):              # checks if any register is free and returns it
        """Checks if any free register is available and returns it"""
        for register in self.registers:
            if self.register_descriptor[register] == 0:
                return register

        for register in self.registers:
            # for registers used for constants
            if self.register_descriptor[register] == 1 and self.last_use[register] < line_no:
                return register

        # return 0 if no register is free
        return 0

    def save_value_from_register(self, register, symbol_table, assembly_code):
        """Save value from register to variable"""
        var = self.register_descriptor[register]
        if var in symbol_table.next_use:
            symbol_table.next_use[var][1] = 0

            line = 'la $a0, ' + var
            assembly_code.add_line(line)

            line = 'sw ' + register + ' 0($a0)'
            assembly_code.add_line(line)

        self.register_descriptor[register] = 0

    def get_empty_register(self, line_no, symbol_table, assembly_code):
        """Get Empty Register"""
        register_allocated = self.free_register(line_no)
        if register_allocated != 0:
            return register_allocated

        # register spilling case
        register = self.get_next_use(line_no, symbol_table)
        self.save_value_from_register(register, symbol_table, assembly_code)
        return register

    def get_register(self, var, symbol_table, line_no, assembly_code):
        """Get Register"""
        if var in symbol_table.next_use:
            # print var + 'hell'
            curr_reg = symbol_table.next_use[var][1]
            if curr_reg != 0:
                self.last_use[curr_reg] = line_no
                return curr_reg

            register = self.get_empty_register(line_no, symbol_table, assembly_code)
            symbol_table.next_use[var][1] = register
            self.register_descriptor[register] = var

            line = 'lw ' + register + ', ' + var
            assembly_code.add_line(line)

            self.last_use[register] = line_no
            return register

        else:
            # Allocating register to constant
            register = self.get_empty_register(line_no, symbol_table, assembly_code)
            self.register_descriptor[register] = 1
            # print var +'o'
            line = 'li ' + register + ', ' + var
            assembly_code.add_line(line)
            self.last_use[register] = line_no
            return register

    def empty_all_registers(self, symbol_table, assembly_code):
        """Empty all registers
        To be used when a block of code end"""

        for register in self.registers:
            self.save_value_from_register(register, symbol_table, assembly_code)

        # Empty register name for variables stored in symbol_table
        for var in symbol_table.next_use:
            symbol_table.next_use[var][1] = 0
