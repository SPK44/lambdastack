from ply import yacc
from lambdastack_lex import tokens, lexer

def p_grammar(_):
    '''
    prog : instr_list

    instr_list : instr instr_list
               | empty

    instr : '?'
          | HEX
          | BYTE
          | CHAR
          | var
          | lambda
          | SQ
          | DQ
          | '`' var
          | I
          | O

    var : NAME
        | SVAR
        | '%'
    
    var_list : var var_list
             | var                
    
    lambda : '[' var_list ':' instr_list ']'
           | '[' instr_list ']'
    '''
    pass

def p_empty(p):
    'empty :'
    pass

def p_error(t):
    print("Syntax error at '%s'" % t.value)

parser = yacc.yacc()
