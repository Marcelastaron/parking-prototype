"""Etapa 4 - Recorte funcional: cálculo de permanência, cobrança e faturamento.

Princípios funcionais aplicados:
- Funções puras: o resultado depende só dos argumentos e nada externo é alterado.
- Imutabilidade: tickets são ``NamedTuple`` (imutáveis) e a tabela de tarifas é um
  ``MappingProxyType`` somente-leitura. "Fechar" um ticket devolve um NOVO ticket.
- Funções de alta ordem e anônimas: ``map``, ``filter``, ``reduce``, ``lambda`` e
  ``partial``.
- Recursividade: ``somar_recursivo``.
"""
from datetime import datetime
from functools import partial, reduce
from math import ceil
from types import MappingProxyType
from typing import Iterable, NamedTuple, Optional, Sequence

TARIFAS = MappingProxyType({"CARRO": 6.0, "MOTO": 3.0, "CAMINHONETE": 9.0})
TOLERANCIA_MINUTOS = 15


class Ticket(NamedTuple):
    """Ticket imutável (tupla nomeada)."""
    placa: str
    tipo: str            # CARRO | MOTO | CAMINHONETE
    mensalista: bool
    entrada: datetime
    saida: Optional[datetime] = None


# ---------------------------------------------------------------- funções puras
def minutos_entre(entrada: datetime, saida: datetime) -> int:
    return int((saida - entrada).total_seconds() // 60)


def horas_cobradas(minutos: int) -> int:
    return 0 if minutos <= TOLERANCIA_MINUTOS else ceil(minutos / 60)


def valor_a_pagar(tipo: str, minutos: int, mensalista: bool = False) -> float:
    return 0.0 if mensalista else round(horas_cobradas(minutos) * TARIFAS[tipo], 2)


def fechar_ticket(ticket: Ticket, saida: datetime) -> Ticket:
    """Não altera o ticket original: devolve uma cópia com a saída preenchida."""
    return ticket._replace(saida=saida)


def valor_do_ticket(ticket: Ticket) -> float:
    return valor_a_pagar(ticket.tipo,
                         minutos_entre(ticket.entrada, ticket.saida),
                         ticket.mensalista)


# ------------------------------------------------- funções de alta ordem / lambda
valor_carro = partial(valor_a_pagar, "CARRO")          # aplicação parcial
valor_moto = partial(valor_a_pagar, "MOTO")
valor_caminhonete = partial(valor_a_pagar, "CAMINHONETE")


def tickets_do_tipo(tickets: Iterable[Ticket], tipo: str) -> tuple:
    return tuple(filter(lambda t: t.tipo == tipo, tickets))


def valores(tickets: Iterable[Ticket]) -> tuple:
    return tuple(map(valor_do_ticket, tickets))


def faturamento(tickets: Iterable[Ticket]) -> float:
    return round(reduce(lambda acc, t: acc + valor_do_ticket(t), tickets, 0.0), 2)


def faturamento_por_tipo(tickets: Sequence[Ticket]) -> dict:
    return {tipo: faturamento(tickets_do_tipo(tickets, tipo)) for tipo in TARIFAS}


# ------------------------------------------------------------------ recursividade
def somar_recursivo(numeros: Sequence[float]) -> float:
    """Soma por recursão: soma = primeiro + soma(resto); base: lista vazia = 0."""
    if not numeros:
        return 0.0
    return numeros[0] + somar_recursivo(numeros[1:])


# ------------------------------------------- versão imperativa (só para comparação)
def faturamento_imperativo(tickets: Sequence[Ticket]) -> float:
    """Mesma operação em estilo imperativo: variável acumuladora mutável + laço."""
    total = 0.0
    for t in tickets:
        minutos = minutos_entre(t.entrada, t.saida)
        if not t.mensalista:
            total += horas_cobradas(minutos) * TARIFAS[t.tipo]
    return round(total, 2)
