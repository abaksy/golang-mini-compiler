#!/usr/bin/python

from code import TreeNode
from code import ThreeAddressCode
from lexer import tokens
from random import randint
from symbol_table import SymbolTable
from symbol_table import SymbolTableNode


import logging
import ply.lex as lex
import ply.yacc as yacc
import sys

from code import Code
three_addr_code = ThreeAddressCode()
assembly_code = Code()

parsed = []
symbol_table = SymbolTable()
var_list = []


generated = {'temp': [], 'scope': ['scope_0'], 'label': [], 'str_list': []}

def gen(s):
    '''
    Generate a new label for a scope or a string identifier when asked to
    This is used for maintaining scope in our symbol table
    '''
    if s not in generated.keys():
        generated[s] = []
    temp = s + '_' + str(len(generated[s]))
    generated[s] += [temp]
    return temp

def print_error(err, lno):
    if lno != -1:
        print("*** Error on line " + str(lno) + ": " + err + "! ***")
    else:
        print("*** Error: " + err + "! ***")
    sys.exit(1)

def check_variable(TreeNode):
    # Return 2 values. first is the name for the variable, second is 0 if variable not found
    if TreeNode.isLvalue == 1:
        if TreeNode.data not in generated['temp']:
            name = symbol_table.search_identifier(TreeNode.data)
            if name == False:
                name = symbol_table.search_function(TreeNode.data)
                if name == False:
                    print_error("Variable " + TreeNode.data + " is undefined", TreeNode.lineno)
                    return TreeNode
                else:
                    return name
            else:
                newNode = SymbolTableNode(name, TreeNode.input_type)
                symbol_table.add_var(newNode)
                if TreeNode.children == []:
                    return name
                else:
                    return name + '[' + TreeNode.children + ']'
        else:
            newNode = SymbolTableNode(TreeNode.data, TreeNode.input_type)
            symbol_table.add_var(newNode)
            return TreeNode.data
    else:
        if TreeNode.input_type != 'STRING':
            return TreeNode.data
        else:
            TreeNode.print_node()
            return TreeNode.data

precedence = (
    ('left','IDENTIFIER'),
    ('right','ASSIGN_OP'),
    ('left','COMMA'),
    ('left','LSQUARE'),
    ('left','RSQUARE'),
    ('left','LCURLY'),
    ('left','RCURLY'),
    ('left','DDD'),
    ('left','DOT'),
    ('left','SEMICOLON'),
    ('left','COLON'),
    ('left','SINGLE_QUOTES'),
    ('left','DOUBLE_QUOTES'),
    ('left','DECIMAL_LIT'),
    ('left','OCTAL_LIT'),
    ('left','HEX_LIT'),
    ('left','FLOAT_LIT'),
    ('left','STRING_LIT'),
    ('left','NEWLINE'),
    ('left','BREAK'),
    ('left','CONTINUE'),
    ('left','RETURN'),
    ('left','RROUND'),
    ('left','LROUND'),
    ('left', 'OR_OR'),
    ('left', 'AMP_AMP'),
    ('left', 'EQ_EQ', 'NOT_EQ','LT','LT_EQ','GT','GT_EQ'),
    ('left', 'PLUS', 'MINUS','OR','CARET'),
    ('left', 'STAR', 'DIVIDE','MODULO','AMP','AND_OR','LS','RS'),
)


'''
General Rule for writing a ply YACC rule

p is a variable of type yacc.YaccProduction
p.slice holds the matched terminals and non-terminals in a string

p[0] is of type None (as it is the LHS of the production), so we assign to it  various values
to make it not None and hence build the syntax tree as 
each production is run through one at a time

Whenever a block or a function starts, create a new scope by calling the gen() function

If needed, p[0] can either be assigned simply to another non-terminal symbol on the left 
Or we can create a tree Node and assign it to p[0] (useful for things like variable declarations etc.)

Nodes of the AST are stored in the TreeNode class objects
Nodes of the Symbol Table are stored in the SymbolTable class objects
'''
def p_SourceFile(p):
    '''SourceFile : PACKAGE IDENTIFIER SEMICOLON ImportDeclList TopLevelDeclList
    '''
    parsed.append(p.slice)
    # TODO: Ignoring package name and Imports for now
    p[0] = p[5]
    return

def p_ImportDeclList(p):
    '''ImportDeclList : ImportDecl SEMICOLON ImportDeclList
                      | empty
    '''
    parsed.append(p.slice)
    # TODO: Ignoring Imports for now
    return

def p_TopLevelDeclList(p):
    '''TopLevelDeclList : TopLevelDecl SEMICOLON TopLevelDeclList
                        | empty
    '''
    parsed.append(p.slice)
    if len(p) == 4:
        if p[3] != None:
            p[0] = TreeNode('TopLevelDeclList', 0, 'INT', p.linespan(1)[0] - numLines, 0, [p[1]] + p[3].children)
        else:
            p[0] = TreeNode('TopLevelDeclList', 0, 'INT', p.linespan(1)[0] - numLines, 0, [p[1]])
    return

