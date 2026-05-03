# Lab 03 — Conjuntos Primero y Siguiente

Laboratorio de gramáticas libres de contexto: cálculo de **Primero** (`FIRST`) y **Siguiente** (`FOLLOW`) sobre la estructura `Gramatica` definida en `src/contract.py` (no terminales como llaves, producciones como listas de símbolos, `ε` como cadena literal).

## Estructura

| Ruta | Rol |
|------|-----|
| `src/contract.py` | Tipo `Gramatica`, `EPSILON`, utilidades (`get_no_terminales`, `get_terminales`). |
| `src/primero.py` | `calcular_primero` y `_primero_secuencia` (Primero de una secuencia; lo reutiliza Siguiente). |
| `src/siguiente.py` | `calcular_siguiente`. |
| `tests/test_primero.py` | Pruebas de Primero con las dos gramáticas finales. |
| `tests/test_siguiente.py` | Pruebas de Siguiente con las mismas gramáticas. |

## Cómo correr las pruebas

Desde la raíz del repo (con `pytest` instalado):

```bash
pytest tests/ -v
```

## Funcionamiento de Siguiente

`calcular_siguiente(gramatica, simbolo_inicial=None)` devuelve un `dict` por no terminal. Si no indicas `simbolo_inicial`, se toma el **primer** no terminal del diccionario (orden de inserción); en las pruebas se pasa explícitamente `"E"` o `"S"`.

Reglas implementadas:

1. **Símbolo inicial:** se agrega `$` al Siguiente del no terminal inicial.
2. **Forma general** `A → α B β` con `B` no terminal: al Siguiente de `B` se agrega **Primero(β)** sin `ε` (cubre β empezando en **terminal** u otro **no terminal** vía los conjuntos Primero).
3. **β vacío o Primero(β) contiene ε** (por ejemplo `B` al final de la producción, o β que puede anularse): al Siguiente de `B` se agrega **Siguiente(A)**.
4. El cálculo es por **punto fijo** hasta que no haya cambios, recorriendo todas las producciones y todas las posiciones de cada no terminal.

En resumen, Siguiente se apoya en **Primero** (incluido `_primero_secuencia` para el sufijo β) más la propagación desde la cabeza `A` cuando hace falta.

## Resultados de Siguiente (dos gramáticas finales)

**Gramática 1** (expresiones con `E`, `E'`, `T`, `T'`, `F`; axioma `E`):

| No terminal | Siguiente |
|---------------|-----------|
| `E`, `E'` | `$`, `)` |
| `T`, `T'` | `$`, `)`, `+` |
| `F` | `$`, `)`, `*`, `+` |

**Gramática 2** (`S → aB | bA`, `A` y `B` con recursión; axioma `S`):

| No terminal | Siguiente |
|---------------|-----------|
| `S`, `A`, `B` | `$`, `a`, `b` |

Los valores anteriores coinciden con las aserciones en `tests/test_siguiente.py`.
