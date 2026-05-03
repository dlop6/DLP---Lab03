from contract import Gramatica, EPSILON, get_no_terminales
from primero import calcular_primero, _primero_secuencia


def calcular_siguiente(
    gramatica: Gramatica,
    simbolo_inicial: str | None = None,
) -> dict[str, set[str]]:
    # FOLLOW por no terminal; FIRST(β) vía _primero_secuencia
    primero = calcular_primero(gramatica)
    no_terminales = get_no_terminales(gramatica)
    if simbolo_inicial is None:
        simbolo_inicial = next(iter(gramatica))

    siguiente: dict[str, set[str]] = {nt: set() for nt in no_terminales}
    siguiente[simbolo_inicial].add("$")

    hubo_cambio = True
    while hubo_cambio:
        hubo_cambio = False
        for A, producciones in gramatica.items():
            for produccion in producciones:
                for i, B in enumerate(produccion):
                    if B not in no_terminales:
                        continue
                    beta = produccion[i + 1 :]
                    first_beta = _primero_secuencia(beta, primero, no_terminales)

                    for b in first_beta - {EPSILON}:
                        if b not in siguiente[B]:
                            siguiente[B].add(b)
                            hubo_cambio = True

                    if EPSILON in first_beta:
                        for f in siguiente[A]:
                            if f not in siguiente[B]:
                                siguiente[B].add(f)
                                hubo_cambio = True

    return siguiente
