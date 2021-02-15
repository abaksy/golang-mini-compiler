"""Defines classes Code and ThreeAddressCode"""

class Code:
    """Defines a class Code which stores any piece of code line by line"""

    def __init__(self):
        """Initializes empty list named code"""
        self.code = []

    def add_line(self, line):
        """Appends a line to the code"""
        self.code.append(line)

    def print_code(self):
        """Prints the code line by line"""
        for i in range(len(self.code)):
            print(self.code[i])

    def length(self):
        """Returns length of code"""
        return len(self.code)

class ThreeAddressCode(Code):
    """Extends the class code to store 3AC"""

    def __init__(self):
        """Initializes Code as well as empty list for storing leaders in 3AC"""
        Code.__init__(self)
        self.leaders = []

    def add_leader(self, leader):
        """Inserts a leader if not already present in the list"""
        if leader not in self.leaders:
            self.leaders.append(leader)

    def append_TAC(self, tac):
        for i in range(tac.length()):
            self.add_line(tac.code[i])
        self.leaders += tac.leaders

class TreeNode:
    """Defines a class for p which stores the element for the Node"""

    def __init__(self, name, data, input_type, line_no, isLvalue = None, children = None, TAC = None):
        """Initializes class TreeNode"""

        self.name = name
        self.data = data
        self.input_type = input_type
        self.lineno = line_no

        if isLvalue is None:
            self.isLvalue = 0
        else:
            self.isLvalue = isLvalue

        if children is None:
            self.children = []
        else:
            self.children = children

        if TAC is None:
            self.TAC = ThreeAddressCode()
        else:
            self.TAC = TAC

    def print_node(self):
        print("Name:", self.name, "Data:", self.data, "Type:", self.input_type, "Is L-Value?", self.isLvalue)
        if len(self.children) != 0:
            print("Children:")
            # time.sleep(0.7)
            for child in self.children:
                if isinstance(child, TreeNode):
                    child.print_node()
                else:
                    print(child)

        if self.TAC.length() != 0:
            print("Three Address Code: ")
            self.TAC.print_code()
        print("")

