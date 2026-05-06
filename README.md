# Lab 03 — Primero y Siguiente

Integrantes: Diego Lopez #23747, Jennifer Toxcon #21276, Roberto Barreda #23354

Objetivo: calcular los conjuntos Primero y Siguiente para una gramatica libre de contexto.
El programa permite ingresar la gramatica, identificar terminales y no terminales, y mostrar resultados claros.
No se usan librerias externas para Primero o Siguiente.

## Uso rapido

```bash
python src/main.py
```

Gramaticas de prueba o desde archivo:

```bash
python src/main.py --demo 1
python src/main.py --demo 2
python src/main.py --archivo docs/gramatica_1.txt
```

## Formato de entrada

- Una produccion por linea: A -> alpha | beta
- Usa espacios entre simbolos.
- Para vacio, usa epsilon o eps.
- Una linea vacia termina el ingreso.

## Gramaticas y salida

- [docs/gramatica_1.txt](docs/gramatica_1.txt)
- [docs/gramatica_2.txt](docs/gramatica_2.txt)
- [docs/salida_ejemplo.txt](docs/salida_ejemplo.txt)

## Video

Link: (pendiente)
