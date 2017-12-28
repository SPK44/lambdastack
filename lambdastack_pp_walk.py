# A tree walker to interpret ubasic programs

from grammar_stuff import assert_match

#########################################################################
# node functions
#########################################################################
def seq(node):
    
    (SEQ, stmt, stmt_list) = node
    assert_match(SEQ, 'seq')
    
    head = walk_pp(stmt)
    tail = walk_pp(stmt_list)

    return head + tail

#########################################################################
def nil(node):
    
    (NIL,) = node
    assert_match(NIL, 'nil')
    
    # do nothing!
    return ""

#########################################################################
def input_stmt(node):

    (I,) = node
    assert_match(I, 'I')

    return "I"

#########################################################################
def output_stmt(node):

    (O,) = node
    assert_match(O, 'O')
    
    return "O"

#########################################################################
def ternary(node):
    
    (QU, var) = node
    assert_match(QU, '?')

    return "?"

#########################################################################
def global_var(node):
    
    (TICK, var) = node
    assert_match(TICK, '`')

    var_name = walk_pp(var)
    
    return "`"+var
    
#########################################################################
def data(node):
    
    (DATA,val) = node
    assert_match(DATA, 'data')
    
    if val < 16:
        string = format(val, 'x')
    else:
        string = '(' + format(val, 'x') + ')'
    
    return string

#########################################################################
def var_exp(node):
    
    (VAR,sym) = node
    assert_match(VAR, 'var')
    
    if len(sym) == 1:
        string = sym
    else:
        string = '(' + sym + ')'
    
    return string

#########################################################################
def lambda_exp(node):
    
    (LAMBDA,varl,body) = node
    assert_match(LAMBDA, 'lambda')
    
    if varl is None:
        string = '[' + walk_pp(body) + ']'
    else:
        string = '[' + walk_pp(varl) + ':' + walk_pp(body) + ']'
    
    return string
    
#########################################################################
def var_list(node):
    
    (LIST, var, var_list) = node
    assert_match(LIST, 'var_list')
    
    if var_list is None:
        return walk_pp(var)
    
    head = walk_pp(var)
    tail = walk_pp(var_list)
    
    return head + tail

#########################################################################
def SQ(node):
    
    (SQ,) = node
    assert_match(SQ, 'SQ')
    
    return "'"
            
#########################################################################
def DQ(node):
    
    (DQ,) = node
    assert_match(DQ, 'DQ')
    
    return '"'
            
#########################################################################
# walk
#########################################################################
def walk_pp(node):
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