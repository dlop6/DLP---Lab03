# contrato compartido entre los tres módulos del lab
# define la estructura de datos de la gramática y utilerías básicas

from typing import TypeAlias

# una gramática es un dict donde cada llave es un no terminal y
# su valor es una lista de producciones (cada producción es una lista de símbolos)
# ej: {"E": [["T", "E'"], ...], "E'": [["+", "T", "E'"], ["ε"]], ...}
Gramatica: TypeAlias = dict[str, list[list[str]]]

EPSILON = "ε"


def get_no_terminales(gramatica: Gramatica) -> set[str]:
    return set(gramatica.keys())


def get_terminales(gramatica: Gramatica) -> set[str]:
    no_terminales = get_no_terminales(gramatica)
    terminales: set[str] = set()
    for producciones in gramatica.values():
        for produccion in producciones:
            for simbolo in produccion:
                if simbolo not in no_terminales and simbolo != EPSILON:
                    terminales.add(simbolo)
    return terminales


# gramática de ejemplo para que persona 2 y 3 puedan trabajar sin depender de nadie
# E → T E'  |  E' → + T E' | ε  |  T → F T'  |  T' → * F T' | ε  |  F → ( E ) | id
GRAMATICA_EJEMPLO: Gramatica = {
    "E":  [["T", "E'"]],
    "E'": [["+", "T", "E'"], [EPSILON]],
    "T":  [["F", "T'"]],
    "T'": [["*", "F", "T'"], [EPSILON]],
    "F":  [["(", "E", ")"], ["id"]],
}
