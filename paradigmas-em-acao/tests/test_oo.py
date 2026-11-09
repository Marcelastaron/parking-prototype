import unittest
from datetime import datetime

from oo import (
    Veiculo, Carro, Moto, Caminhonete, Vaga, Estacionamento,
    SemVagaError, VeiculoJaEstacionadoError, VeiculoNaoEncontradoError,
)


def hora(h, m):
    return datetime(2026, 11, 9, h, m)


def novo_estacionamento():
    vagas = [Vaga(1, "COMUM"), Vaga(2, "MOTO"), Vaga(3, "GRANDE")]
    return Estacionamento("Teste", vagas)


class TestVeiculos(unittest.TestCase):
    def test_classe_abstrata_nao_instancia(self):
        with self.assertRaises(TypeError):
            Veiculo("ABC1D23")

    def test_placa_invalida(self):
        with self.assertRaises(ValueError):
            Carro("123")

    def test_encapsulamento_placa_somente_leitura(self):
        c = Carro("abc-1d23")
        self.assertEqual(c.placa, "ABC1D23")
        with self.assertRaises(AttributeError):
            c.placa = "ZZZ9Z99"

    def test_polimorfismo_tarifas(self):
        self.assertEqual(Carro("ABC1D23").calcular_valor(130), 18.0)
        self.assertEqual(Moto("XYZ9K88").calcular_valor(130), 9.0)
        self.assertEqual(Caminhonete("QWE4R56").calcular_valor(125), 27.0)

    def test_tolerancia_e_hora_iniciada(self):
        c = Carro("ABC1D23")
        self.assertEqual(c.calcular_valor(15), 0.0)
        self.assertEqual(c.calcular_valor(16), 6.0)
        self.assertEqual(c.calcular_valor(60), 6.0)
        self.assertEqual(c.calcular_valor(61), 12.0)

    def test_mensalista_nao_paga(self):
        self.assertEqual(Carro("ABC1D23", mensalista=True).calcular_valor(500), 0.0)


class TestEstacionamento(unittest.TestCase):
    def test_fluxo_entrada_saida(self):
        est = novo_estacionamento()
        est.registrar_entrada(Carro("ABC1D23"), hora(8, 0))
        self.assertEqual(est.vagas_livres("COMUM"), 0)
        t = est.registrar_saida("ABC1D23", hora(10, 10))
        self.assertEqual(t.valor, 18.0)
        self.assertEqual(est.vagas_livres("COMUM"), 1)
        self.assertEqual(est.faturamento_total(), 18.0)

    def test_sem_vaga(self):
        est = novo_estacionamento()
        est.registrar_entrada(Carro("ABC1D23"), hora(8, 0))
        with self.assertRaises(SemVagaError):
            est.registrar_entrada(Carro("DEF2G34"), hora(8, 5))

    def test_veiculo_duplicado(self):
        est = novo_estacionamento()
        est.registrar_entrada(Carro("ABC1D23"), hora(8, 0))
        with self.assertRaises(VeiculoJaEstacionadoError):
            est.registrar_entrada(Carro("ABC1D23"), hora(8, 5))

    def test_saida_inexistente(self):
        with self.assertRaises(VeiculoNaoEncontradoError):
            novo_estacionamento().registrar_saida("ABC1D23", hora(9, 0))

    def test_vaga_correta_por_tipo(self):
        est = novo_estacionamento()
        t = est.registrar_entrada(Moto("XYZ9K88"), hora(8, 0))
        self.assertEqual(t.vaga.tipo, "MOTO")

    def test_saida_antes_da_entrada(self):
        est = novo_estacionamento()
        est.registrar_entrada(Carro("ABC1D23"), hora(9, 0))
        with self.assertRaises(ValueError):
            est.registrar_saida("ABC1D23", hora(8, 0))


if __name__ == "__main__":
    unittest.main()
