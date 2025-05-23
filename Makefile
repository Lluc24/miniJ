.PHONY: clean

exprsLexer.py exprsLexer.tokens exprsParser.py exprs.tokens &: exprs.g4
	antlr4 -Dlanguage=Python3 -no-listener -visitor exprs.g4

clean:
	rm *.tokens *.interp exprsLexer.py exprsParser.py exprsVisitor.py