def p_TopLevelDecl(p):
    '''TopLevelDecl : Declaration
                    | FunctionDecl
    '''
    parsed.append(p.slice)
    p[0] = p[1]
    return

def p_ImportDecl(p):
    '''ImportDecl : IMPORT LROUND ImportSpecList RROUND
                  | IMPORT ImportSpec
    '''
    parsed.append(p.slice)
    # TODO: Ignoring Imports for now
    return

def p_ImportSpecList(p):
    '''ImportSpecList : ImportSpec SEMICOLON ImportSpecList
                      | empty
    '''
    parsed.append(p.slice)
    # TODO: Ignoring Imports for now
    return

def p_ImportSpec(p):
    '''ImportSpec : DOT string_lit
                  | IDENTIFIER string_lit
                  | empty string_lit
    '''
    parsed.append(p.slice)
    # TODO: Ignoring Imports for now
    return

def p_Block(p):
    '''Block : LCURLY ScopeStart StatementList ScopeEnd RCURLY
    '''
    parsed.append(p.slice)
    p[0] = p[3]
    p[0].data = p[2].data
    p[0].name = 'Block'
    return

def p_ScopeStart(p):
    '''ScopeStart : empty
    '''
    parsed.append(p.slice)
    symbol_table.add_scope(gen('scope'))
    p[0] = TreeNode('ScopeStart', symbol_table.current_scope, 'None', p.linespan(1)[0] - numLines)
    return

def p_ScopeEnd(p):
    '''ScopeEnd : empty
    '''
    parsed.append(p.slice)
    symbol_table.end_scope()
    return

def p_StatementList(p):
    '''StatementList : Statement SEMICOLON StatementList
                     | empty
    '''
    parsed.append(p.slice)
    if len(p) == 4:
        p[0] = TreeNode('StatementList', 0, 'INT', p.linespan(1)[0] - numLines, 0, [p[1].data] + p[3].children)
    else:
        p[0] = TreeNode('StatementList', 0, 'INT', p.linespan(1)[0] - numLines)
    return

def p_Statement(p):
    '''Statement : Declaration
                 | SimpleStmt
                 | ReturnStmt
                 | Block
                 | IfStmt
                 | SwitchStmt
                 | ForStmt
                 | BreakStmt
                 | ContinueStmt
                 | GotoStmt
                 | PrintIntStmt
                 | PrintStrStmt
    '''
    parsed.append(p.slice)
    p[0] = p[1]
    p[0].name = 'Statement'
    return

def p_PrintIntStmt(p):
    '''PrintIntStmt : PRINTLN LROUND IDENTIFIER RROUND
                    | PRINTLN LROUND int_lit RROUND
    '''
    if hasattr(p[3], 'name') and p[3].name == 'int_lit':
        p[0] = p[3]
        # p[0].isLvalue = 0
    else:
        p[0] = TreeNode('IDENTIFIER', p[3], 'INT', p.linespan(1)[0] - numLines, 1, [])
    p[0].name = 'PrintIntStmt'
    return

def p_PrintStrStmt(p):
    '''PrintStrStmt : PRINTLN LROUND string_lit RROUND
    '''
    p[0] = p[3]
    name = symbol_table.current_scope + '_' + gen('str_list')
    parametersNode = SymbolTableNode(p[3].data, p[3].input_type)
    newNode = SymbolTableNode(name, p[3].input_type, parameters = [parametersNode])
    symbol_table.add_var(newNode)
    p[0].name = 'PrintStrStmt'
    return

def p_Declaration(p):
    '''Declaration : ConstDecl
                   | TypeDecl
                   | VarDecl
    '''
    parsed.append(p.slice)
    p[0] = p[1]
    p[0].name = 'Declaration'
    return

def p_ConstDecl(p):
    '''ConstDecl : CONST LROUND ConstSpecList RROUND
                 | CONST ConstSpec
    '''
    parsed.append(p.slice)
    return

def p_ConstSpecList(p):
    '''ConstSpecList : empty
                     | ConstSpecList ConstSpec SEMICOLON
    '''
    parsed.append(p.slice)
    return

def p_ConstSpec(p):
    '''ConstSpec : IDENTIFIER
                 | IdentifierList
                 | IDENTIFIER EQ Expression
                 | IdentifierList EQ ExpressionList
                 | IDENTIFIER Type EQ Expression
                 | IdentifierList Type EQ ExpressionList
    '''
    parsed.append(p.slice)
    return

def p_IdentifierList(p):
    '''IdentifierList : IDENTIFIER COMMA IdentifierBotList
    '''
    parsed.append(p.slice)
    node = TreeNode('IDENTIFIER', p[1], 'INT', p.linespan(1)[0] - numLines, 1)
    p[0] = TreeNode('IdentifierList', 0, 'None', p.linespan(1)[0] - numLines, 0, [node] + p[3].children)
    return

