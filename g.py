import sys
from antlr4 import *
from gLexer import gLexer
from gParser import gParser
from visitor import Visitor

if __name__ == "__main__":
    args = sys.argv
    file = args[1]
    input_stream = FileStream(file)
    lexer = gLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = gParser(token_stream)
    tree = parser.root()

    visitor = Visitor()
    visitor.visit(tree)