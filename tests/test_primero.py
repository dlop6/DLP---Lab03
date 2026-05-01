import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from contract import EPSILON
from primero import calcular_primero


# gramática 1: expresiones aritméticas con epsilon
# E → T E' | E' → + T E' | ε | T → F T' | T' → * F T' | ε | F → ( E ) | id
G1 = {
    "E":  [["T", "E'"]],
    "E'": [["+", "T", "E'"], [EPSILON]],
    "T":  [["F", "T'"]],
    "T'": [["*", "F", "T'"], [EPSILON]],
    "F":  [["(", "E", ")"], ["id"]],
}

# gramática 2: gramática simple sin epsilon
# S → a B | b A | A → a | a S | b A A | B → b | b S | a B B
G2 = {
    "S": [["a", "B"], ["b", "A"]],
    "A": [["a"], ["a", "S"], ["b", "A", "A"]],
    "B": [["b"], ["b", "S"], ["a", "B", "B"]],
}


class TestPrimeroGramatica1:
    def setup_method(self):
        self.primero = calcular_primero(G1)

    def test_primero_F(self):
        assert self.primero["F"] == {"(", "id"}

    def test_primero_T_prima(self):
        assert self.primero["T'"] == {"*", EPSILON}

    def test_primero_T(self):
        assert self.primero["T"] == {"(", "id"}

    def test_primero_E_prima(self):
        assert self.primero["E'"] == {"+", EPSILON}

    def test_primero_E(self):
        assert self.primero["E"] == {"(", "id"}


class TestPrimeroGramatica2:
    def setup_method(self):
        self.primero = calcular_primero(G2)

    def test_primero_S(self):
        assert self.primero["S"] == {"a", "b"}

    def test_primero_A(self):
        assert self.primero["A"] == {"a", "b"}

    def test_primero_B(self):
        assert self.primero["B"] == {"b", "a"}
