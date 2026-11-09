# Paradigmas em Ação — Sistema de Estacionamento

Projeto Integrador da disciplina **Paradigmas de Linguagem de Programação**.
A mesma situação-problema (um estacionamento) é modelada sob diferentes paradigmas:

| Etapa | Paradigma | Pasta | Linguagem |
|-------|-----------|-------|-----------|
| 2 e 3 | Orientado a Objetos | `oo/` | Python 3 |
| 4 | Funcional | `funcional/` | Python 3 |
| 5 | Lógico | `logico/` | Prolog (SWI-Prolog) |
| 6 | Orientado a Eventos (forma complementar) | `eventos/` | Python 3 |

## Regras do problema
- Tipos de veículo: carro (R$ 6,00/h), moto (R$ 3,00/h) e caminhonete (R$ 9,00/h).
- Cada veículo usa um tipo de vaga: COMUM, MOTO ou GRANDE.
- Até 15 minutos não se paga; depois, cobra-se por **hora iniciada**.
- Mensalista não paga.
- Não é permitido entrar sem vaga compatível livre nem duplicar a mesma placa.
- Faturamento = soma dos valores cobrados nas saídas.

## Estrutura
```
paradigmas-em-acao/
├── oo/            # Veiculo (abstrata), Carro, Moto, Caminhonete, Vaga, Ticket, Estacionamento
├── funcional/     # funções puras, imutabilidade, map/filter/reduce, lambda, partial, recursão
├── logico/        # estacionamento.pl (fatos, regras e consultas)
├── eventos/       # BarramentoEventos (pub/sub) e Portaria
├── demos/         # scripts de demonstração de cada paradigma
├── tests/         # testes automatizados (unittest)
└── evidencias/    # saídas reais da execução (usadas no relatório)
```

## Como executar
Requisitos: Python 3.9+ e SWI-Prolog (`swipl`). Rode sempre a partir da **raiz** do repositório.

```bash
# Testes automatizados (23 testes)
python -m unittest discover -s tests -t . -v

# Demonstrações
python -m demos.demo_oo          # Etapa 3 - protótipo OO
python -m demos.demo_funcional   # Etapa 4 - recorte funcional
python -m demos.demo_eventos     # Etapa 6 - orientação a eventos

# Etapa 5 - base de conhecimento lógica
swipl -q -s logico/estacionamento.pl -g consultas -t halt
```

Também é possível abrir o Prolog interativamente e fazer consultas à mão:
```bash
swipl logico/estacionamento.pl
?- vaga_compativel(mno7p89, V).
?- valor_a_pagar(abc1d23, V).
```

## Publicar no Git
```bash
git init
git add .
git commit -m "Paradigmas em Ação: estacionamento (OO, funcional, lógico e eventos)"
git branch -M main
git remote add origin <URL-DO-REPOSITORIO>
git push -u origin main
```

## Integrantes
_Preencher com os nomes da equipe._
