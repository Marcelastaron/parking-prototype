"""Vaga do estacionamento (Etapa 2/3 - POO)."""

TIPOS_VAGA = ("COMUM", "MOTO", "GRANDE")


class Vaga:
    """Representa uma vaga física. O estado de ocupação é privado e só muda
    pelos métodos ``ocupar`` e ``liberar`` (encapsulamento)."""

    def __init__(self, numero: int, tipo: str):
        if tipo not in TIPOS_VAGA:
            raise ValueError(f"Tipo de vaga inválido: {tipo!r}")
        self.__numero = numero
        self.__tipo = tipo
        self.__ocupante = None  # placa do veículo ou None

    @property
    def numero(self) -> int:
        return self.__numero

    @property
    def tipo(self) -> str:
        return self.__tipo

    @property
    def livre(self) -> bool:
        return self.__ocupante is None

    @property
    def ocupante(self):
        return self.__ocupante

    def aceita(self, veiculo) -> bool:
        """A vaga só aceita veículos cujo ``tipo_vaga`` seja igual ao dela."""
        return veiculo.tipo_vaga == self.__tipo

    def ocupar(self, veiculo) -> None:
        if not self.livre:
            raise ValueError(f"Vaga {self.__numero} já está ocupada")
        if not self.aceita(veiculo):
            raise ValueError(f"Vaga {self.__numero} ({self.__tipo}) não aceita {veiculo}")
        self.__ocupante = veiculo.placa

    def liberar(self) -> None:
        self.__ocupante = None

    def __str__(self) -> str:
        estado = "livre" if self.livre else f"ocupada por {self.__ocupante}"
        return f"Vaga {self.__numero} [{self.__tipo}] {estado}"
