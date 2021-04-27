#!/usr/bin/env python
from symboltable import SymbolTable
from code import ThreeAddressCode

start = 0


def get_all_stmt_lhs(three_addr_code, name):
    stmts = []
    for idx, line in enumerate(three_addr_code.code):
        if len(line) == 4 and line[1] == name:
            stmts.append(idx)
    return stmts


def get_all_assignments(three_addr_code, name):
    stmts = []
    for idx, line in enumerate(three_addr_code.code):
        if line[0] in ['=', ':='] and line[2] == name and line[-1] == '':
            stmts.append(idx)
    return stmts


def pack_temps(symbol_table, three_addr_code):
    '''
    Remove all extra temporaries
    '''
    code = three_addr_code.code
    remove = list()
    for row in symbol_table.symbol_table:
        #print("FOR", row.name)
        stmts = get_all_stmt_lhs(three_addr_code, row.name)
        assignments = get_all_assignments(three_addr_code, row.name)
        try:
            if row.name.startswith("temp_"):
                #print(f"PACKING {three_addr_code.code[stmts[0]]}, {three_addr_code.code[assignments[0]]}")
                final_name = code[assignments[0]][1]
                three_addr_code.code[stmts[0]][1] = final_name
                remove.append(assignments[0])
        except:
            #print("COULD NOT PACK", stmts, assignments)
            continue
    n = len(three_addr_code.code)
    three_addr_code.code = [three_addr_code.code[i]
                            for i in range(n) if i not in remove]
    return three_addr_code

def check_line_expr(line):
    l1_flag = line[0] not in ["goto", "break", "continue"]
    l2_flag = len(line) == 4
    return l1_flag or l2_flag


def common_subexpr_eliminate(three_addr_code):
    '''
    Remove duplicate lines from Three Address Code
    Duplicates occur due to common subexpressions being repeated
    '''
    c = three_addr_code.code
    to_remove = list()
    for line in c:
        line_count = c.count(line)
        if line_count > 1:
            indices = [i for i, value in enumerate(c) if (value == line and value[0] in ['+', '-', '*', '/', ':=', '='])]
            to_remove += indices[1:]
    to_remove = list(set(to_remove))
    three_addr_code.code = [c[i] for i in range(len(c)) if i not in to_remove]
    return three_addr_code


def constant_folding(three_addr_code: ThreeAddressCode, symbol_table: SymbolTable):
    to_remove = list()
    for idx, line in enumerate(three_addr_code.code):
        if len(line) == 4:
            node1 = symbol_table.search_node(line[2])
            node2 = symbol_table.search_node(line[3])
            if node1:
                three_addr_code.code[idx][2] = node1.value
                to_remove += get_all_stmt_lhs(three_addr_code, node1.name)
            if node2:
                three_addr_code.code[idx][3] = node2.value
                to_remove += get_all_stmt_lhs(three_addr_code, node2.name)
    three_addr_code.code = [three_addr_code.code[i] for i in range(
        len(three_addr_code.code)) if i not in to_remove]
    return three_addr_code


def optimize_tac(symbol_table, three_addr_code):
    '''
    Function that performs optimizations on TAC
    '''
    three_addr_code = common_subexpr_eliminate(three_addr_code)
    print("\nAFTER COMMON SUBEXPRESSION ELIMINATION:")
    three_addr_code.print_code()
    three_addr_code = constant_folding(three_addr_code, symbol_table)
    #print("Code length: ", len(three_addr_code.code))
    print("\nAFTER CONSTANT FOLDING:")
    three_addr_code.print_code()
    #print("Code length: ", len(three_addr_code.code))
    return three_addr_code
