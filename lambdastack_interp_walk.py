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
    
    val = walk(value)
    
    if type(val) is int:
        val = hex(val)
    
    print(val)

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

    value = state.stacks.pop_value()
    
    state.symbol_table.declare_sym(var, value, g=True) # Do a variable assignment

#########################################################################
def data(node):
    
    (DATA,val) = node
    assert_match(DATA, 'data')
    
    state.stacks.push_value(node)
    
    return val

#########################################################################
def var_exp(node):
    
    (VAR,sym) = node
    assert_match(VAR, 'var')
    
    value = state.symbol_table.lookup_sym(sym)
    if value is not None:
        state.stacks.push_value(value)
    
    return sym

#########################################################################
def lambda_exp(node):
    
    (LAMBDA,varl,body) = node
    assert_match(LAMBDA, 'lambda')
    
    state.stacks.push_value(node)
    
    return 'Output of lambda not supported yet'
    
#########################################################################
def var_list(node):
    
    (LIST, var, var_list) = node
    assert_match(LIST, 'var_list')
        
    head = [walk(var)] if walk(var) is not None else []
    tail = walk(var_list) if walk(var_list) is not None else []
    
    return head + tail

#########################################################################
def SQ(node):
    
    (SQ,val) = node
    assert_match(SQ, 'SQ')
    
    value = state.stacks.pop_value()
    
    if value[0] == 'data':
        b = state.stacks.pop_value()
        a = state.stacks.pop_value()
        if value[1] > 15:
            b = exec_bitwise(value[1] // 16, a, b)
            a = state.stacks.pop_value()
            
        result = exec_bitwise(op % 16, a, b)
        
    elif value[1] == 'lambda':
        stack = state.stacks.get_curr_stack()
        (LAMBDA, var_l, body) = value
        result = exec_lambda(walk(var_l), body, stack, fill_out=False)
        
    else:
        raise ValueError("Unknown node found on stack: " + node)
        
    state.stacks.push_value(result)
    
#########################################################################
def DQ(node):
    
    (DQ,val) = node
    assert_match(DQ, 'DQ')
    
    value = state.stacks.pop_value()

    if value[0] == 'data':
        result = ('lambda', None, value[1])
        
    elif value[1] == 'lambda':
        stack = state.stacks.get_curr_stack()
        (LAMBDA, var_l, body) = value
        result = exec_lambda(var_l, body, stack, fill_out=True)
        
    else:
        raise ValueError("Unknown node found on stack: " + node)
        
    state.stacks.push_value(result)
    
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
    'lambda'  : lambda_exp,
    'nil'     : nil
}

#########################################################################
# helper functions
#########################################################################

def exec_lambda(var_l, body, stack, fill_out=False):
    
    state.symbol_table.push_scope()
    state.stacks.push_stack()
    
    if var_l.count('%') > 1:
        raise ValueError("Too many '%' in lambda with an input of: " + varl)
    
    if var_l is not None:        
        
        # We reverse this to match up with the stack
        var_l.reverse()
        found = False
        
        for i in var_l:
            
            if i == '%' and found == False:
                var_l.reverse()
                stack.reverse()
                found = True
                continue
                
            elif i == '%' and found == True:
                state.symbol_table.declare_sym(i, stack)
                
            
            val = stack.pop()
            state.symbol_table.declare_sym(i, val)
    
        
    state.symbol_table.pop_scope()
    state.stacks.pop_stack()
    
def exec_bitwise(op, a, b):
    return 0
