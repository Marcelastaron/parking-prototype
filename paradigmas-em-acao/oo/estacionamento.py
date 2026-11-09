"""Classe principal do protótipo OO (Etapa 3)."""
from datetime import datetime

from .ticket import Ticket


class ErroEstacionamento(Exception):
    """Erro base das regras do estacionamento."""


class SemVagaError(ErroEstacionamento):
    def __init__(self, tipo: str):
        super().__init__(f"Não há vaga {tipo} livre")
        self.tipo = tipo


class VeiculoJaEstacionadoError(ErroEstacionamento):
    pass


class VeiculoNaoEncontradoError(ErroEstacionamento):
    pass


class Estacionamento:
    """Coordena vagas e tickets. Os dados internos são privados."""

    def __init__(self, nome: str, vagas):
        self.__nome = nome
        self.__vagas = list(vagas)
        self.__abertos = {}      # placa -> Ticket
        self.__fechados = []     # tickets encerrados
        self.__proximo_codigo = 1

    @property
    def nome(self) -> str:
        return self.__nome

    @property
    def total_vagas(self) -> int:
        return len(self.__vagas)

    def vagas_livres(self, tipo: str = None) -> int:
        return sum(1 for v in self.__vagas if v.livre and (tipo is None or v.tipo == tipo))

    @property
    def taxa_ocupacao(self) -> float:
        ocupadas = self.total_vagas - self.vagas_livres()
        return ocupadas / self.total_vagas if self.total_vagas else 0.0

    def registrar_entrada(self, veiculo, quando: datetime) -> Ticket:
        if veiculo.placa in self.__abertos:
            raise VeiculoJaEstacionadoError(f"{veiculo.placa} já está no estacionamento")
        vaga = next((v for v in self.__vagas if v.livre and v.aceita(veiculo)), None)
        if vaga is None:
            raise SemVagaError(veiculo.tipo_vaga)
        vaga.ocupar(veiculo)
        ticket = Ticket(self.__proximo_codigo, veiculo, vaga, quando)
        self.__proximo_codigo += 1
        self.__abertos[veiculo.placa] = ticket
        return ticket

    def registrar_saida(self, placa: str, quando: datetime) -> Ticket:
        placa = placa.strip().upper().replace("-", "")
        ticket = self.__abertos.get(placa)
        if ticket is None:
            raise VeiculoNaoEncontradoError(f"{placa} não está no estacionamento")
        ticket.fechar(quando)
        ticket.vaga.liberar()
        del self.__abertos[placa]
        self.__fechados.append(ticket)
        return ticket

    @property
    def tickets_abertos(self) -> tuple:
        return tuple(self.__abertos.values())

    @property
    def tickets_fechados(self) -> tuple:
        return tuple(self.__fechados)

    def faturamento_total(self) -> float:
        return round(sum(t.valor for t in self.__fechados), 2)
