from lambdastack_lex import lexer
from lambdastack_interp_gram import parser
from lambdastack_state import state
from lambdastack_interp_walk import walk
from grammar_stuff import dump_AST

def main():

	while True:
		
		try:
			input_stream = input()
		except EOFError:
			return

		# initialize the state object
		state.initialize()

		# build the AST
		parser.parse(input_stream, lexer=lexer)

		# walk the AST
		#dump_AST(state.AST)
		walk(state.AST)

		
main()
