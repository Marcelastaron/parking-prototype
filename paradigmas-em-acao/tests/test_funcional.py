import unittest
from datetime import datetime

from funcional import (
    Ticket, fechar_ticket, valor_a_pagar, valor_do_ticket, faturamento,
    faturamento_imperativo, faturamento_por_tipo, somar_recursivo, valor_carro,
)
from oo import Carro, Moto, Caminhonete


def hora(h, m):
    return datetime(2026, 11, 9, h, m)


class TestFuncional(unittest.TestCase):
    def test_tabela_entradas_saidas(self):
        casos = [
            (("CARRO", 10, False), 0.0),
            (("CARRO", 15, False), 0.0),
            (("CARRO", 16, False), 6.0),
            (("CARRO", 60, False), 6.0),
            (("CARRO", 61, False), 12.0),
            (("MOTO", 130, False), 9.0),
            (("CAMINHONETE", 125, False), 27.0),
            (("CARRO", 200, True), 0.0),
        ]
        for args, esperado in casos:
            with self.subTest(args=args):
                self.assertEqual(valor_a_pagar(*args), esperado)

    def test_imutabilidade(self):
        t0 = Ticket("ABC1D23", "CARRO", False, hora(8, 0))
        t1 = fechar_ticket(t0, hora(9, 0))
        self.assertIsNone(t0.saida)
        self.assertIsNotNone(t1.saida)
        with self.assertRaises(AttributeError):
            t0.placa = "XXX0X00"

    def test_pureza_mesma_entrada_mesma_saida(self):
        self.assertEqual(valor_a_pagar("MOTO", 90), valor_a_pagar("MOTO", 90))

    def test_faturamento_funcional_igual_imperativo(self):
        tickets = (
            fechar_ticket(Ticket("ABC1D23", "CARRO", False, hora(8, 0)), hora(10, 10)),
            fechar_ticket(Ticket("BRA2E19", "CARRO", True, hora(8, 10)), hora(11, 30)),
            fechar_ticket(Ticket("XYZ9K88", "MOTO", False, hora(8, 30)), hora(9, 15)),
            fechar_ticket(Ticket("QWE4R56", "CAMINHONETE", False, hora(8, 40)), hora(10, 45)),
        )
        self.assertEqual(faturamento(tickets), 48.0)
        self.assertEqual(faturamento_imperativo(tickets), 48.0)
        self.assertEqual(faturamento_por_tipo(tickets),
                         {"CARRO": 18.0, "MOTO": 3.0, "CAMINHONETE": 27.0})

    def test_recursao(self):
        self.assertEqual(somar_recursivo(()), 0.0)
        self.assertEqual(somar_recursivo((18.0, 0.0, 3.0, 27.0)), 48.0)

    def test_partial(self):
        self.assertEqual(valor_carro(130), 18.0)

    def test_equivalencia_com_versao_oo(self):
        """A regra de preço funcional deve coincidir com a da hierarquia OO."""
        pares = [(Carro("ABC1D23"), "CARRO"), (Moto("XYZ9K88"), "MOTO"),
                 (Caminhonete("QWE4R56"), "CAMINHONETE")]
        for veiculo, tipo in pares:
            for minutos in (0, 15, 16, 60, 61, 125, 130, 600):
                with self.subTest(tipo=tipo, minutos=minutos):
                    self.assertEqual(veiculo.calcular_valor(minutos),
                                     valor_a_pagar(tipo, minutos))


if __name__ == "__main__":
    unittest.main()
