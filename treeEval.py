from exprsVisitor import exprsVisitor
from functions import get_function
import numpy as np

def decode_number(num_str):
    if num_str[0] == "_":
        return -int(num_str[1:])
    else:
        return int(num_str)

def encode_number(num):
    if num < 0:
        return "_" + str(-num)
    else:
        return str(num)

class TreeEval(exprsVisitor):

    def __init__(self):
        super().__init__()
        self.taula_variables = {}
        self.taula_funcions = {}
        self.pila = []

    # Visit a parse tree produced by exprsParser#genExpr.
    def visitGenExpr(self, ctx):
        self.visitChildren(ctx)
        resultat = self.pila.pop()
        print(" ".join(map(encode_number, resultat)))

    # Visit a parse tree produced by exprsParser#genAssign.
    def visitGenAssign(self, ctx):
        [var, _, expr] = list(ctx.getChildren())
        self.visit(expr)
        assig = self.pila.pop()
        self.taula_variables[var.getText()] = assig

    # Visit a parse tree produced by exprsParser#genFunc.
    def visitGenFunc(self, ctx):
        [func, _, expr] = list(ctx.getChildren())
        self.taula_funcions[func.getText()] = expr

    # Visit a parse tree produced by exprsParser#binOperExpr.
    def visitBinOperExpr(self, ctx):
        [expr_esq, oper, expr_dreta] = list(ctx.getChildren())
        self.visit(expr_dreta)
        self.visit(expr_esq)
        self.visit(oper)

    # Visit a parse tree produced by exprsParser#unOperExpr.
    def visitUnOperExpr(self, ctx):
        [oper, expr] = list(ctx.getChildren())
        self.visit(expr)
        self.visit(oper)

    # TODO: Es pot suprimir aquesta funcio?
    # Visit a parse tree produced by exprsParser#parExpr.
    def visitParExpr(self, ctx):
        [_, expr_list, _] = list(ctx.getChildren())
        self.visit(expr_list)

    # Visit a parse tree produced by exprsParser#listExpr.
    def visitListExpr(self, ctx):
        nums = list(ctx.getChildren())
        nums = np.array([decode_number(num.getText()) for num in nums], dtype=int)
        self.pila.append(nums)

    # Visit a parse tree produced by exprsParser#varExpr.
    def visitVarExpr(self, ctx):
        valor = self.taula_variables[ctx.getText()]
        self.pila.append(valor)

    # Visit a parse tree produced by exprsParser#compFunc.
    def visitCompFunc(self, ctx):
        [func1, _, func2] = list(ctx.getChildren())
        self.visit(func2)
        self.visit(func1)

    # Visit a parse tree produced by exprsParser#binaryFunc.
    def visitBinaryFunc(self, ctx):
        [expr, oper, _] = list(ctx.getChildren())
        self.visit(expr)
        self.visit(oper)

    # Visit a parse tree produced by exprsParser#unaryFunc.
    def visitUnaryFunc(self, ctx):
        self.visitChildren(ctx)

    # Visit a parse tree produced by exprsParser#binaryOper.
    def visitBinaryOper(self, ctx):
        primer_operand = self.pila.pop()
        segon_operand = self.pila.pop()
        oper = ctx.getText()
        f = get_function(oper)
        resultat = f(primer_operand, segon_operand)
        self.pila.append(resultat)

    # Visit a parse tree produced by exprsParser#unaryOper.
    def visitUnaryOper(self, ctx):
        oper = ctx.getText()
        if oper in self.taula_funcions:
            self.visit(self.taula_funcions[oper])
        else:
            operand = self.pila.pop()
            f = get_function(oper)
            resultat = f(operand)
            self.pila.append(resultat)