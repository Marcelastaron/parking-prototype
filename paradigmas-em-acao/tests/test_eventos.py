import unittest
from datetime import datetime

from eventos import (
    BarramentoEventos, Portaria,
    VEICULO_ENTROU, VEICULO_SAIU, LOTACAO_ALTA, VAGAS_ESGOTADAS,
)
from oo import Carro, Moto, Vaga, Estacionamento


def hora(h, m):
    return datetime(2026, 11, 9, h, m)


class TestEventos(unittest.TestCase):
    def setUp(self):
        vagas = [Vaga(1, "COMUM"), Vaga(2, "MOTO")]
        self.est = Estacionamento("Teste", vagas)
        self.bus = BarramentoEventos()
        self.registro = []
        for ev in (VEICULO_ENTROU, VEICULO_SAIU, LOTACAO_ALTA, VAGAS_ESGOTADAS):
            self.bus.inscrever(ev, lambda e, d: self.registro.append(e))
        self.portaria = Portaria(self.est, self.bus)

    def test_entrada_publica_evento(self):
        self.portaria.entrada(Carro("ABC1D23"), hora(8, 0))
        self.assertEqual(self.registro[0], VEICULO_ENTROU)

    def test_lotacao_alta(self):
        self.portaria.entrada(Carro("ABC1D23"), hora(8, 0))   # 50%
        self.portaria.entrada(Moto("XYZ9K88"), hora(8, 5))    # 100%
        self.assertIn(LOTACAO_ALTA, self.registro)

    def test_vagas_esgotadas(self):
        self.portaria.entrada(Carro("ABC1D23"), hora(8, 0))
        resultado = self.portaria.entrada(Carro("DEF2G34"), hora(8, 5))
        self.assertIsNone(resultado)
        self.assertIn(VAGAS_ESGOTADAS, self.registro)

    def test_saida_publica_evento_com_ticket(self):
        capturado = []
        self.bus.inscrever(VEICULO_SAIU, lambda e, d: capturado.append(d["ticket"].valor))
        self.portaria.entrada(Carro("ABC1D23"), hora(8, 0))
        self.portaria.saida("ABC1D23", hora(10, 10))
        self.assertEqual(capturado, [18.0])


if __name__ == "__main__":
    unittest.main()
