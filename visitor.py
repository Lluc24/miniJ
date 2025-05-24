from gVisitor import gVisitor
from funcions import descodifica_llista, codifica_llista, obtenir_funcio

class Visitor(gVisitor):
    def __init__(self):
        super().__init__()
        self.taula_variables = {}
        self.taula_funcions = {}
        self.pila = []

    def visitGenExpr(self, ctx):
        self.visitChildren(ctx)
        resultat = self.pila.pop()
        print(descodifica_llista(resultat))

    # Visit a parse tree produced by exprsParser#genAssign.
    def visitGenAssign(self, ctx):
        [var, _, expr] = list(ctx.getChildren())
        self.visit(expr)
        self.taula_variables[var.getText()] = self.pila.pop()

    # Visit a parse tree produced by exprsParser#genFunc.
    def visitGenFunc(self, ctx):
        [func, _, expr] = list(ctx.getChildren())
        self.taula_funcions[func.getText()] = expr

    # Visit a parse tree produced by exprsParser#binOperExpr.
    def visitExprOperBin(self, ctx):
        [expr_esq, oper, expr_dreta] = list(ctx.getChildren())
        self.visit(expr_dreta)
        self.visit(expr_esq)
        self.visit(oper)

    # Visit a parse tree produced by exprsParser#unOperExpr.
    def visitExprOperUn(self, ctx):
        [oper, expr] = list(ctx.getChildren())
        self.visit(expr)
        self.visit(oper)

    # Visit a parse tree produced by exprsParser#listExpr.
    def visitExprLlista(self, ctx):
        nums = list(ctx.getChildren())
        self.pila.append(codifica_llista(nums))

    # Visit a parse tree produced by exprsParser#varExpr.
    def visitExprVar(self, ctx):
        valor = self.taula_variables[ctx.getText()]
        self.pila.append(valor)

    # Visit a parse tree produced by exprsParser#compFunc.
    def visitFuncComp(self, ctx):
        [func1, _, func2] = list(ctx.getChildren())
        self.visit(func2)
        self.visit(func1)

    # Visit a parse tree produced by exprsParser#binaryFunc.
    def visitFuncOperBin(self, ctx):
        [expr, oper, _] = list(ctx.getChildren())
        self.visit(expr)
        self.visit(oper)

    # Visit a parse tree produced by exprsParser#binaryOper.
    def visitOperBin(self, ctx):
        primer_operand = self.pila.pop()
        segon_operand = self.pila.pop()
        f = obtenir_funcio(ctx.getText())
        resultat = f(primer_operand, segon_operand)
        self.pila.append(resultat)

    # Visit a parse tree produced by exprsParser#unaryOper.
    def visitOperUn(self, ctx):
        oper = ctx.getText()
        if oper in self.taula_funcions:
            self.visit(self.taula_funcions[oper])
        else:
            operand = self.pila.pop()
            f = obtenir_funcio(oper)
            resultat = f(operand)
            self.pila.append(resultat)