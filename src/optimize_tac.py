#!/usr/bin/env python
from symboltable import SymbolTable
from code import ThreeAddressCode

start = 0

def block_label_gen():
    global start
    block_label = f"b{start}"
    start += 1
    return block_label


def basic_blocks(three_addr_code):
    leaders = [0]
    labels = dict()
    basic_block = dict()
    label_block = dict()
    #First Pass
    for idx, line in enumerate(three_addr_code.code):
        if line[0].startswith("label_") and len(line) == 1:
            labels[line[0]] = idx
    #Second Pass
    for idx, line in enumerate(three_addr_code.code):
        if line[0] == "goto":
            leaders.append(labels.get(line[1]))   #Target of jump instruction   
            leaders.append(idx+1)                 #Instr immediately after jump instruction
        if line[0] in ["ifgotoeq", "ifgotoneq"]:
            leaders.append(labels.get(line[-1]))  #Target of jump instruction
            leaders.append(idx+1)                 #Instr immediately after jump instruction  
        if line[0] == "return":
            leaders.append(idx+1)
    leaders = list(set(leaders))
    if len(leaders) == 1:
        basic_block["b0"] = three_addr_code.code
    else:
        for idx in range(len(leaders)-1):
            label = block_label_gen()
            basic_block[label] = three_addr_code.code[leaders[idx]:leaders[idx+1]]
    label = block_label_gen()
    basic_block[label] = three_addr_code.code[leaders[-1]:]
    for bl in basic_block:
        code = basic_block[bl]
        for line in code:
            if len(line) == 1 and line[0].startswith("label_"):
                    label_block[line[0]] = bl
    return basic_block, label_block
        

def build_cfg(basic_block, label_block):
    for b in basic_block:
        print(b, basic_block[b])
    print("LABEL", label_block)
    graph = {i:{j:0 for j in basic_block} for i in basic_block}
    graph["b0"]["b0"] = 1
    for bl in basic_block:
        last_instr = basic_block[bl][-1]
        if last_instr[0] in ["ifgotoeq", "ifgotoneq", "goto"]:
            if last_instr[-1] == '':
                target_label = last_instr[1]
            else:
                target_label = last_instr[-1]
            block = label_block[target_label]
            graph[bl][block] = 1
        if last_instr[0] != "goto":
            next_block_label = "b"+str(int(bl[1])+1)
            graph[bl][next_block_label] = 1
    for label in graph:
        print(label, graph[label])

def get_all_stmt_lhs(three_addr_code, name):
    stmts = []
    for idx, line in enumerate(three_addr_code.code):
        if line[1] == name:
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
    three_addr_code.code = [three_addr_code.code[i] for i in range(n) if i not in remove]
    return three_addr_code

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
            indices = [i for i, value in enumerate(c) if value == line]
            to_remove += indices[1:]
    to_remove = list(set(to_remove))
    three_addr_code.code = [c[i] for i in range(len(c)) if i not in to_remove]
    return three_addr_code

def optimize_tac(symbol_table, three_addr_code):
    '''
    three_addr_code = pack_temps(symbol_table,three_addr_code)
    #three_addr_code.print_code()
    basic_block, label_block = basic_blocks(three_addr_code)
    build_cfg(basic_block, label_block)
    '''
    three_addr_code = common_subexpr_eliminate(three_addr_code)
    #three_addr_code = pack_temps(symbol_table, three_addr_code)
    return three_addr_code
    

