# A tree walker to interpret ubasic programs

from lambdastack_state import state
from lambdastack_fill_var_walk import walk_fill_out
from lambdastack_pp_walk import walk_pp
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
    
    state.stacks.push_value(['data',value])

#########################################################################
def output_stmt(node):

    (O,) = node
    assert_match(O, 'O')
    
    value = state.stacks.pop_value()
    
    val = walk_pp(value)
    
    print(val)

#########################################################################
def ternary(node):
    
    (QU, var) = node
    assert_match(QU, '?')

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
    
    state.symbol_table.declare_sym(walk(var), value, g=True) # Do a variable assignment

#########################################################################
def data(node):
    
    (DATA,val) = node
    assert_match(DATA, 'data')
    
    state.stacks.push_value(['data', val])
    
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
    
    state.stacks.push_value(['lambda', varl, body])
        
#########################################################################
def var_list(node):
    
    (LIST, var, var_list) = node
    assert_match(LIST, 'var_list')
    
    if var_list is None:
        return [walk(var)]
    
    head = [walk(var)]
    tail = walk(var_list)
    
    return head + tail

#########################################################################
def SQ(node):
    
    (SQ,) = node
    assert_match(SQ, 'SQ')
    
    value = state.stacks.pop_value()
    
    if value[0] == 'data':
        b = state.stacks.pop_value()
        a = state.stacks.pop_value()
        if value[1] > 15:
            b = exec_bitwise(value[1] // 16, a[1], b[1])
            a = state.stacks.pop_value()
            
        result = exec_bitwise(value[1] % 16, a[1], b[1])
        state.stacks.push_value(['data',result])
        
    elif value[0] == 'lambda':
        (LAMBDA, var_l, body) = value
        exec_lambda(var_l, body, fill_out=False)
        
    else:
        raise ValueError("Unknown node found on stack: " + str(node))
            
#########################################################################
def DQ(node):
    
    (DQ,) = node
    assert_match(DQ, 'DQ')
    
    value = state.stacks.pop_value()

    if value[0] == 'data':
        result = ['lambda', None, value[1]]
        
    elif value[0] == 'lambda':
        (LAMBDA, var_l, body) = value
        exec_lambda(var_l, body, fill_out=True)
        result = ['lambda', None, body]
        
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
    'SQ'      : SQ,
    'DQ'      : DQ,
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

def exec_lambda(var_l, body, fill_out=False):
    
    state.symbol_table.push_scope()
    
    
    ### Start: Filling out the scope dictionary ### 
    if var_l is not None:        
        
        # Actually build the list now
        var_l = walk(var_l)
        
        if var_l.count('%') > 1:
            raise ValueError("Too many '%' in lambda with an input of: " + varl)
        
        found = False
        index = len(var_l) - 1
        
        while(index >= 0):
            
            i = var_l[index]
            
            if i == '%' and found == False:
                var_l.reverse()
                state.stacks.reverse()
                found = True
                index = len(var_l) - 1
                continue
                
            elif i == '%' and found == True:
                state.stacks.reverse()
                stack = state.stacks.get_curr_stack()
                state.symbol_table.declare_sym(i, build_seq(stack))
                break
            
            val = state.stacks.pop_value()
            state.symbol_table.declare_sym(i, val)
            var_l.pop()
            
            index -= 1
    
    ### End: Filling out the scope dictionary ###
    
    state.stacks.push_stack()
    
    if fill_out:
        walk_fill_out(body)
    else:
        walk(body)
    
    state.symbol_table.pop_scope()
    state.stacks.compress_stack()
    
def exec_bitwise(op, a, b):
    
    result = {
        0: lambda a,b: 0,
        1: lambda a,b:  (a ^ 0xFF) & (b ^ 0xFF),
        2: lambda a,b:  (a ^ 0xFF) &  b,
        3: lambda a,b:  (a ^ 0xFF),
        4: lambda a,b:  a  & (b ^ 0xFF),
        5: lambda a,b:  (b ^ 0xFF),
        6: lambda a,b:  a  ^  b,
        7: lambda a,b:  (a ^ 0xFF) | (b ^ 0xFF),
        8: lambda a,b:  a  &  b,
        9: lambda a,b:  (a ^ 0xFF) ^  b,
        10: lambda a,b: b,
        11: lambda a,b: (a ^ 0xFF) |  b,
        12: lambda a,b: a,
        13: lambda a,b: a  | (b ^ 0xFF),
        14: lambda a,b: a  |  b,
        15: lambda a,b: 1,
    }[op](a,b)
               
    return result

def build_seq(l):
    
    if len(l) == 0:
        return ['nil']
    
    seq = ['seq', l.pop(0)]
    seq.append(build_seq(l))
    return seq

def build_var_l(l):
    
    if len(l) == 0:
        return ['nil']
    
    seq = ['var_list', l.pop(0)]
    seq.append(build_seq(l))
    return seq