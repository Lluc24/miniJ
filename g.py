"""
Mòdul principal per a la interpretació de programes en el llenguatge G.

Aquest fitxer actua com a controlador principal del sistema: s'encarrega de carregar
el fitxer d'entrada, inicialitzar els components generats per ANTLR (lexer i parser),
i delegar l'execució a un visitor semàntic si no es detecten errors de sintaxi.

També inclou detecció i gestió bàsica d'errors sintàctics, mostrant informació útil
en cas de fallades.
"""

import sys
from antlr4 import *
from gLexer import gLexer
from gParser import gParser
from visitor import Visitor
import warnings
warnings.filterwarnings("ignore")

def main():
    """
    Executa el procés complet d’anàlisi i interpretació del codi G contingut en un fitxer passat com a paràmetre.

    El flux de processament és:
        1. Carrega el fitxer font passat com a argument.
        2. Genera un flux de tokens amb el lexer gLexer.
        3. Construeix l’arbre sintàctic amb gParser.
        4. Si no hi ha errors sintàctics, s’executa el visitor semàntic Visitor.
        5. Si hi ha errors sintàctics, s’informa l’usuari amb suggeriments.
    """
    args = sys.argv
    file = args[1]
    input_stream = FileStream(file)
    lexer = gLexer(input_stream)
    lexer.removeErrorListeners()
    token_stream = CommonTokenStream(lexer)
    parser = gParser(token_stream)
    parser.removeErrorListeners()
    tree = parser.root()

    if parser.getNumberOfSyntaxErrors() == 0:
        visitor = Visitor()
        visitor.visit(tree)
    else:
        print(parser.getNumberOfSyntaxErrors(), 'errors lèxics/sintàctics.')
        tree = tree.toStringTree(recog=parser)
        print(tree)
        if tree.find(r"<missing '\n'> <EOF>") != -1:
            print("Verifica que hi hagi un salt de línia al final del fitxer.")


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"Error inesperat: {error}")