"""Hierarquia de veículos do estacionamento (Etapas 2 e 3 - Programação Orientada a Objetos).

Conceitos demonstrados neste módulo:
- Abstração: ``Veiculo`` é uma classe abstrata (não pode ser instanciada).
- Encapsulamento: placa e condição de mensalista são atributos privados,
  acessíveis somente por propriedades somente-leitura.
- Herança/especialização: ``Carro``, ``Moto`` e ``Caminhonete`` herdam de ``Veiculo``.
- Polimorfismo: cada subclasse sobrescreve ``tarifa_hora`` e ``tipo_vaga``; o método
  ``calcular_valor`` (herdado) produz resultados diferentes conforme o objeto.
"""
import re
from abc import ABC, abstractmethod
from math import ceil

# Padrão antigo (ABC1234) e Mercosul (ABC1D23)
PADRAO_PLACA = re.compile(r"^[A-Z]{3}[0-9][A-Z0-9][0-9]{2}$")
TOLERANCIA_MINUTOS = 15


class Veiculo(ABC):
    """Abstração de um veículo que utiliza o estacionamento."""

    def __init__(self, placa: str, mensalista: bool = False):
        placa = placa.strip().upper().replace("-", "")
        if not PADRAO_PLACA.match(placa):
            raise ValueError(f"Placa inválida: {placa!r}")
        self.__placa = placa
        self.__mensalista = bool(mensalista)

    # ---- encapsulamento: acesso somente leitura -------------------------
    @property
    def placa(self) -> str:
        return self.__placa

    @property
    def mensalista(self) -> bool:
        return self.__mensalista

    # ---- pontos de especialização (polimorfismo) ------------------------
    @property
    @abstractmethod
    def tarifa_hora(self) -> float:
        """Valor cobrado por hora iniciada (R$)."""

    @property
    @abstractmethod
    def tipo_vaga(self) -> str:
        """Tipo de vaga que o veículo precisa: COMUM, MOTO ou GRANDE."""

    # ---- comportamento comum --------------------------------------------
    @staticmethod
    def horas_cobradas(minutos: int) -> int:
        """Até 15 min não se paga; depois, cobra-se por hora iniciada."""
        if minutos <= TOLERANCIA_MINUTOS:
            return 0
        return ceil(minutos / 60)

    def calcular_valor(self, minutos: int) -> float:
        """Valor a pagar pela permanência. Mensalista não paga."""
        if minutos < 0:
            raise ValueError("Permanência não pode ser negativa")
        if self.__mensalista:
            return 0.0
        return round(self.horas_cobradas(minutos) * self.tarifa_hora, 2)

    def __str__(self) -> str:
        extra = " (mensalista)" if self.__mensalista else ""
        return f"{self.__class__.__name__} {self.__placa}{extra}"


class Carro(Veiculo):
    @property
    def tarifa_hora(self) -> float:
        return 6.0

    @property
    def tipo_vaga(self) -> str:
        return "COMUM"


class Moto(Veiculo):
    @property
    def tarifa_hora(self) -> float:
        return 3.0

    @property
    def tipo_vaga(self) -> str:
        return "MOTO"


class Caminhonete(Veiculo):
    @property
    def tarifa_hora(self) -> float:
        return 9.0

    @property
    def tipo_vaga(self) -> str:
        return "GRANDE"