def p_IdentifierBotList(p):
    '''IdentifierBotList : IDENTIFIER COMMA IdentifierBotList
                         | IDENTIFIER
    '''
    parsed.append(p.slice)
    if len(p) == 2:
        node = TreeNode('IDENTIFIER', p[1], 'INT', p.linespan(1)[0] - numLines, 1)
        p[0] = TreeNode('IdentifierBotList', 0, 'None', p.linespan(1)[0] - numLines, 0, [node])
    elif len(p) == 4:
        node = TreeNode('IDENTIFIER', p[1], 'INT', p.linespan(1)[0] - numLines, 1)
        p[0] = TreeNode('IdentifierBotList', 0, 'None', p.linespan(1)[0] - numLines, 0, [node] + p[3].children)
    return


def p_ExpressionList(p):
    '''ExpressionList : Expression COMMA ExpressionBotList
    '''
    parsed.append(p.slice)
    p[0] = TreeNode('ExpressionList', 0, 'INT', p.linespan(1)[0] - numLines, 0, [p[1]] + p[3].children)
    return

def p_ExpressionBotList(p):
    '''ExpressionBotList : Expression COMMA ExpressionBotList
                         | Expression
    '''
    parsed.append(p.slice)
    if len(p) == 2:
        p[0] = TreeNode('ExpressionBotList', 0, 'INT', p.linespan(1)[0] - numLines, 0, [p[1]])
    elif len(p) == 4:
        p[0] = TreeNode('ExpressionBotList', 0, 'INT', p.linespan(1)[0] - numLines, 0, [p[1]] + p[3].children)
    return

def p_TypeDecl(p):
    '''TypeDecl : TYPE TypeSpecTopList
    '''
    parsed.append(p.slice)
    return

def p_TypeSpecTopList(p):
    '''TypeSpecTopList : TypeSpec
                       | LROUND TypeSpecList RROUND
    '''
    parsed.append(p.slice)
    return

def p_TypeSpecList(p):
    '''TypeSpecList : empty
                    | TypeSpecList TypeSpec SEMICOLON
    '''
    parsed.append(p.slice)
    return

def p_TypeSpec(p):
    '''TypeSpec : AliasDecl
                | TypeDef
    '''
    parsed.append(p.slice)
    return

def p_AliasDecl(p):
    '''AliasDecl : IDENTIFIER EQ Type
    '''
    parsed.append(p.slice)
    return

def p_TypeDef(p):
    '''TypeDef : IDENTIFIER Type
    '''
    parsed.append(p.slice)
    return

def p_Type(p):
    '''Type : TypeLit
            | StandardTypes
            | LROUND Type RROUND
    '''
    parsed.append(p.slice)
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]
    p[0].name = 'Type'
    return

def p_StandardTypes(p):
    '''StandardTypes : PREDEFINED_TYPES
    '''
    parsed.append(p.slice)
    p[0] = TreeNode('StandardTypes', p[1], 'NONE', p.linespan(1)[0] - numLines)
    return

def p_TypeLit(p):
    '''TypeLit : ArrayType
               | StructType
               | FunctionType
               | PointerType
    '''
    parsed.append(p.slice)
    p[0] = p[1]
    p[0].name = 'TypeLit'
    return

def p_PointerType(p):
    '''PointerType : STAR Type
    '''
    parsed.append(p.slice)
    return

def p_ArrayType(p):
    '''ArrayType : LSQUARE ArrayLength RSQUARE Type
    '''
    parsed.append(p.slice)
    p[0] = TreeNode('ArrayType', p[2].data, p[4].data, p.linespan(1)[0] - numLines)
    return

def p_ArrayLength(p):
    '''ArrayLength : Expression
    '''
    parsed.append(p.slice)
    p[0] = p[1]
    p[0].name = 'ArrayLength'
    return

def p_StructType(p):
    '''StructType : STRUCT LCURLY FieldDeclList RCURLY
    '''
    parsed.append(p.slice)
    return

def p_FieldDeclList(p):
    '''FieldDeclList : empty
                     | FieldDeclList FieldDecl SEMICOLON
    '''
    parsed.append(p.slice)
    return

def p_FieldDecl(p):
    '''FieldDecl : IdentifierList Type TagTop
                 | IDENTIFIER Type TagTop
    '''
    parsed.append(p.slice)
    return

def p_TagTop(p):
    '''TagTop : empty
              | Tag
    '''
    parsed.append(p.slice)
    return

def p_Tag(p):
    '''Tag : string_lit
    '''
    parsed.append(p.slice)
    return

def p_FunctionType(p):
    '''FunctionType : FUNC Signature
    '''
    parsed.append(p.slice)
    return

