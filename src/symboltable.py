#!/usr/bin/env python
class symboltable_node:
    """Defines a class Code which stores any piece of code line by line"""

    def __init__(self):
        """Initializes empty list named code"""
        self.name = ''
        self.type = ''
        self.scope = 0
        self.value = 0
        self.expr = None
        self.exprnode = None
    # def add_line(self, line):
    #     """Appends a line to the code"""
    #     self.code.append(line)

    # def print_code(self):
    #     """Prints the code line by line"""
    #     for i in range(len(self.code)):
    #         print(self.code[i])

    # def length(self):
    #     """Returns length of code"""
    #     return len(self.code)


class SymbolTable:
    """Defines a class for p which stores the element for the Node"""

    def __init__(self):
        """Initializes class TreeNode"""

        self.symbol_table = []

    def print_symbol_table(self):
        """Prints the symbol table"""
        print('\nSYMBOL TABLE')
        print("NAME  |  TYPE  |  SCOPE  |  VALUE  |  EXPR\n--------------------------------------------------")
        for i in range(len(self.symbol_table)):
            entry = self.symbol_table[i]
            print(entry.name, "\t", entry.type, "\t",
                  entry.scope, "\t ", entry.value, "\t   ", entry.expr)
            '''
            if entry.name.startswith("temp") or entry.name.startswith("label"):
                pass
            else:
                print(entry.name, "\t", entry.type, "\t", entry.scope)
            '''

    def add_node(self, symboltable_node):
        name = symboltable_node.name
        for st_node in self.symbol_table:
            if st_node.name == name:
                return False
        self.symbol_table.append(symboltable_node)
        return True

    def search_node(self, name):
        for i in range(len(self.symbol_table)):
            if self.symbol_table[i].name == name:
                return self.symbol_table[i]
        return []
    
    def search_expr(self, expr):
        for i in range(len(self.symbol_table)):
            if self.symbol_table[i].expr == expr:
                return self.symbol_table[i]
        return []
    
