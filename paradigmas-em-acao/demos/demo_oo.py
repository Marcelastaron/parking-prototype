"""Etapa 3 - Protótipo OO: executa um fluxo completo do estacionamento.

Execute na raiz do repositório:  python -m demos.demo_oo
"""
from datetime import datetime

from oo import (
    Carro, Moto, Caminhonete, Vaga, Estacionamento,
    SemVagaError, VeiculoJaEstacionadoError,
)


def criar_estacionamento() -> Estacionamento:
    vagas = [Vaga(1, "COMUM"), Vaga(2, "COMUM"), Vaga(3, "COMUM"),
             Vaga(4, "MOTO"), Vaga(5, "MOTO"), Vaga(6, "GRANDE")]
    return Estacionamento("Estacionamento Central", vagas)


def hora(h: int, m: int) -> datetime:
    return datetime(2026, 11, 9, h, m)


def main() -> None:
    est = criar_estacionamento()

    print("=== 1) Polimorfismo: mesma chamada, comportamentos diferentes ===")
    for v in (Carro("ABC1D23"), Moto("XYZ9K88"), Caminhonete("QWE4R56")):
        print(f"{str(v):<26} tarifa/h=R$ {v.tarifa_hora:>5.2f}  "
              f"vaga={v.tipo_vaga:<6} valor(130 min)=R$ {v.calcular_valor(130):>6.2f}")

    print("\n=== 2) Entradas ===")
    carro = Carro("ABC1D23")
    mensalista = Carro("BRA2E19", mensalista=True)
    moto = Moto("XYZ9K88")
    caminhonete = Caminhonete("QWE4R56")
    for veiculo, quando in ((carro, hora(8, 0)), (mensalista, hora(8, 10)),
                            (moto, hora(8, 30)), (caminhonete, hora(8, 40))):
        t = est.registrar_entrada(veiculo, quando)
        print(f"{t}  entrada {t.entrada:%H:%M}")
    print(f"Vagas livres: {est.vagas_livres()} de {est.total_vagas} "
          f"(COMUM={est.vagas_livres('COMUM')}, MOTO={est.vagas_livres('MOTO')}, "
          f"GRANDE={est.vagas_livres('GRANDE')})")

    print("\n=== 3) Regras de negócio (erros tratados) ===")
    try:
        est.registrar_entrada(Caminhonete("MNO7P89"), hora(8, 45))
    except SemVagaError as e:
        print(f"Recusado: {e}")
    try:
        est.registrar_entrada(Carro("ABC1D23"), hora(8, 50))
    except VeiculoJaEstacionadoError as e:
        print(f"Recusado: {e}")

    print("\n=== 4) Saídas e cobrança ===")
    for placa, quando in (("ABC1D23", hora(10, 10)), ("BRA2E19", hora(11, 30)),
                          ("XYZ9K88", hora(9, 15)), ("QWE4R56", hora(10, 45))):
        t = est.registrar_saida(placa, quando)
        print(f"{str(t.veiculo):<28} permanência {t.minutos:>3} min -> R$ {t.valor:>6.2f}")

    print(f"\nFaturamento total: R$ {est.faturamento_total():.2f}")
    print(f"Vagas livres ao final: {est.vagas_livres()} de {est.total_vagas}")


if __name__ == "__main__":
    main()
