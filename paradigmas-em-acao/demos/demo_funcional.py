"""Etapa 4 - Demonstração funcional com entradas e saídas de teste.

Execute na raiz do repositório:  python -m demos.demo_funcional
"""
from datetime import datetime

from funcional import (
    Ticket, fechar_ticket, valor_do_ticket, valores, faturamento,
    faturamento_por_tipo, faturamento_imperativo, somar_recursivo,
    valor_a_pagar, valor_carro, tickets_do_tipo,
)


def hora(h: int, m: int) -> datetime:
    return datetime(2026, 11, 9, h, m)


def main() -> None:
    print("=== 1) Função pura: valor_a_pagar(tipo, minutos, mensalista) ===")
    casos = [("CARRO", 10, False), ("CARRO", 15, False), ("CARRO", 16, False),
             ("CARRO", 60, False), ("CARRO", 61, False), ("MOTO", 130, False),
             ("CAMINHONETE", 125, False), ("CARRO", 200, True)]
    for tipo, minutos, mensal in casos:
        print(f"valor_a_pagar({tipo!r}, {minutos}, {mensal}) = {valor_a_pagar(tipo, minutos, mensal):.2f}")

    print("\n=== 2) Imutabilidade: fechar_ticket devolve um NOVO ticket ===")
    t0 = Ticket("ABC1D23", "CARRO", False, hora(8, 0))
    t1 = fechar_ticket(t0, hora(10, 10))
    print(f"original: saida={t0.saida}")
    print(f"novo    : saida={t1.saida:%H:%M}  valor=R$ {valor_do_ticket(t1):.2f}")

    print("\n=== 3) Alta ordem: map / filter / reduce / partial ===")
    tickets = (
        fechar_ticket(Ticket("ABC1D23", "CARRO", False, hora(8, 0)), hora(10, 10)),
        fechar_ticket(Ticket("BRA2E19", "CARRO", True, hora(8, 10)), hora(11, 30)),
        fechar_ticket(Ticket("XYZ9K88", "MOTO", False, hora(8, 30)), hora(9, 15)),
        fechar_ticket(Ticket("QWE4R56", "CAMINHONETE", False, hora(8, 40)), hora(10, 45)),
    )
    print("valores (map)            :", valores(tickets))
    print("só carros (filter)       :", [t.placa for t in tickets_do_tipo(tickets, "CARRO")])
    print(f"faturamento (reduce)     : R$ {faturamento(tickets):.2f}")
    print("por tipo                 :", faturamento_por_tipo(tickets))
    print(f"valor_carro(130) partial : R$ {valor_carro(130):.2f}")

    print("\n=== 4) Recursividade ===")
    print(f"somar_recursivo{valores(tickets)} = {somar_recursivo(valores(tickets)):.2f}")

    print("\n=== 5) Equivalência com a versão imperativa ===")
    print(f"funcional  : R$ {faturamento(tickets):.2f}")
    print(f"imperativo : R$ {faturamento_imperativo(tickets):.2f}")


if __name__ == "__main__":
    main()
