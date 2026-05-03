import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from contract import EPSILON
from siguiente import calcular_siguiente

# mismas gramáticas finales que en test_primero
G1 = {
    "E": [["T", "E'"]],
    "E'": [["+", "T", "E'"], [EPSILON]],
    "T": [["F", "T'"]],
    "T'": [["*", "F", "T'"], [EPSILON]],
    "F": [["(", "E", ")"], ["id"]],
}

G2 = {
    "S": [["a", "B"], ["b", "A"]],
    "A": [["a"], ["a", "S"], ["b", "A", "A"]],
    "B": [["b"], ["b", "S"], ["a", "B", "B"]],
}


class TestSiguienteGramatica1:
    def setup_method(self):
        self.siguiente = calcular_siguiente(G1, simbolo_inicial="E")

    def test_siguiente_E(self):
        assert self.siguiente["E"] == {"$", ")"}

    def test_siguiente_E_prima(self):
        assert self.siguiente["E'"] == {"$", ")"}

    def test_siguiente_T(self):
        assert self.siguiente["T"] == {"$", ")", "+"}

    def test_siguiente_T_prima(self):
        assert self.siguiente["T'"] == {"$", ")", "+"}

    def test_siguiente_F(self):
        assert self.siguiente["F"] == {"$", ")", "*", "+"}


class TestSiguienteGramatica2:
    def setup_method(self):
        self.siguiente = calcular_siguiente(G2, simbolo_inicial="S")

    def test_siguiente_S(self):
        assert self.siguiente["S"] == {"$", "a", "b"}

    def test_siguiente_A(self):
        assert self.siguiente["A"] == {"$", "a", "b"}

    def test_siguiente_B(self):
        assert self.siguiente["B"] == {"$", "a", "b"}
