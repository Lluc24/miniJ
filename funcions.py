from functools import reduce
import numpy as np


class Funcio:
    def funcio_dual(*args):
        if len(args) == 1:
            return np.array([np.size(*args)])
        else:
            return args[1][args[0].astype(bool)]

    mapa_funcions = {
        '+': lambda x, y: np.add(x, y),
        '-': lambda x, y: np.subtract(x, y),
        '*': lambda x, y: np.multiply(x, y),
        '%': lambda x, y: np.floor_divide(x, y),
        '^': lambda x, y: np.power(x, y),
        '|': lambda x, y: np.mod(y, x),
        '>': lambda x, y: np.greater(x, y).astype(int),
        '<': lambda x, y: np.less(x, y).astype(int),
        '>=': lambda x, y: np.greater_equal(x, y).astype(int),
        '<=': lambda x, y: np.less_equal(x, y).astype(int),
        '=': lambda x, y: np.equal(x, y).astype(int),
        '<>': lambda x, y: np.not_equal(x, y).astype(int),
        ',': lambda x, y: np.concatenate((x, y), axis=0),
        ']': lambda x: x,
        '#': funcio_dual,
        '{': lambda x, y: y[x],
        'i.': lambda x: np.arange(x),
    }

def obtenir_funcio(operador):
    inici, ultim = operador[:-1], operador[-1]
    if ultim == ":":
        return lambda x: Funcio.mapa_funcions[inici](x, x)
    elif ultim == "/":
        return lambda x: np.array([reduce(Funcio.mapa_funcions[inici], x)])
    elif ultim == "~":
        return lambda x, y: Funcio.mapa_funcions[inici](y, x)
    else:
        return Funcio.mapa_funcions[operador]

def descodifica_elem(num):
    if num[0] == "_":
        return -int(num[1:])
    else:
        return int(num)

def codifica_elem(num):
    if num < 0:
        return "_" + str(-num)
    else:
        return str(num)

def codifica_llista(llista):
    return np.array([descodifica_elem(elem.getText()) for elem in llista])

def descodifica_llista(llista):
    return " ".join(map(codifica_elem, llista))