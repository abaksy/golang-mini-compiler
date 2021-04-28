#!/usr/bin/env python

import ply.lex as lex
import sys
import os

semimode = False

def setSemiMode():
    global semimode
    if input_code[lexer.lexpos] == '\n':
        semimode = True

# The following are the list of keywords which are reserved in GoLang
reserved_keywords = {
    'nil'      : 'NIL',
    'default'  : 'DEFAULT',
    'func'     : 'FUNC',
    'select'   : 'SELECT',
    'case'     : 'CASE',
    'go'       : 'GO',
    'struct'   : 'STRUCT',
    'else'     : 'ELSE',
    'goto'     : 'GOTO',
    'package'  : 'PACKAGE',
    'switch'   : 'SWITCH',
    'const'    : 'CONST',
    'if'       : 'IF',
    'type'     : 'TYPE',
    'for'      : 'FOR',
    'import'   : 'IMPORT',
    'var'      : 'VAR',
    'true'     : 'TRUE',
    'false'    : 'FALSE'
}

# These are the list of all tokens which we will be going to use in our building of lexer
tokens = list(reserved_keywords.values()) + [
    'PLUS',
    'MINUS',
    'STAR',
    'DIVIDE',
    'MODULO',
    'AMP',
    'OR',
    'CARET',
    'LS',
    'RS',
    'AND_OR',
    'PLUS_EQ',
    'MINUS_EQ',
    'STAR_EQ',
    'DIVIDE_EQ',
    'MODULO_EQ',
    'AMP_EQ',
    'OR_EQ',
    'CARET_EQ',
    'LS_EQ',
    'RS_EQ',
    'AND_OR_EQ',
    'AMP_AMP',
    'OR_OR',
    'LT_MINUS',
    'PLUS_PLUS',
    'MINUS_MINUS',
    'EQ_EQ',
    'LT',
    'GT',
    'EQ',
    'NOT',
    'NOT_EQ',
    'LT_EQ',
    'GT_EQ',
    'ASSIGN_OP',
    'LSQUARE',
    'RSQUARE',
    'LROUND',
    'RROUND',
    'LCURLY',
    'RCURLY',
    'COMMA',
    'DDD',
    'DOT',
    'SEMICOLON',
    'COLON',
    'SINGLE_QUOTES',
    'DOUBLE_QUOTES',

    'DECIMAL_LIT',
    'OCTAL_LIT',
    'HEX_LIT',
    'FLOAT_LIT',
    'STRING_LIT',

    # 'UNICODE_DIGIT','UNICODE_LETTER',
    # 'ESCAPED_CHAR', 'BYTE_VALUE', 'OCTAL_BYTE_VALUE', 'HEX_BYTE_VALUE',
    # 'UNDERSCORE'
    'NEWLINE',
    'IDENTIFIER',
    'PREDEF_TYPE',
    'BREAK',
    'CONTINUE',
    'RETURN', 
    'invalidIdent'
]

t_ignore = ' \t'

def t_COMMENT(t):
    r'(/\*([^*]|\n|(\*+([^*/]|\n])))*\*+/)|(//.*)'
    pass

def t_BREAK(t):
    r'break'
    setSemiMode()
    return t

def t_CONTINUE(t):
    r'continue'
    setSemiMode()
    return t

def t_RETURN(t):
    r'return'
    setSemiMode()
    return t

# Note: We need to have tokens in such a way that
# the tokens like '==' should preceede the token '='
def t_PLUS_PLUS(t):
    r'(\+\+)'
    setSemiMode()
    return t

def t_MINUS_MINUS(t):
    r'(--)'
    setSemiMode()
    return t