def p_Signature(p):
    '''Signature : Parameters
                 | Parameters Result
    '''
    parsed.append(p.slice)
    p[0] = p[1]
    p[0].name = 'Signature'
    s = 'scope_' + str(len(generated['scope']))
    symbol_table.new_scope(s)
    for child in p[1].children:
        symbol_table.add_identifier(child, s)
        newNode = SymbolTableNode(s + '_' + child.data, child.input_type)
        symbol_table.add_var(newNode, s)
    # symbol_table.print_symbol_table()

    if len(p) == 2:
        p[0].input_type = TreeNode('Result', 0, 'None', p.linespan(1)[0] - numLines)
    else:
        p[0].input_type = p[2]
    return

def p_Result(p):
    '''Result : Parameters
              | Type
    '''
    parsed.append(p.slice)
    if p[1].name == 'Type':
        p[0] = TreeNode('Result', 1, 'None', p.linespan(1)[0] - numLines, 0, [p[1]])
    else:
        p[0] = p[1]
        p[0].name = 'Result'
    return

def p_Parameters(p):
    '''Parameters : LROUND RROUND
                  | LROUND ParameterList RROUND
    '''
    parsed.append(p.slice)
    if len(p) == 3:
        p[0] = TreeNode('Parameters', 0, 'None', p.linespan(1)[0] - numLines)
    else:
        p[0] = p[2]
        p[0].name = 'Parameters'
    return

def p_ParameterList(p):
    '''ParameterList : ParameterDecl
                     | ParameterList COMMA ParameterDecl
    '''
    parsed.append(p.slice)
    if len(p) == 2:
        p[0] = p[1]
        p[0].name = 'ParameterList'
    elif len(p) == 4:
        p[0] = TreeNode('ParameterList', p[1].data + p[3].data, 'None', p.linespan(1)[0] - numLines, 0, p[1].children + p[3].children)
    return

def p_ParameterDecl(p):
    '''ParameterDecl : IdentifierList Type
                     | IDENTIFIER Type
                     | Type
    '''
    parsed.append(p.slice)
    p[0] = TreeNode('ParameterDecl', 0, 'None', p.linespan(1)[0] - numLines)
    if len(p) == 3:
        if hasattr(p[1], 'name') and  p[1].name == 'IdentifierList':
            for node in p[1].children:
                p[0].data += 1
                node.input_type = p[2].data
                p[0].children += [node]
        else:
            node = TreeNode('IDENTIFIER', p[1], p[2].data, p.linespan(1)[0] - numLines, 1)
            p[0].data += 1
            p[0].children += [node]
    else:
        p[0].data += 1
        p[0].children += [p[1]]
    return

def p_VarDecl(p):
    '''VarDecl : VAR VarSpecTopList
    '''
    parsed.append(p.slice)
    p[0] = p[2]
    p[0].name = 'VarDecl'
    return

def p_VarSpecTopList(p):
    '''VarSpecTopList : VarSpec
                      | LROUND VarSpecList RROUND
    '''
    parsed.append(p.slice)
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]
    p[0].name = 'VarSpecTopList'
    return

def p_VarSpecList(p):
    '''VarSpecList : empty
                   | VarSpecList VarSpec SEMICOLON
    '''
    return

def p_VarSpec(p):
    '''VarSpec : IDENTIFIER Type
               | IDENTIFIER EQ Expression
               | IDENTIFIER Type EQ Expression
               | IdentifierList Type
               | IdentifierList EQ ExpressionList
               | IdentifierList Type EQ ExpressionList
    '''
    # Insert into symbol table
    p[0] = TreeNode('VarSpec', 0, 'NONE', p.linespan(1)[0] - numLines, )
    if hasattr(p[1], 'name') and  p[1].name == 'IdentifierList':
        zero_val = TreeNode('decimal_lit', 0, 'INT', p.linespan(1)[0] - numLines, )
        # l1 = len(p[1].children)
        # if len(p) == 3:
        #     expr_list = TreeNode('Expr_List', 0, 'NONE', 0, [zero_val] * l1)
        # elif len(p) == 4:
        #     expr_list = p[3]
        # elif len(p) == 5:
        #     expr_list = p[4]
        # l2 = len(expr_list.children)
        # p[0].TAC.append_TAC(expr_list.TAC)
        # p[0].TAC.append_TAC(p[1].TAC)
        # if l1 == l2:
        #     for i in range(l1):
        #         p[0].TAC.add_line(['=', p[1].children[i], expr_list.children[i].data, ''])
        # else:
        #     print_error("Variable Declaration mismatch: " + str(l1) + " identifier(s) but " + str(l2) + " value(s)")

    else:
        p[1] = TreeNode('IDENTIFIER',p[1],'INT', p.linespan(1)[0] - numLines, 1)
        if p[2].input_type != 'NONE':
            # array case
            # p[2].print_node()
            if symbol_table.add_identifier(p[1], size = p[2].data) == False:
                print_error("Unable to add to SymbolTable", -1)
                return
            name = symbol_table.search_identifier(p[1].data)
            newNode = SymbolTableNode(name, p[1].input_type,size = p[2].data)
            symbol_table.add_var(newNode)
        p[0] = TreeNode('VarSpec',p[1].data,'INT', p.linespan(1)[0] - numLines)
        # expr = TreeNode('Expr', 0, 'NONE')
        # if len(p) == 4:
            # expr = p[3]
            # p[0].TAC.append_TAC(p[3].TAC)
            # p[0].TAC.add_line(['=', check_variable(p[1]), check_variable(expr), ''])
        # elif len(p) == 5:
            # expr = p[4]
            # p[0].TAC.append_TAC(p[4].TAC)
            # p[0].TAC.add_line(['=', check_variable(p[1]), check_variable(expr), ''])
    return

