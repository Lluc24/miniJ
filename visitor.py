"""
Mòdul d'interpretació semàntica del llenguatge G (versió simplificada de J) a partir de
l'arbre de sintaxi generat per ANTLR.

Aquest mòdul conté la classe Visitor, que recorre l'arbre sintàctic produït pel parser gParser
i executa les instruccions corresponents. Es basa en una pila per gestionar l'avaluació d'expressions
i utilitza un entorn amb taules de variables i funcions definides per l'usuari.

Està pensat per ser utilitzat com a part d’un intèrpret del llenguatge G, amb suport per a operadors
unaris i binaris, composició de funcions, i estructures llistes. Aquest mòdul depèn del mòdul motor_g
per a la manipulació d'operadors i la codificació/descodificació de dades.
"""


from gVisitor import gVisitor
from motor_g import GestorOperadors, codifica_llista, descodifica_llista

class Visitor(gVisitor):
    """
    Classe que implementa el patró visitor per interpretar expressions del llenguatge J. Analitza la
    semàntica de les expressions a partir de visitar l'arbre de sintaxi generat per ANTLR. S'encarrega de crear
    la taula de variables, la taula de funcions, assignar memòria per a les variables, comprovar errors de tipus,
    i executar les expressions ajudant-se de la classe GestorOperadors per a les operacions.

    Aquesta classe hereta de gVisitor (generat per ANTLR) i redefineix els mètodes de visita necessaris.
    """

    def __init__(self):
        """
        Inicialitza una instància del visitor semàntic per al llenguatge J.
        Crea i inicialitza les taules de variables i funcions, una com la pila per a l'avaluació d'expressions,
        i el gestor d'operacions.
        """
        super().__init__()
        self.taula_variables = {}
        self.taula_funcions = {}
        self.pila = []
        self.gestor_operadors = GestorOperadors()

    def visitGenExpr(self, ctx):
        """
        Visita el node general (equival a una sentència genèrica) i imprimeix el resultat final.
        S'encarrega de mostrar quins possibles erros semàntics s'han trobat durant la visita.
        """
        try:
            self.visitChildren(ctx)
            resultat = self.pila.pop()
            print(descodifica_llista(resultat))
        except ValueError as ve:
            print(f"Error de valor: {ve}")
        except Exception as ex:
            print(f"Error durant l'execució: {ex}")

    def visitGenAssign(self, ctx):
        """
       Processa una assignació de variable: avalua l’expressió d'assignació
       i guarda el resultat a la taula de variables amb el nom corresponent.
       """
        [var, _, expr] = list(ctx.getChildren())
        self.visit(expr)
        self.taula_variables[var.getText()] = self.pila.pop()

    def visitGenFunc(self, ctx):
        """
       Processa una assignació de funció de forma mandrosa: guarda l'arbre de sintaxi a la taula
       de funcions amb el nom corresponent. Més tard, quan es cridi la funció, serà avaluat.
       """
        [func, _, expr] = list(ctx.getChildren())
        self.taula_funcions[func.getText()] = expr

    def visitExprOperBin(self, ctx):
        """
        Avalua una l'operació binària de dues expressions, notar que l'ordre de visita és primer
        l'expressió de la dreta, seguit de l'expressió de l'esquerra, i finalment l'operador.
        """
        [expr_esq, oper, expr_dreta] = list(ctx.getChildren())
        self.visit(expr_dreta)
        self.visit(expr_esq)
        self.visit(oper)

    def visitExprOperUn(self, ctx):
        """
        Avalua una l'operació unària d'una expressió, notar que l'ordre de visita és primer
        l'expressió i després l'operador.
        """
        [oper, expr] = list(ctx.getChildren())
        self.visit(expr)
        self.visit(oper)

    def visitExprLlista(self, ctx):
        """
        Avalua una llista de valors literals: codifica la llista corresponent als valors del node
        i l’emmagatzema a la pila.
        """
        nums = [node.getText() for node in list(ctx.getChildren())]
        self.pila.append(codifica_llista(nums))

    def visitExprVar(self, ctx):
        """
        Avalua una variable: cerca el valor corresponent a la taula de variables i el col·loca a la pila.
        """
        valor = self.taula_variables[ctx.getText()]
        self.pila.append(valor)

    def visitFuncComp(self, ctx):
        """
        Avalua una funció formada per la composició de dues funcions.
        Aquest node és visitat quan es crida una funció (no quan es defineix).
        Notar que l'ordre de visita és primer la funció de la dreta i després la de l'esquerra.
        """
        [func1, _, func2] = list(ctx.getChildren())
        self.visit(func2)
        self.visit(func1)

    def visitFuncOperBin(self, ctx):
        """
        Avalua una funció formada per una expressió i un operador binari.
        Aquest node és visitat quan es crida una funció (no quan es defineix).
        Notar que l'ordre de visita és primer l'expressió i després l'operador.
        """
        [expr, oper, _] = list(ctx.getChildren())
        self.visit(expr)
        self.visit(oper)

    def visitOperBin(self, ctx):
        """
        Aplica un operador binari als dos operands que es troben a la pila.
        Notar que el primer operand és el que es troba a la part superior de la pila.
        """
        primer_operand = self.pila.pop()
        segon_operand = self.pila.pop()
        func = self.gestor_operadors.obtenir_funcio(ctx.getText())
        resultat = func(primer_operand, segon_operand)
        self.pila.append(resultat)

    def visitOperUn(self, ctx):
        """
        Aplica un operador unari. Si l’operador és una funció definida per l’usuari, s’executa la seva
        expressió associada. Si no, s’obté una funció del GestorOperadors i s’aplica a l’operand extret de la pila.
        """
        oper = ctx.getText()
        if oper in self.taula_funcions:
            self.visit(self.taula_funcions[oper])
        else:
            operand = self.pila.pop()
            func = self.gestor_operadors.obtenir_funcio(oper)
            resultat = func(operand)
            self.pila.append(resultat)