t_LS_EQ = r'(<<=)'
t_RS_EQ = r'(>>=)'
t_AND_OR_EQ = r'(&\^=)'
t_LS = r'(<<)'
t_RS = r'(>>)'
t_AND_OR = r'&\^'
t_PLUS_EQ = r'(\+=)'
t_MINUS_EQ = r'(-=)'
t_STAR_EQ = r'(\*=)'
t_DIVIDE_EQ = r'/='
t_MODULO_EQ = r'(%=)'
t_AMP_EQ = r'(&=)'
t_OR_EQ = r'(\|=)'
t_CARET_EQ = r'(\^=)'
t_AMP_AMP = r'(&&)'
t_OR_OR = r'(\|\|)'
t_LT_MINUS  = r'(<-)'
t_EQ_EQ = r'(==)'
t_NOT_EQ = r'(!=)'
t_NOT = r'!'
t_LT_EQ = r'(<=)'
t_GT_EQ = r'(>=)'
t_ASSIGN_OP = r'(:=)'
t_LSQUARE = r'\['
t_LROUND = r'\('
t_LCURLY = r'\{'
t_COMMA = r'\,'
t_DDD = r'\.\.\.'
t_DOT = r'\.'
t_SEMICOLON = r'\;'
t_COLON = r'\:'
t_DOUBLE_QUOTES = r'\"'
t_SINGLE_QUOTES = r'\''
t_PLUS = r'\+'
t_MINUS = r'-'
t_EQ = r'='
t_LT = r'<'
t_GT = r'>'
t_AMP = r'\&'
t_STAR = r'\*'
t_DIVIDE = r'\/'
t_MODULO = r'\%'
t_OR = r'\|'
t_CARET = r'\^'

def t_invalidIdent(t):
    r'[0-9][a-zA-Z_]+'
    print(f"LEXICAL ERROR: Invalid Identifier '{t.value}' on line {t.lexer.lineno}")
    sys.exit(-1)

def t_PREDEF_TYPE(t):
    r'((int)|(float)|(char)|(string)|(bool))'
    return t

def t_HEX_LIT(t):
    r'0[x|X][0-9A-Fa-f]+'
    setSemiMode()
    return t

def t_FLOAT_LIT(t):
    r'([0-9]+\.([0-9]+)?((e|E)(\+|\-)?[0-9]+)?)|([0-9]+(e|E)(\+|\-)?[0-9]+)|(\.[0-9]+((e|E)(\+|\-)?[0-9]+)?)'
    setSemiMode()
    return t

def t_OCTAL_LIT(t):
    r'0[0-7]*'
    setSemiMode()
    return t

def t_DECIMAL_LIT(t):
    r'[1-9][0-9]*'
    setSemiMode()
    return t

def t_RCURLY(t):
    r'\}'
    setSemiMode()
    return t

def t_RROUND(t):
    r'\)'
    setSemiMode()
    return t

def t_RSQUARE(t):
    r'\]'
    setSemiMode()
    return t

def t_STRING_LIT(t):
    r'(\"[^(\")]*\")|(\`[^(\`)]*\`)'
    t.value = t.value[1:-1]
    setSemiMode()
    return t

def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    global semimode
    if semimode:
        semimode = False
        o = lex.LexToken()
        o.type = 'SEMICOLON'
        o.value = ';'
        o.lineno = t.lexer.lineno
        o.lexpos = t.lexer.lexpos
        return o

def t_IDENTIFIER(t):
    r'[a-zA-Z_@][a-zA-Z_0-9]*'
    t.type = reserved_keywords.get(t.value, 'IDENTIFIER')
    setSemiMode()
    return t

def t_error(t):
    print("There is an illegal character '%s' in the input program" % t.value[0])
    t.lexer.skip(1)

if len(sys.argv) < 2:
    print("Please provide a valid file path!")
    sys.exit(-1)
input_file = sys.argv[1]
if os.path.isfile(input_file) is False:
    print('Input file ' + input_file + ' does not exist')
    sys.exit(1)

input_code = open(input_file, 'r').read()
if input_code[len(input_code)-1] != '\n':
    input_code += '\n'
lexer = lex.lex()
lexer.input(input_code)
token_stream = []

t = lexer.token()
while t is not None:
    token_stream.append(t)
    t = lexer.token()
'''
for token in token_stream:
    print(token)
'''
