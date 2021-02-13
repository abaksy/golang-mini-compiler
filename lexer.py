#!/usr/bin/python

import ply.lex as lex
import sys

print_op = 0

input_file = sys.argv[1]
if len(sys.argv) > 2:
    print_op = int(sys.argv[2])

import os
if os.path.isfile(input_file) is False:
    print('Input file ' + input_file + ' does not exist')
    sys.exit(1)

input_code = open(input_file, 'r').read()
if input_code[len(input_code)-1] != '\n':
    input_code += '\n'

semimode = False

def setSemiMode():
    global semimode
    if input_code[lexer.lexpos] == '\n':
        semimode = True

# The following are the list of kwywords which are reserved in GoLang
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
    'RUNE_LIT',

    # 'UNICODE_DIGIT','UNICODE_LETTER',
    # 'ESCAPED_CHAR', 'BYTE_VALUE', 'OCTAL_BYTE_VALUE', 'HEX_BYTE_VALUE',
    # 'UNDERSCORE'
    'NEWLINE',
    'PREDEFINED_TYPES',
    'IDENTIFIER',

    'BREAK',
    'CONTINUE',
    'RETURN',
    'PRINTLN'
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

def t_PRINTLN(t):
    r'Println'
    # setSemiMode()
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

def t_PREDEFINED_TYPES(t):
    r'((int)|(float)|(char)|(string)|(bool))'
    return t

def t_STRING_LIT(t):
    r'(\"[^(\")]*\")|\`((\\x[0-9A-Fa-f]{2})|(\\u[0-9A-Fa-f]{4})|(\\U[0-9A-Fa-f]{8})|(\\[0-7]{3})|(\\(a|b|f|n|r|t|v|\\|\'|\"))|([^(\`)]))*\`'
    t.value = t.value[1:-1]
    setSemiMode()
    return t

def t_RUNE_LIT(t):
    r'\'((\\x[0-9A-Fa-f]{2})|(\\u[0-9A-Fa-f]{4})|(\\U[0-9A-Fa-f]{8})|(\\[0-7]{3})|(\\(a|b|f|n|r|t|v|\\|\'|\"))|([^(\')]))\''
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
    print(t)
    print("*** Error (Lexer): There is an illegal character '%r' in the input program on line number %d and position %d ***" % (t.value, t.lineno, t.lexpos))
    t.lexer.skip(1)

lexer = lex.lex()
lexer.input(input_code)

token_type_list = {}
lexeme_list = {}
token_stream = []

tokens_more_than_once = ['IDENTIFIER']

while 1:
    tokens_generated = lexer.token()
    token_stream.append(tokens_generated)

    if not tokens_generated:
        break
    token_name = tokens_generated.value
    token_type = tokens_generated.type

    if token_type not in token_type_list:
        token_type_list[token_type]= 1
        lexeme_list[token_type] = [token_name]
    else:
        if token_name not in lexeme_list[token_type]:
            lexeme_list[token_type].append(token_name)
            token_type_list[token_type] += 1
        else:
            if token_type not in tokens_more_than_once:
                token_type_list[token_type] += 1

def print_tokens(tokens):
    """Prints the token stream in order"""
    for token in token_stream:
        if token != None:
            print(token)

def print_lexemes(token_type_list, lexemes):
    """Prints the lexemes in a tabular format"""
    print("Token" + " " * 20 + "Occurrances" + " " * 22 + "Lexemes")
    print("-" * 65)

    for data in token_type_list:
        sys.stdout.write("{:25s} {:>4s}".format(data, (str)(token_type_list[data])))
        print("{:>35s}".format(lexemes[data][0]))
        for lexlist in lexemes[data][1:]:
            sys.stdout.write("{:>65s}\n".format(lexlist))
        print("-" * 65)

if print_op & 1:
    print_lexemes(token_type_list, lexeme_list)
if print_op & 2:
    print_tokens(token_stream)

