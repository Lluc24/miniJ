import sys
from antlr4 import *
from exprsLexer import exprsLexer
from exprsParser import exprsParser
from treeEval import TreeEval

if __name__ == "__main__":
    args = sys.argv
    file = args[1]
    input_stream = FileStream(file)
    print("Input stream:", input_stream)
    lexer = exprsLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = exprsParser(token_stream)
    tree = parser.root()

    str_tree = tree.toStringTree(recog=parser)
    print("Parse tree:", str_tree)

    visitor = TreeEval()
    visitor.visit(tree)