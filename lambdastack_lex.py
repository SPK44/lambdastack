# Lexer for Exp1bytecode

from ply import lex

reserved = {
    'I' : 'I',
    'O' : 'O'
}

literals = ['?', '`', '[', ']', ':', '%']

tokens = ['SVAR', 'NAME','HEX', 'BYTE', 'CHAR', 'SQ', 'DQ'] + list(reserved.values())

t_ignore = ' \t'

def t_SVAR(t):
    r'[a-zG-Z]'
    t.type = reserved.get(t.value,'SVAR')    # Check for reserved words
    return t

def t_NAME(t):
    r'[(][a-zG-Z]+[)]'
    # strip parentheses
    t.value = t.value[1:-1]
    return t

def t_HEX(t):
    r'[0-9a-fA-F]'
    t.value = int(t.value, 16)
    return t

def t_BYTE(t):
    r'\([0-9a-fA-F]{2}\)'
    # Strip parentheses
    t.value = int(t.value[1:-1], 16)
    return t

def t_CHAR(t):
    r'\(\'[a-fA-F]\)'
    # Strip parentheses and quote
    t.value = ord(t.value[2:-1])
    return t

def t_SQ(t):
    r'\''
    t.value = "'"
    return t

def t_DQ(t):
    r'\"'
    t.value = '"'
    return t
    
def t_NEWLINE(t):
    r'\n'
    pass
    
def t_error(t):
    print("Illegal character %s" % t.value[0])
    t.lexer.skip(1)

# build the lexer
lexer = lex.lex(debug=0)
