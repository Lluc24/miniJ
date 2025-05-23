from exprsVisitor import exprsVisitor
import numpy as np
from generalTree import GeneralTree

def get_number(num_str):
    if num_str[0] == "_":
        return -int(num_str[1:])
    else:
        return int(num_str)

class TreeEval(exprsVisitor):

    def __init__(self):
        super().__init__()
        self.memory = {}

    # Visit a parse tree produced by exprsParser#genExpr.
    def visitGenExpr(self, ctx):
        expr_tree = self.visitChildren(ctx)
        print("Expression tree:", expr_tree)
        print("Expression evaluation:", expr_tree.get_evaluation())
        print(expr_tree.get_tree_view())

    # Visit a parse tree produced by exprsParser#genAssign.
    def visitGenAssign(self, ctx):
        [var, _, expr] = list(ctx.getChildren())
        var_str = var.getText()
        expr_tree = self.visit(expr)
        expr_eval = expr_tree.get_evaluation()

        self.memory[var_str] = expr_eval

        var_tree = GeneralTree(var_str, evaluation=var_str, color=True)
        result_tree = GeneralTree(':=', f'{var_str} := {expr_eval}', [var_tree, expr_tree], color=True)
        print(result_tree.get_tree_view())
        return result_tree

    # Visit a parse tree produced by exprsParser#binOperExpr.
    def visitBinOperExpr(self, ctx):
        [left_expr, operation, right_expr] = list(ctx.getChildren())
        right_tree = self.visit(right_expr)
        right_eval = right_tree.get_evaluation()
        left_tree = self.visit(left_expr)
        left_eval = left_tree.get_evaluation()
        op_str = operation.getText()

        if op_str == "+":
            result = np.add(left_eval, right_eval)
        elif op_str == "-":
            result = np.subtract(left_eval, right_eval)
        elif op_str == "*":
            result = np.multiply(left_eval, right_eval)
        elif op_str == "%":
            result = np.divide(left_eval, right_eval)
        elif op_str == "^":
            result = np.power(left_eval, right_eval)
        elif op_str == "|":
            result = np.mod(left_eval, right_eval)
        result_tree = GeneralTree(op_str, result, [left_tree, right_tree], color=True)
        return result_tree

    # Visit a parse tree produced by exprsParser#parExpr.
    def visitParExpr(self, ctx):
        [_, expr_list, _] = list(ctx.getChildren())
        expr_tree = self.visit(expr_list)
        left_par_tree = GeneralTree("(", "(", color=True)
        right_par_tree = GeneralTree(")", ")", color=True)
        result_tree = GeneralTree("parExpr", expr_tree.get_evaluation(), [left_par_tree, expr_tree, right_par_tree], color=True)
        return result_tree

    # Visit a parse tree produced by exprsParser#listExpr.
    def visitListExpr(self, ctx):
        expr_list = list(ctx.getChildren())
        nums = np.array([get_number(expr.getText()) for expr in expr_list], dtype=int)
        result_tree = GeneralTree("listExpr", nums, color=True)
        return result_tree

    # Visit a parse tree produced by exprsParser#varExpr.
    def visitVarExpr(self, ctx):
        var_str = ctx.getText()
        var_value = self.memory[var_str]
        result_tree = GeneralTree(var_str, var_value, color=True)
        return result_tree
