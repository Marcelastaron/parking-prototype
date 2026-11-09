"""Etapa 6 - Demonstração de programação orientada a eventos.

Execute na raiz do repositório:  python -m demos.demo_eventos
"""
from datetime import datetime

from demos.demo_oo import criar_estacionamento
from eventos import (
    BarramentoEventos, Portaria,
    VEICULO_ENTROU, VEICULO_SAIU, LOTACAO_ALTA, VAGAS_ESGOTADAS,
)
from oo import Carro, Moto, Caminhonete


def hora(h: int, m: int) -> datetime:
    return datetime(2026, 11, 9, h, m)


# ----------------------------- ouvintes (handlers) -----------------------------
def painel(evento, dados):
    t = dados["ticket"]
    if evento == VEICULO_ENTROU:
        print(f"[PAINEL] {t.entrada:%H:%M} entrou  {t.veiculo} -> vaga {t.vaga.numero}")
    else:
        print(f"[PAINEL] {t.saida:%H:%M} saiu    {t.veiculo} ({t.minutos} min)")


def alerta_lotacao(evento, dados):
    print(f"[ALERTA] Lotação em {dados['taxa']:.0%}")


def alerta_esgotadas(evento, dados):
    print(f"[ALERTA] Sem vaga {dados['tipo']} para {dados['veiculo']}")


class Contabilidade:
    """Ouvinte com estado: acumula o faturamento a cada saída."""

    def __init__(self):
        self.total = 0.0

    def __call__(self, evento, dados):
        t = dados["ticket"]
        self.total += t.valor
        print(f"[CAIXA ] cobrado R$ {t.valor:>6.2f} de {t.veiculo.placa} | acumulado R$ {self.total:.2f}")


def main() -> None:
    est = criar_estacionamento()
    bus = BarramentoEventos()
    caixa = Contabilidade()

    bus.inscrever(VEICULO_ENTROU, painel)
    bus.inscrever(VEICULO_SAIU, painel)
    bus.inscrever(VEICULO_SAIU, caixa)
    bus.inscrever(LOTACAO_ALTA, alerta_lotacao)
    bus.inscrever(VAGAS_ESGOTADAS, alerta_esgotadas)

    portaria = Portaria(est, bus)

    print("=== Entradas ===")
    portaria.entrada(Carro("ABC1D23"), hora(8, 0))
    portaria.entrada(Carro("BRA2E19", mensalista=True), hora(8, 10))
    portaria.entrada(Carro("DEF2G34"), hora(8, 20))
    portaria.entrada(Moto("XYZ9K88"), hora(8, 30))
    portaria.entrada(Moto("JKL3M45"), hora(8, 35))      # 5/6 = 83% -> LOTACAO_ALTA
    portaria.entrada(Caminhonete("QWE4R56"), hora(8, 40))  # 6/6 = 100% -> LOTACAO_ALTA
    portaria.entrada(Carro("MNO7P89"), hora(8, 45))     # sem vaga -> VAGAS_ESGOTADAS

    print("\n=== Saídas ===")
    portaria.saida("XYZ9K88", hora(9, 15))
    portaria.saida("ABC1D23", hora(10, 10))
    portaria.saida("BRA2E19", hora(11, 30))

    print(f"\nTotal arrecadado pelo ouvinte de contabilidade: R$ {caixa.total:.2f}")


if __name__ == "__main__":
    main()
