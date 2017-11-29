# define and initialize the structures of our abstract machine

class StackStack:

    #-------
    def __init__(self):
        # global scope stack must always be present
        self.stack = [[]]
        self.curr_stack = 0
        
    #-------
    def push_stack(self):
        # push a new stack onto the stack
        self.stack.append([])
        self.curr_stack += 1

    #-------
    def pop_stack(self):
        # pop the left most dictionary off the stack
        if self.curr_stack == 0:
            raise ValueError("cannot pop the global stack")
        else:
            self.stack.pop()
            self.curr_stack -= 1


    #-------
    def push_value(self, value):
        # push the value in the current stack
        if type(value) is list:
            for i in value:
                self.stack[self.curr_stack].append(('data',i))
            return
        
        scope_stack = self.stack[self.curr_stack]
        scope_stack.append(value)

    #-------
    def pop_value(self):
        return self.stack[self.curr_stack].pop()
    
    #-------
    def get_curr_stack(self):
        return self.stack[self.curr_stack]
        
class DictStack:

    #-------
    def __init__(self):
        # global scope dictionary must always be present
        self.scoped_symtab = [{}]
        self.curr_scope = 0
        
    #-------
    def push_scope(self):
        # push a new dictionary onto the stack
        self.scoped_symtab.append({})
        self.curr_scope += 1

    #-------
    def pop_scope(self):
        # pop the right most dictionary off the stack
        if self.curr_scope == 0:
            raise ValueError("cannot pop the global scope")
        else:
            self.scoped_symtab.pop()
            self.curr_scope -= 1

    #-------
    def declare_sym(self, sym, node, g=False):
        # declare the scalar in the current scope
        # unless g is set to true, in that case, it is global
        
        scope = self.curr_scope
        if g:
            scope = 0
        
        # first we need to check whether the symbol was already declared
        # at this scope
        if sym in self.scoped_symtab[scope]:
            raise ValueError("symbol {} already declared".format(sym))
        
        # enter the symbol in the current scope
        scope_dict = self.scoped_symtab[scope]
        scope_dict[sym] = node

    #-------
    def lookup_sym(self, sym):
        # find the first occurence of sym in the currecnt scope
        # and return the associated value.
        # This language only has local, and global scope

        for scope in [self.curr_scope, 0]:
            if sym in self.scoped_symtab[scope]:
                node = self.scoped_symtab[scope].get(sym)
                return node

        # not found
        return None



class State:

    def __init__(self):
        self.initialize()
    
    def initialize(self):
        self.AST = None
        self.symbol_table = DictStack()
        self.stacks = StackStack()

state = State() 