def p_FunctionDecl(p):
    '''FunctionDecl : FUNC FunctionName Signature
                    | FUNC FunctionName Signature FunctionBody
    '''
    parsed.append(p.slice)
    # symbol_table.print_symbol_table()
    p[0] = TreeNode('FunctionDecl', 0, 'INT', p.linespan(1)[0] - numLines)
    symbol_table.add_function(p[2].data, p[3].input_type, p[3].children)
    if len(p) == 5:
        noOfParams = 0
        for f in symbol_table.symbol_table[symbol_table.current_scope]['functions']:
            if f.name == p[2].data:
                noOfParams = len(f.parameters)
    return

def p_FunctionName(p):
    '''FunctionName : IDENTIFIER
    '''
    parsed.append(p.slice)
    p[0] = TreeNode('FunctionName', p[1], 'INT', p.linespan(1)[0] - numLines, 1)
    return

def p_FunctionBody(p):
    '''FunctionBody : Block
    '''
    parsed.append(p.slice)
    p[0] = p[1]
    p[0].name = 'FunctionBody'
    return

def p_SimpleStmt(p):
    '''SimpleStmt : Expression
                  | Assignment
                  | ShortVarDecl
                  | IncDecStmt
    '''
    parsed.append(p.slice)
    p[0] = p[1]
    p[0].name = 'SimpleStmt'
    return

def p_IncDecStmt(p):
    '''IncDecStmt : Expression PLUS_PLUS
                  | Expression MINUS_MINUS
    '''
    parsed.append(p.slice)
    one_val = TreeNode('IncDecStmt', '1', 'INT', p.linespan(1)[0] - numLines)
    p[0] = p[1]
    if p[1].isLvalue == 1:
        if p[2] == '++':
            pass
            #p[0].TAC.add_line(['+', check_variable(p[1]), check_variable(p[1]), one_val.data])
        else:
            pass
            #p[0].TAC.add_line(['-', check_variable(p[1]), check_variable(p[1]), one_val.data])
    else:
        print_error("Lvalue required", p.linespan(1)[0] - numLines)
    p[0].name = 'IncDecStmt'
    return

def p_ShortVarDecl(p):
    '''ShortVarDecl : ExpressionList ASSIGN_OP ExpressionList
                    | Expression ASSIGN_OP Expression
    '''
    parsed.append(p.slice)
    # TODO: Add in symbol table
    p[0] = TreeNode('ShortVarDecl', 0, 'INT', p.linespan(1)[0] - numLines)
    if p[1].name == 'ExpressionList':
        l1 = len(p[1].children)
        l2 = len(p[3].children)
        if l1 == l2:
            for i in range(l1):
                if p[1].children[i].isLvalue == 0:
                    print_error("Lvalue required", p.linespan(1)[0] - numLines)
                    return
                else:
                    if symbol_table.add_identifier(p[1].children[i]) == False:
                        print_error("Unable to add to SymbolTable", -1)
                        return
        else:
            print_error("Variable Declaration mismatch: " + str(l1) + " identifier(s) but " + str(l2) + " value(s)", p.linespan(1)[0] - numLines)

    elif p[1].name == 'Expression':
        if p[1].isLvalue == 0:
            print_error("Lvalue required", p.linespan(1)[0] - numLines)
            return
        else:
            if symbol_table.add_identifier(p[1]) == False:
                print_error("Unable to add to SymbolTable", -1)
                return
    return

