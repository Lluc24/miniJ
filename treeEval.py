from exprsVisitor import exprsVisitor
import numpy as np
from generalTree import GeneralTree

def get_number(num_str):
    if num_str[0] == "_":
        return -int(num_str[1:])
    else:
        return int(num_str)

class TreeEval(exprsVisitor):

    # Visit a parse tree produced by exprsParser#genExpr.
    def visitGenExpr(self, ctx):
        expr_tree = self.visitChildren(ctx)
        print("Expression tree:", expr_tree)
        print("Expression evaluation:", expr_tree.get_evaluation())
        print(expr_tree.get_tree_view())

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
        elif op_str== "^":
            result = np.power(left_eval, right_eval)
        result_tree = GeneralTree(op_str, result, [left_tree, right_tree], color=True)
        return result_tree

    # Visit a parse tree produced by exprsParser#listExpr.
    def visitListExpr(self, ctx):
        [expr_list] = list(ctx.getChildren())
        tree = self.visit(expr_list)
        return tree

    # Visit a parse tree produced by exprsParser#buildList.
    def visitBuildList(self, ctx):
        [init, last] = list(ctx.getChildren())
        last_int = get_number(last.getText())
        init_tree = self.visit(init)
        last_tree = GeneralTree("last", last_int, color=False)

        init_list = init_tree.get_evaluation()
        built_list = np.append(init_list, last_int)
        result_tree = GeneralTree("buildList", built_list, [init_tree, last_tree], color=True)
        return result_tree

    # Visit a parse tree produced by exprsParser#baseList.
    def visitBaseList(self, ctx):
        [base] = list(ctx.getChildren())
        base_int = get_number(base.getText())
        base_tree = GeneralTree(f"baseList", np.array([base_int]), color=False)
        return base_tree
