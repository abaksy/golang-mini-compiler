from ply import lex
import sys

tokens = ['ID', 'INT_LIT', 'FLOAT_LIT', 'STR_LIT', 'COMMENT',         #Literals and Identifiers
            'PLUS', 'MINUS', 'MUL', 'DIV', 'MOD',           #Arithmetic
            'GT', 'LT', 'GE', 'LE', 'EQEQ', 'NEQ',          #Relational
            'BAND', 'BOR', 'BXOR', 'BNOT', 'LSHIFT', 'RSHIFT',      #Bitwise
            'LAND', 'LOR',                                  #Logical
            'INCR', 'DECR', 'NOT',                           #Unary
            'EQ', 'PLUS_EQ', 'MIN_EQ', 'MUL_EQ', 'DIV_EQ', 'MOD_EQ', 'LSHIFT_EQ', 'RSHIFT_EQ', 'BAND_EQ', 'BOR_EQ', 'BXOR_EQ',  #Assignment
            'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'LSQ', 'RSQ', 'ELLIPSIS', 'DOT', 'COMMA', 'SCOLON', 'COLON']                #Punctuation
            
reserved = {
    'break':'BREAK',
    'case': 'CASE',
    'continue': 'CONTINUE',
    'const': 'CONST',
    'default': 'DEFAULT',
    'else':'ELSE',
    'for': 'FOR', 
    'func': 'FUNC',
    'go': 'GO',
    'if': 'IF',
    'import': 'IMPORT',
    'map': 'MAP', 
    'package': 'PACKAGE',
    'return':'RETURN',
    'select': 'SELECT', 
    'switch': 'SWITCH',
    'struct': 'STRUCT',
    'type': 'TYPE', 
    'var': 'VAR'
}

tokens += list(reserved.values())

t_GE = r'>='
t_LE = r'<='
t_EQEQ = r'=='
t_NEQ = r'!='
t_LSHIFT = r'<<'
t_RSHIFT = r'>>'
t_LAND = r'&&'
t_LOR = r'\|\|'
t_INCR = r'\+\+'
t_DECR = r'--'
t_PLUS_EQ = r'\+='
t_MIN_EQ = r'-='
t_MUL_EQ = r'\*='
t_DIV_EQ = r'/='
t_MOD_EQ = r'%='
t_LSHIFT_EQ = r'<<='
t_RSHIFT_EQ = r'>>='
t_BAND_EQ = r'&='
t_BOR_EQ = r'\|='
t_BXOR_EQ = r'\^='

t_PLUS = r'\+'
t_MINUS = r'-'
t_MUL = r'\*'
t_DIV = r'/'
t_MOD = r'%'
t_GT = r'>'
t_LT = r'<'
t_BAND = r'&'
t_BOR = r'\|'
t_BXOR = r'\^'
t_BNOT = r'~'
t_NOT = r'!'
t_EQ = r'='

t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LSQ = r'\['
t_RSQ = r'\]'
t_ELLIPSIS = r'\.\.\.'
t_DOT = r'\.'
t_COMMA = r'\,'
t_SCOLON = r';'
t_COLON = r':'


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def find_column(input, token):
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1

def t_STR_LIT(t):
    r'"([^"\\]|\\.)*"'
    return t

def t_ID(t):
    r'[a-zA-Z_]([a-zA-Z0-9_])*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_INT_LIT(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except:
        t.value = 0
        print("Error in specifying integer literal")
    return t

'''
def t_FLOAT_LIT(t):
    #PLEASE HELP WRITE REGEX FOR FLOAT NUMBERS
    try:
        t.value = float(t.value)
    except:
        t.value = 0.0
    return t
'''
t_ignore = ' \t'

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

if __name__=="__main__":
    lexer = lex.lex()
    with open(sys.argv[1]) as f:
        text = f.read()
    lexer.input(text)
    tok = lexer.token()
    while tok is not None:
        print(tok)
        tok = lexer.token()

precedence = (
    ('left', 'COMMA'),
    ('right', 'EQ', 'PLUS_EQ', 'MIN_EQ', 'MUL_EQ', 'DIV_EQ', 'MOD_EQ', 'LSHIFT_EQ', 'RSHIFT_EQ', 'BAND_EQ', 'BOR_EQ', 'BXOR_EQ'),
    ('left', 'LOR'),
    ('left', 'LAND'),
    ('left', 'BOR'),
    ('left', 'BXOR'),
    ('left', 'BAND'),
    ('left', 'EQEQ', 'NEQ'),
    ('left', 'GT', 'LT', 'GE', 'LE'),
    ('left', 'LSHIFT', 'RSHIFT'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MUL', 'DIV', 'MOD'),
    ('right', 'INCR', 'DECR', 'NOT', 'BNOT'),
)
    