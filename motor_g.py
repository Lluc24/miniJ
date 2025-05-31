"""
Mòdul encarregat d'encapsular la lògica operacional del llenguatge G (versió simplificada de J).

Inclou tant la implementació de funcions mitjançant la classe GestorOperadors
com la codificació/descodificació d'enters entre el format G i codificació interna.

Com a codificació interna utilitza matrius d'una dimensió de NumPy d'enters.
"""
import numpy as np


class GestorOperadors:
    """
    Aquesta classe encapsula el comportament dels operadors de G.
    En concret, mitjançant el mètode obtenir_funcio, retorna funcions que
    implementen el comportament dels operadors passats com a paràmetres.
    """

    def __init__(self):
        """
        Inicialitza el gestor amb un mapa d'operadors del llenguatge G a funcions de NumPy.
        Diferencia els operadors binaris i unaris, i els agrupa en diccionaris.
        Associa operadors binaris i unaris a funcions de NumPy que implementen el seu comportament.
        """
        self.mapa_funcions_bin = {
            '+': np.add,
            '-': np.subtract,
            '*': np.multiply,
            '%': np.floor_divide,
            '^': np.power,
            '|': lambda x, y: np.mod(y, x),
            '>': lambda x, y: np.greater(x, y).astype(int),
            '<': lambda x, y: np.less(x, y).astype(int),
            '>=': lambda x, y: np.greater_equal(x, y).astype(int),
            '<=': lambda x, y: np.less_equal(x, y).astype(int),
            '=': lambda x, y: np.equal(x, y).astype(int),
            '<>': lambda x, y: np.not_equal(x, y).astype(int),
            ',': lambda x, y: np.concatenate((x, y), axis=0),
            '#': lambda x, y: y[x.astype(bool)],
            '{': lambda x, y: y[x],
        }

        self.mapa_funcions_un = {
            'i.': np.arange,
            '#': lambda x: np.array([np.size(x)]),
            ']': lambda x: x,
        }

    def obtenir_funcio(self, operador):
        """
        Retorna una funció Python callable associada a un operador de G,
        incloent modificadors com ':', '/', '~', i tractament especial de '#'.
        """
        if operador == '#':
            return self._funcio_cardinalitat_variable
        elif operador.endswith(':'):
            f = self.obtenir_funcio(operador[:-1])
            return lambda  x: f(x, x)
        elif operador.endswith('/'):
            f = self.obtenir_funcio(operador[:-1])
            return lambda x: np.array([self._fold(f, x)])
        elif operador.endswith('~'):
            f = self.obtenir_funcio(operador[:-1])
            return lambda x, y: f(y, x)
        elif operador in self.mapa_funcions_bin:
            if operador == '{' or operador == ',': # No tenen comprovació de llargada
                return self.mapa_funcions_bin[operador]
            else:
                return self._comprovacio_llargada(self.mapa_funcions_bin[operador])
        elif operador in self.mapa_funcions_un:
            return self.mapa_funcions_un[operador]
        else:
            raise ValueError(f"operador desconegut '{operador}'")

    def _funcio_cardinalitat_variable(self, *args):
        """
        Implementa '#' en mode una o dues aritats.
        """
        if len(args) == 1:
            return self.mapa_funcions_un['#'](*args)
        else:
            return self.mapa_funcions_bin['#'](*args)

    def _comprovacio_llargada(self, func):
        """
        Retorna la funció passada com a paràmetre afegint comprovació de llargades.
        Utilitza clausura de funcions.
        """
        def aplicacio_segura(x, y):
            if np.size(x) == np.size(y) or np.size(x) == 1 or np.size(y) == 1:
                return func(x, y)
            else:
                raise ValueError("length error")
        return aplicacio_segura

    def _fold(self, func, x: np.ndarray):
        return x[0] if np.size(x) == 1 else func(x[0], self._fold(func, x[1:]))

def codifica_llista(llista: list[str]) -> np.ndarray:
    """
    Converteix una cadena G en una matriu d'una dimensió
    de numpy (codificació interna dels elements).
    """
    codifica_elem = lambda e: -int(e[1:]) if e.startswith("_") else int(e)
    return np.array(list(map(codifica_elem, llista)))


def descodifica_llista(llista: np.ndarray) -> str:
    """
    Descodifica una matriu d'una dimensió de numpy (codificació interna dels elements)
    a una cadena segons la notació en G.
    """
    codifica_elem = lambda e: f"_{-e}" if e < 0 else str(e)
    return " ".join(map(codifica_elem, llista))
