# A tree walker to interpret ubasic programs

from lambdastack_state import state
from grammar_stuff import assert_match
import sys

#########################################################################
# node functions
#########################################################################
def seq(node):
    
    (SEQ, stmt, stmt_list) = node
    assert_match(SEQ, 'seq')
    
    walk(stmt)
    walk(stmt_list)

#########################################################################
def nil(node):
    
    (NIL,) = node
    assert_match(NIL, 'nil')
    
    # do nothing!
    pass

#########################################################################
def input_stmt(node):

    (I,) = node
    assert_match(I, 'I')

    s = input("Enter a byte in hexadecimal form 00-FF: ")
    
    value = int(s, 16)
    
    state.stacks.push_value(value)

#########################################################################
def output_stmt(node):

    (O,) = node
    assert_match(O, 'O')
        
    value = state.stacks.pop_value()
    
    if type(value) is int
        value = chr(value)
    
    print(value, end='')

#########################################################################
def ternary(node):

    a = state.stacks.pop_value()
    b = state.stacks.pop_value()
    x = state.stacks.pop_value()

    if walk(x):
        state.stacks.push_value(a)
    else:
        state.stacks.push_value(b)

#########################################################################
def global_var(node):
    
    (TICK, var) = node
    assert_match(TICK, '`')

    assign_stmt(('assign',name, var_exp)) # Do a variable assignment

#########################################################################
def plus_exp(node):
    
    (PLUS,c1,c2) = node
    assert_match(PLUS, '+')
    
    v1 = walk(c1)
    v2 = walk(c2)
    
    return v1 + v2

#########################################################################
def minus_exp(node):
    
    (MINUS,c1,c2) = node
    assert_match(MINUS, '-')
    
    v1 = walk(c1)
    v2 = walk(c2)
    
    return v1 - v2

#########################################################################
def times_exp(node):
    
    (TIMES,c1,c2) = node
    assert_match(TIMES, '*')
    
    v1 = walk(c1)
    v2 = walk(c2)
    
    return v1 * v2

#########################################################################
def divide_exp(node):
    
    (DIVIDE,c1,c2) = node
    assert_match(DIVIDE, '/')
    
    v1 = walk(c1)
    v2 = walk(c2)
    
    return v1 // v2

#########################################################################
def eq_exp(node):
    
    (EQ,c1,c2) = node
    assert_match(EQ, '==')
    
    v1 = walk(c1)
    v2 = walk(c2)
    
    return 1 if v1 == v2 else 0

#########################################################################
def le_exp(node):
    
    (LE,c1,c2) = node
    assert_match(LE, '<=')
    
    v1 = walk(c1)
    v2 = walk(c2)
    
    return 1 if v1 <= v2 else 0

#########################################################################
def and_exp(node):
    
    (AND,c1,c2) = node
    assert_match(AND, '&')
    
    v1 = walk(c1)
    v2 = walk(c2)
    
    return 1 if (v1 and v2) else 0

#########################################################################
def or_exp(node):
    
    (OR,c1,c2) = node
    assert_match(OR, '|')
    
    v1 = walk(c1)
    v2 = walk(c2)
    
    return 1 if (v1 or v2) else 0

#########################################################################
def integer_exp(node):

    (INTEGER, value) = node
    assert_match(INTEGER, 'integer')
    
    return value

#########################################################################
def string_exp(node):

    (INTEGER, value) = node
    assert_match(INTEGER, 'string')
    
    return value

#########################################################################
def id_exp(node):
    
    (ID, name) = node
    assert_match(ID, 'id')
    
    return state.symbol_table.get(name, 0)

#########################################################################
def uminus_exp(node):
    
    (UMINUS, exp) = node
    assert_match(UMINUS, 'uminus')
    
    val = walk(exp)
    return - val

#########################################################################
def not_exp(node):
    
    (NOT, exp) = node
    assert_match(NOT, 'not')
    
    val = walk(exp)
    return 0 if val != 0 else 1

#########################################################################
def paren_exp(node):
    
    (PAREN, exp) = node
    assert_match(PAREN, 'paren')
    
    # return the valuexpe of the parenthesized expression
    return walk(exp)

#########################################################################
def step_exp(node):
    
    (STEP, val) = node
    assert_match(STEP, 'step')
    
    return walk(val)

#########################################################################
def value_l_exp(node):
    
    (VALUEL, val, val_list) = node
    assert_match(VALUEL, 'value_l')
        
    head = [walk(val)] if walk(val) is not None else []
    tail = walk(val_list) if walk(val_list) is not None else []
    
    return head + tail

#########################################################################
# walk
#########################################################################
def walk(node):
    # node format: (TYPE, [child1[, child2[, ...]]])
    node_type = node[0]
    
    if node_type in dispatch_dict:
        node_function = dispatch_dict[node_type]
        return node_function(node)
    else:
        raise ValueError("walk: unknown tree node type: " + node_type)

# a dictionary to associate tree nodes with node functions
dispatch_dict = {
    'seq'     : seq,
    '?'       : ternary,
    'SQ'      : single_quote,
    'DQ'      : double_quote,
    'I'       : input_stmt,
    'O'       : output_stmt,
    '`'       : global_var,
    'data'    : data,
    'var'     : var_exp,
    'var_list': var_list,
    'lambda'  : lambda_exp
    'nil'     : nil
}


