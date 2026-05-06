from __future__ import annotations

import argparse

from contract import EPSILON, Gramatica, get_terminales
from primero import calcular_primero
from siguiente import calcular_siguiente

GRAMATICA_1: Gramatica = {
    "E": [["T", "E'"]],
    "E'": [["+", "T", "E'"], [EPSILON]],
    "T": [["F", "T'"]],
    "T'": [["*", "F", "T'"], [EPSILON]],
    "F": [["(", "E", ")"], ["id"]],
}

GRAMATICA_2: Gramatica = {
    "S": [["a", "B"], ["b", "A"]],
    "A": [["a"], ["a", "S"], ["b", "A", "A"]],
    "B": [["b"], ["b", "S"], ["a", "B", "B"]],
}

GRAMATICAS_PRUEBA: dict[str, tuple[str, Gramatica, str]] = {
    "1": ("Expresiones aritmeticas", GRAMATICA_1, "E"),
    "2": ("Recursion simple", GRAMATICA_2, "S"),
}

EPSILON_ALIASES = {"epsilon", "eps"}


def _es_epsilon(texto: str) -> bool:
    return texto == EPSILON or texto.lower() in EPSILON_ALIASES


def _normalizar_simbolo(simbolo: str) -> str:
    if _es_epsilon(simbolo):
        return EPSILON
    return simbolo


def _tokenizar_produccion(texto: str) -> list[str]:
    limpio = texto.strip()
    if not limpio:
        return [EPSILON]

    if _es_epsilon(limpio):
        return [EPSILON]

    tokens = limpio.split()
    if any(_es_epsilon(token) for token in tokens):
        raise ValueError(
            "La produccion con epsilon debe ir sola, ejemplo: A -> epsilon"
        )

    return [_normalizar_simbolo(token) for token in tokens]


def _split_flecha(linea: str) -> tuple[str, str]:
    if "->" in linea:
        lhs, rhs = linea.split("->", 1)
        return lhs.strip(), rhs.strip()
    if "::=" in linea:
        lhs, rhs = linea.split("::=", 1)
        return lhs.strip(), rhs.strip()
    raise ValueError("Formato invalido. Use '->' o '::='.")


def parsear_gramatica(lineas: list[str]) -> tuple[Gramatica, str]:
    gramatica: Gramatica = {}
    simbolo_inicial: str | None = None

    for linea in lineas:
        limpia = linea.strip()
        if not limpia or limpia.startswith("#"):
            continue

        lhs, rhs = _split_flecha(limpia)
        if not lhs:
            raise ValueError("No terminal vacio en el lado izquierdo.")

        if simbolo_inicial is None:
            simbolo_inicial = lhs

        producciones = []
        for parte in rhs.split("|"):
            producciones.append(_tokenizar_produccion(parte))

        gramatica.setdefault(lhs, []).extend(producciones)

    if not gramatica:
        raise ValueError("No se ingreso ninguna produccion valida.")

    return gramatica, simbolo_inicial or next(iter(gramatica))


def _leer_gramatica_consola() -> tuple[Gramatica, str]:
    print("Ingrese producciones, una por linea (A -> alpha | beta).")
    print("Use espacios entre simbolos. Epsilon: epsilon o eps.")
    print("Linea vacia para terminar.\n")

    lineas: list[str] = []
    while True:
        try:
            linea = input()
        except EOFError:
            break
        if not linea.strip():
            break
        lineas.append(linea)

    return parsear_gramatica(lineas)


def _cargar_gramatica_archivo(ruta: str) -> tuple[Gramatica, str]:
    with open(ruta, "r", encoding="utf-8") as archivo:
        lineas = archivo.readlines()
    return parsear_gramatica(lineas)


def _orden_simbolo(simbolo: str) -> tuple[int, str]:
    if simbolo == EPSILON:
        return (1, "")
    if simbolo == "$":
        return (2, "")
    return (0, simbolo)


def _mostrar_simbolo(simbolo: str) -> str:
    if simbolo == EPSILON:
        return "epsilon"
    return simbolo


def _formatear_lista(simbolos: list[str]) -> str:
    return "{ " + ", ".join(_mostrar_simbolo(simbolo) for simbolo in simbolos) + " }"


def _formatear_conjunto(simbolos: set[str]) -> str:
    ordenados = sorted(simbolos, key=_orden_simbolo)
    return _formatear_lista(ordenados)


def _imprimir_gramatica(gramatica: Gramatica) -> None:
    for no_terminal, producciones in gramatica.items():
        rhs = " | ".join(
            _mostrar_simbolo(p[0]) if len(p) == 1 and p[0] == EPSILON else " ".join(p)
            for p in producciones
        )
        print(f"{no_terminal} -> {rhs}")


def _imprimir_resultados(gramatica: Gramatica, simbolo_inicial: str) -> None:
    print("\n==== Gramatica ====")
    _imprimir_gramatica(gramatica)

    no_terminales = list(gramatica.keys())
    terminales = sorted(get_terminales(gramatica), key=_orden_simbolo)

    print(f"\nSimbolo inicial: {simbolo_inicial}")
    print("No terminales:", _formatear_lista(no_terminales))
    print("Terminales:", _formatear_lista(terminales))

    primero = calcular_primero(gramatica)
    siguiente = calcular_siguiente(gramatica, simbolo_inicial=simbolo_inicial)

    print("\nPrimero:")
    for no_terminal in no_terminales:
        print(f"  FIRST({no_terminal}) = {_formatear_conjunto(primero[no_terminal])}")

    print("\nSiguiente:")
    for no_terminal in no_terminales:
        print(f"  FOLLOW({no_terminal}) = {_formatear_conjunto(siguiente[no_terminal])}")


def _seleccionar_gramatica_interactiva() -> tuple[Gramatica, str]:
    while True:
        print("Opciones:")
        print("  1) Gramatica de prueba 1 (expresiones)")
        print("  2) Gramatica de prueba 2 (recursion)")
        print("  3) Ingresar gramatica manual")
        opcion = input("Opcion [1-3]: ").strip()

        if opcion in GRAMATICAS_PRUEBA:
            _, gramatica, simbolo_inicial = GRAMATICAS_PRUEBA[opcion]
            return gramatica, simbolo_inicial

        if opcion == "3":
            try:
                return _leer_gramatica_consola()
            except ValueError as exc:
                print(f"Error: {exc}")
                continue

        print("Opcion invalida.\n")


def _preguntar_continuar() -> bool:
    respuesta = input("Procesar otra gramatica? [s/N]: ").strip().lower()
    return respuesta == "s"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Calculo de Primero y Siguiente para una gramatica."
    )
    parser.add_argument(
        "--demo",
        choices=sorted(GRAMATICAS_PRUEBA.keys()),
        help="Ejecuta con una gramatica de prueba (1 o 2).",
    )
    parser.add_argument(
        "--archivo",
        help="Carga la gramatica desde un archivo de texto.",
    )

    args = parser.parse_args()

    if args.demo:
        _, gramatica, simbolo_inicial = GRAMATICAS_PRUEBA[args.demo]
        _imprimir_resultados(gramatica, simbolo_inicial)
        return 0

    if args.archivo:
        try:
            gramatica, simbolo_inicial = _cargar_gramatica_archivo(args.archivo)
        except (OSError, ValueError) as exc:
            print(f"Error al leer el archivo: {exc}")
            return 1
        _imprimir_resultados(gramatica, simbolo_inicial)
        return 0

    while True:
        gramatica, simbolo_inicial = _seleccionar_gramatica_interactiva()
        _imprimir_resultados(gramatica, simbolo_inicial)
        if not _preguntar_continuar():
            break

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