def p_Assignment(p):
    '''Assignment : ExpressionList assign_op ExpressionList
                  | Expression assign_op Expression
    '''
    parsed.append(p.slice)
    p[0] = TreeNode('Assignment', 0, 'INT', p.linespan(1)[0] - numLines)
    if p[1].name == 'ExpressionList':
        l1 = len(p[1].children)
        l2 = len(p[3].children)
        if l1 == l2:
            for i in range(l1):
                if p[1].children[i].isLvalue == 0:
                    print_error("Lvalue required", p.linespan(1)[0] - numLines)
                    return
                else:
                    if symbol_table.search_identifier(p[1].children[i].data) == False and p[1].children[i].data not in generated['temp']:
                        print_error("Variable " + p[1].children[i].data + " is undefined", p.linespan(1)[0] - numLines)
                        return
                    if p[3].children[i].isLvalue == 1 and symbol_table.search_identifier(p[3].children[i].data) == False and p[3].children[i].data not in generated['temp']:
                        print_error("Variable " + p[3].children[i].data + " is undefined", p.linespan(1)[0] - numLines)
                        return
        else:
            print_error("Variable Declaration mismatch: " + str(l1) + " identifier(s) but " + str(l2) + " value(s)",  p.linespan(1)[0] - numLines)

    elif p[1].name == 'Expression':
        if p[1].isLvalue == 0:
            print_error("Lvalue required", p.linespan(1)[0] - numLines)
            return
        else:
            if symbol_table.search_identifier(p[1].data) == False and p[1].data not in generated['temp']:
                print_error("Variable " + p[1].data + " is undefined", p.linespan(1)[0] - numLines)
                return
            if p[3].isLvalue == 1 and symbol_table.search_identifier(p[3].data) == False and p[3].data not in generated['temp']:
                print_error("Variable " + p[3].data + " is undefined", p.linespan(1)[0] - numLines)
                return
    return

def p_assign_op(p):
    '''assign_op : EQ
                 | PLUS_EQ
                 | MINUS_EQ
                 | OR_EQ
                 | CARET_EQ
                 | STAR_EQ
                 | DIVIDE_EQ
                 | MODULO_EQ
                 | LS_EQ
                 | RS_EQ
                 | AMP_EQ
                 | AND_OR_EQ
    '''
    parsed.append(p.slice)
    p[0] = TreeNode('assign_op', p[1], 'OPERATOR', p.linespan(1)[0] - numLines)
    return

def p_IfStmt(p):
    '''IfStmt : IF Expression Block
              | IF Expression Block ELSE elseTail
    '''
    parsed.append(p.slice)
    if len(p) == 4:
        l1 = gen('label')
        p[0] = TreeNode('IfStmt', 0, 'INT', p.linespan(1)[0] - numLines)
    if len(p) == 6:
        l1 = gen('label')
        l2 = gen('label')
        p[0] = TreeNode('IfStmt', 0, 'INT', p.linespan(1)[0] - numLines)
    return

def p_elseTail(p):
    '''elseTail : IfStmt
                | Block
    '''
    parsed.append(p.slice)
    p[0] = p[1]
    p[0].name = 'elseTail'
    return

def p_SwitchStmt(p):
    '''SwitchStmt : ExprSwitchStmt
    '''
    parsed.append(p.slice)
    p[0] = TreeNode('SwitchStmt', 0, 'INT', p.linespan(1)[0] - numLines, 0, [])
    return

def p_ExprSwitchStmt(p):
    '''ExprSwitchStmt : SWITCH SimpleStmt SEMICOLON LCURLY ScopeStart ExprCaseClauseList ScopeEnd RCURLY
                      | SWITCH SimpleStmt SEMICOLON Expression LCURLY ScopeStart ExprCaseClauseList ScopeEnd RCURLY
                      | SWITCH LCURLY ScopeStart ExprCaseClauseList ScopeEnd RCURLY
                      | SWITCH Expression LCURLY ScopeStart ExprCaseClauseList ScopeEnd RCURLY
    '''
    parsed.append(p.slice)
    if len(p) == 8:
        l1 = gen('label')
        l2 = gen('label')
        p[0] = TreeNode('ExprSwitchStmt', 0, 'INT', p.linespan(1)[0] - numLines)
        t1 = TreeNode('IDENTIFIER', gen('temp'), 'INT', p.linespan(1)[0] - numLines, 1)
        for i in range(len(p[5].children)):
            pass
    return

def p_ExprCaseClauseList(p):
    '''ExprCaseClauseList : empty
                          | ExprCaseClauseList ExprCaseClause
    '''
    parsed.append(p.slice)
    TAC1 = ThreeAddressCode()
    TAC2 = ThreeAddressCode()
    if len(p) == 3:
        TAC1 = p[1].data
        TAC2 = p[2].data
        p[0] = TreeNode('ExprCaseClauseList', TAC1, 'INT', p.linespan(1)[0] - numLines, 0, p[1].children + p[2].children)

    else:
        p[0] = TreeNode('ExprCaseClauseList', TAC1, 'INT', p.linespan(1)[0] - numLines)

    return

def p_ExprCaseClause(p):
    '''ExprCaseClause : ExprSwitchCase COLON StatementList
    '''
    parsed.append(p.slice)
    l1 = gen('label')
    p[0] = TreeNode('ExprCaseClause', 0, 'INT', p.linespan(1)[0] - numLines)
    p[0].children = [[p[1].data,l1]]
    p[0].data = None

    return

