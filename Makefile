.PHONY: clean install

install:
	pip install antlr4-tools; antlr4; pip install antlr4-python3-runtime

gLexer.py gLexer.tokens gParser.py g.tokens &: g.g4
	antlr4 -Dlanguage=Python3 -no-listener -visitor g.g4

clean:
	rm *.tokens *.interp gLexer.py gParser.py gVisitor.py
