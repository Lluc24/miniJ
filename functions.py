from operator import add, sub, mul, floordiv, pow, mod
from functools import reduce
import numpy as np




class Function:
    def dual_function(*args):
        if len(args) == 1:
            result = np.array([np.size(*args)])
        elif len(args) == 2:
            result = args[1][args[0].astype(bool)]
        return result

    funcs_map = {
        '+': add,
        '-': sub,
        '*': mul,
        '%': floordiv,
        '^': pow,
        '|': lambda x, y: mod(y, x),
        '>': lambda x, y: (x > y).astype(int),
        '<': lambda x, y: (x < y).astype(int),
        '>=': lambda x, y: (x >= y).astype(int),
        '<=': lambda x, y: (x <= y).astype(int),
        '=': lambda x, y: (x == y).astype(int),
        '<>': lambda x, y: (x != y).astype(int),
        ',': lambda x, y: np.concatenate((x, y), axis=0),
        ']': lambda x: x,
        '#': dual_function,
        '{': lambda x, y: y[x],
        'i.': lambda x: np.arange(x),
    }

def get_function(operator):
    if operator[-1] == ":":
        func = lambda x: Function.funcs_map[operator[:-1]](x, x)
    elif operator[-1] == "/":
        func = lambda x: np.array([reduce(Function.funcs_map[operator[:-1]], x)])
    elif operator[-1] == "~":
        func = lambda x, y: Function.funcs_map[operator[:-1]](y, x)
    else:
        func = Function.funcs_map[operator]
    return func