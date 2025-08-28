import unittest
from vacas import estado_vaca

class TestVacas(unittest.TestCase):
    def test_vaca_feliz(self):
        resultado = estado_vaca("Lola")
        self.assertEqual(resultado, "La vaca Lola está feliz 🐮")

if __name__ == "__main__":
    unittest.main()