from contract import Gramatica, EPSILON, get_no_terminales


def _primero_secuencia(
    secuencia: list[str],
    primero: dict[str, set[str]],
    no_terminales: set[str],
) -> set[str]:
    # calcula el conjunto primero de una secuencia de símbolos
    # esta función también la usa persona 2 para calcular siguiente
    resultado: set[str] = set()

    for simbolo in secuencia:
        if simbolo == EPSILON:
            resultado.add(EPSILON)
            break

        if simbolo not in no_terminales:
            # es terminal, se agrega directo y se corta
            resultado.add(simbolo)
            break

        # es no terminal, se agrega su primero sin epsilon
        resultado |= primero[simbolo] - {EPSILON}

        if EPSILON not in primero[simbolo]:
            # no puede derivar epsilon, se corta
            break
    else:
        # todos los símbolos pueden derivar epsilon
        resultado.add(EPSILON)

    return resultado


def calcular_primero(gramatica: Gramatica) -> dict[str, set[str]]:
    no_terminales = get_no_terminales(gramatica)
    primero: dict[str, set[str]] = {nt: set() for nt in no_terminales}

    # punto fijo: se itera hasta que no haya cambios en ningún conjunto
    hubo_cambio = True
    while hubo_cambio:
        hubo_cambio = False
        for no_terminal, producciones in gramatica.items():
            for produccion in producciones:
                nuevos = _primero_secuencia(produccion, primero, no_terminales)
                if not nuevos.issubset(primero[no_terminal]):
                    primero[no_terminal] |= nuevos
                    hubo_cambio = True

    return primero
