from ply import yacc
from lambdastack_lex import tokens, lexer
from lambdastack_state import state

def p_prog(p):
    '''
    prog : instr_list
    '''
    state.AST = p[1]

def p_instr_list(p):
    '''
    instr_list : instr instr_list
               | empty
    '''
    # append instr to program
    if len(p) == 3:
        p[0] = ('seq', p[1], p[2])
    elif len(p) == 2:
        p[0] = p[1]

def p_literal_instr(p):
    '''
    instr : '?'
          | SQ
          | DQ
          | I
          | O
          | '`' var
    '''
    # for each instr assemble the appropriate tuple
    if p[1] == '?':
        p[0] = ('?',)
    elif p[1] == "'":
        p[0] = ('SQ',)
    elif p[1] == '"':
        p[0] = ('DQ',)
    elif p[1] == 'I':
        p[0] = ('I',)
    elif p[1] == 'O':
        p[0] = ('O',)
    elif p[1] == '`':
        p[0] = ('`', p[2])
    else:
        raise ValueError("unexpected symbol {}".format(p[1]))
        
def p_data_instr(p):
    '''
    instr : HEX
          | BYTE
          | CHAR
    '''
    p[0] = ('data',p[1])
    
def p_through_instr(p):
    '''
    instr : var
          | lambda
    '''
    p[0] = p[1]

def p_var(p):
    '''
    var : NAME
        | SVAR
        | '%'
    '''
    p[0] = ('var', p[1])

def p_var_list(p):
    '''
    var_list : var var_list
             | var
    '''
    if len(p) == 3:
        p[0] = ('var_list', p[1], p[2])
    elif len(p) == 2:
        p[0] = p[1]
        
def p_lambda(p):
    '''
    lambda : '[' var_list ':' instr_list ']'
           | '[' instr_list ']'
    '''
    
    if len(p) > 4:
        p[0] = ('lambda', p[2], p[4])
    else:
        p[0] = ('lambda', None, p[2]) 
    
def p_empty(p):
    '''
    empty :
    '''
    p[0] = ('nil',)

def p_error(t):
    print("Syntax error at '%s'" % t.value)

parser = yacc.yacc(debug=False, tabmodule='lambdastack')

