"""Ticket de permanência (Etapa 2/3 - POO)."""
from datetime import datetime


class Ticket:
    """Registra a entrada, a vaga usada e, ao fechar, a saída e o valor cobrado."""

    def __init__(self, codigo: int, veiculo, vaga, entrada: datetime):
        self.__codigo = codigo
        self.__veiculo = veiculo
        self.__vaga = vaga
        self.__entrada = entrada
        self.__saida = None
        self.__valor = None

    @property
    def codigo(self) -> int:
        return self.__codigo

    @property
    def veiculo(self):
        return self.__veiculo

    @property
    def vaga(self):
        return self.__vaga

    @property
    def entrada(self) -> datetime:
        return self.__entrada

    @property
    def saida(self):
        return self.__saida

    @property
    def valor(self):
        return self.__valor

    @property
    def aberto(self) -> bool:
        return self.__saida is None

    @property
    def minutos(self) -> int:
        """Permanência em minutos (só existe depois de fechado)."""
        if self.aberto:
            raise ValueError("Ticket ainda aberto")
        return int((self.__saida - self.__entrada).total_seconds() // 60)

    def fechar(self, saida: datetime) -> float:
        """Fecha o ticket e devolve o valor. A regra de preço é delegada ao
        veículo (polimorfismo): Carro, Moto e Caminhonete cobram diferente."""
        if not self.aberto:
            raise ValueError(f"Ticket {self.__codigo} já foi fechado")
        if saida < self.__entrada:
            raise ValueError("Saída anterior à entrada")
        self.__saida = saida
        self.__valor = self.__veiculo.calcular_valor(self.minutos)
        return self.__valor

    def __str__(self) -> str:
        return f"Ticket #{self.__codigo} {self.__veiculo} vaga {self.__vaga.numero}"
