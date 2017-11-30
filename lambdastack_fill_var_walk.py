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
    
    walk_fill_out(stmt)
    walk_fill_out(stmt_list)

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

    pass

#########################################################################
def output_stmt(node):

    (O,) = node
    assert_match(O, 'O')
    
    pass

#########################################################################
def ternary(node):
    (QU, var) = node
    assert_match(QU, '?')

    pass

#########################################################################
def global_var(node):
    (TICK, var) = node
    assert_match(TICK, '`')
    
    pass

#########################################################################
def data(node):
    (DATA,val) = node
    assert_match(DATA, 'data')
    
    pass

#########################################################################
def var_exp(node):
    
    (VAR,sym) = node
    assert_match(VAR, 'var')
    
    value = state.symbol_table.lookup_sym(sym)
    
    if value is not None:
        node.clear()
        node.extend(value)
        

#########################################################################
def lambda_exp(node):
    
    (LAMBDA,varl,body) = node
    assert_match(LAMBDA, 'lambda')
    
    pass
    
#########################################################################
def var_list(node):
    
    (LIST, var, var_list) = node
    assert_match(LIST, 'var_list')
    
    pass

#########################################################################
def SQ(node):
    
    (SQ,) = node
    assert_match(SQ, 'SQ')
    
    pass
            
#########################################################################
def DQ(node):
    
    (DQ,) = node
    assert_match(DQ, 'DQ')
    
    pass
    
#########################################################################
# walk
#########################################################################
def walk_fill_out(node):
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