def p_ExprSwitchCase(p):
    '''ExprSwitchCase : CASE ExpressionList
                      | DEFAULT
                      | CASE Expression
    '''
    parsed.append(p.slice)
    p[0] = TreeNode('ExprSwitchCase', 0, 'INT', p.linespan(1)[0] - numLines)
    if len(p) == 3:
        p[0].data = p[2].data

    return

def p_ForStmt(p):
    '''ForStmt : FOR Expression Block
               | FOR Block
    '''
    parsed.append(p.slice)
    p[0] = TreeNode('ForStmt', 0, 'INT', p.linespan(1)[0] - numLines)
    if len(p) == 4:
        l1 = gen('label')
        l2 = gen('label')

    if len(p) == 3:
        l1 = gen('label')
    return

def p_ReturnStmt(p):
    '''ReturnStmt : RETURN
                  | RETURN Expression
                  | RETURN ExpressionList
    '''
    parsed.append(p.slice)
    if len(p) == 2:
        p[0] = TreeNode('ReturnStmt', 0, 'None', p.linespan(1)[0] - numLines)
    if len(p) == 3:
        if p[2].name == 'Expression':
            p[0] = p[2]
            p[0].name = 'ReturnStmt'
    return

def p_BreakStmt(p):
    '''BreakStmt : BREAK IDENTIFIER
    '''
    parsed.append(p.slice)
    return

def p_ContinueStmt(p):
    '''ContinueStmt : CONTINUE IDENTIFIER
    '''
    parsed.append(p.slice)
    return

def p_GotoStmt(p):
    '''GotoStmt : GOTO IDENTIFIER
    '''
    parsed.append(p.slice)
    return

def p_Expression(p):
    '''Expression : UnaryExpr
                  | Expression OR_OR Expression
                  | Expression AMP_AMP Expression
                  | Expression EQ_EQ Expression
                  | Expression NOT_EQ Expression
                  | Expression LT Expression
                  | Expression LT_EQ Expression
                  | Expression GT Expression
                  | Expression GT_EQ Expression
                  | Expression PLUS Expression
                  | Expression MINUS Expression
                  | Expression OR Expression
                  | Expression CARET Expression
                  | Expression STAR Expression
                  | Expression DIVIDE Expression
                  | Expression MODULO Expression
                  | Expression LS Expression
                  | Expression RS Expression
                  | Expression AMP Expression
                  | Expression AND_OR Expression
    '''
    parsed.append(p.slice)
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4:
        p[0] = TreeNode('IDENTIFIER', gen('temp'), 'INT', p.linespan(1)[0] - numLines, 1, [])
    p[0].name = 'Expression'
    return

def p_UnaryExpr(p):
    '''UnaryExpr : PrimaryExpr
                 | unary_op UnaryExpr
    '''
    parsed.append(p.slice)
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        p[0] = TreeNode('IDENTIFIER', gen('temp'), 'INT', p.linespan(1)[0] - numLines, 1)
    p[0].name = 'UnaryExpr'
    return

def p_unary_op(p):
    '''unary_op : PLUS
                | MINUS
                | NOT
                | CARET
                | STAR
                | AMP
                | LT_MINUS
    '''
    parsed.append(p.slice)
    p[0] = TreeNode('unary_op', p[1], 'OPERATOR', p.linespan(1)[0] - numLines)
    return

def p_PrimaryExpr(p):
    '''PrimaryExpr : Operand
                   | IDENTIFIER
                   | PrimaryExpr Selector
                   | PrimaryExpr Index
                   | PrimaryExpr Arguments
    '''
    parsed.append(p.slice)
    if len(p) == 2:
        if p.slice[1].type == 'IDENTIFIER':
            p[0] = TreeNode('IDENTIFIER', p[1], 'INT', p.linespan(1)[0] - numLines, 1)
        elif p[1].name == 'Operand':
            p[0] = p[1]
    elif len(p) == 3:
        if p[2].name == 'Index':
            p[0] = TreeNode('IDENTIFIER', p[1].data, 'INT', p.linespan(1)[0] - numLines,  1)
        elif p[2].name == 'Arguments':
            p[0] = TreeNode('IDENTIFIER', gen('temp'), 'INT',p.linespan(1)[0] - numLines, 1)

            # p[1].print_node()
            func = check_variable(p[1]).split("_")
            scope, funcName =  "_".join(func[:2]), "_".join(func[2:])

            temp = 0
            for f in symbol_table.symbol_table[scope]['functions']:
                if f.name == funcName:
                    temp = len(f.parameters)

            # p[2].print_node()
            for child in p[2].children:
                pass
            if temp != p[2].data:
                print_error('Function ' + funcName + ' requires ' + str(temp) + ' parameters but ' + str(p[2].data) + ' supplied', p.linespan(1)[0] - numLines)
    p[0].name = 'PrimaryExpr'
    return

def p_Operand(p):
    '''Operand  : Literal
                | LROUND Expression RROUND
    '''
    parsed.append(p.slice)
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]
    p[0].name = 'Operand'
    return

def p_Literal(p):
    '''Literal  : BasicLit
                | FunctionLit
    '''
    parsed.append(p.slice)
    p[0] = p[1]
    p[0].name = 'Literal'
    return

def p_BasicLit(p):
    '''BasicLit : int_lit
                | float_lit
                | string_lit
                | rune_lit
    '''
    parsed.append(p.slice)
    p[0] = p[1]
    p[0].name = 'BasicLit'
    return

def p_int_lit(p):
    '''int_lit : decimal_lit
               | octal_lit
               | hex_lit
    '''
    parsed.append(p.slice)
    p[0] = p[1]
    p[0].name = 'int_lit'
    return

def p_decimal_lit(p):
    '''decimal_lit : DECIMAL_LIT
    '''
    parsed.append(p.slice)
    p[0] = TreeNode('decimal_lit', p[1], 'INT', p.linespan(1)[0] - numLines)
    return

def p_octal_lit(p):
    '''octal_lit : OCTAL_LIT
    '''
    parsed.append(p.slice)
    p[0] = TreeNode('octal_lit', p[1], 'OCT', p.linespan(1)[0] - numLines)
    return

def p_hex_lit(p):
    '''hex_lit  : HEX_LIT
    '''
    parsed.append(p.slice)
    p[0] = TreeNode('hex_lit', p[1], 'HEX', p.linespan(1)[0] - numLines)
    return

def p_float_lit(p):
    '''float_lit : FLOAT_LIT
    '''
    parsed.append(p.slice)
    p[0] = TreeNode('float_lit', p[1], 'FLOAT', p.linespan(1)[0] - numLines)
    return

def p_FunctionLit(p):
    '''FunctionLit : FUNC Signature FunctionBody
    '''
    parsed.append(p.slice)
    # Anonymous Function
    # Not implemented yet
    return

def p_Selector(p):
    '''Selector : DOT IDENTIFIER
    '''
    parsed.append(p.slice)
    return

def p_Index(p):
    '''Index : LSQUARE Expression RSQUARE
    '''
    parsed.append(p.slice)
    p[0] = p[2]
    p[0].name = 'Index'
    return

def p_Arguments(p):
    '''Arguments : LROUND RROUND
                 | LROUND ExpressionList RROUND
                 | LROUND Expression RROUND
                 | LROUND Type RROUND
                 | LROUND Type COMMA ExpressionList RROUND
                 | LROUND Type COMMA Expression RROUND
    '''
    # print p.slice
    parsed.append(p.slice)
    if len(p) == 3:
        p[0] = TreeNode('Arguments', 0, 'None', p.linespan(1)[0] - numLines)
    if len(p) == 4:
        if p[2].name == 'Expression':
            p[0] = TreeNode('Arguments', 1, 'None', p.linespan(1)[0] - numLines, 0, [p[2]])
        if p[2].name == 'ExpressionList':
            p[0] = p[2]
            p[0].name = 'Arguments'
            p[0].data = len(p[2].children)
    return

def p_string_lit(p):
    '''string_lit : STRING_LIT
    '''
    parsed.append(p.slice)
    p[0] = TreeNode('string_lit', p[1], 'STRING', p.linespan(1)[0] - numLines)
    return

def p_rune_lit(p):
    '''rune_lit : RUNE_LIT
    '''
    parsed.append(p.slice)
    p[0] = TreeNode('rune_lit', p[1], 'RUNE',p.linespan(1)[0] - numLines)
    return

def p_empty(p):
    'empty :'
    pass

def p_error(p):
    print(p)
    if p == None:
        print(str(sys.argv[1]) + " :: You missed something at the end")
    else:
        print(str(sys.argv[1]) + " :: Syntax error in line no " +  str(p.linespan(1)[0] - numLines))

# Standard Logger
logging.basicConfig(
    level = logging.DEBUG,
    filename = "parselog.txt",
    filemode = "w",
    format = "%(filename)10s:%(lineno)4d:%(message)s"
)

log = logging.getLogger()

yacc.yacc(debug=True, debuglog=log)    #Startup YACC

input_file = sys.argv[1]

import os
if os.path.isfile(input_file) is False:
    print('Input file ' + input_file + ' does not exist')
    sys.exit(1)

input_code = open(input_file, 'r').read()

if input_code[len(input_code)-1] != '\n':  #Add trailing newline to the file if it does not exist
    input_code += '\n'

numLines = len(input_code.split("\n"))-1
yacc.parse(input_code, debug=log, tracking=True)   #Run YACC, write log information to parselog.txt
symbol_table.print_symbol_table()
