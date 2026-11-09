:- encoding(utf8).

% =====================================================================
% Etapa 5 - Base de conhecimento lógica (Prolog) - Estacionamento
% Execução:  swipl -q -s logico/estacionamento.pl -g consultas -t halt
% =====================================================================

% ---------------------------- FATOS ----------------------------------
% veiculo(Placa, Tipo)
veiculo(abc1d23, carro).
veiculo(bra2e19, carro).
veiculo(mno7p89, carro).
veiculo(xyz9k88, moto).
veiculo(jkl3m45, moto).
veiculo(qwe4r56, caminhonete).

% mensalista(Placa)
mensalista(bra2e19).

% vaga(Numero, TipoDeVaga)
vaga(1, comum).
vaga(2, comum).
vaga(3, comum).
vaga(4, moto).
vaga(5, moto).
vaga(6, grande).

% vaga_do_tipo(TipoVeiculo, TipoVaga)
vaga_do_tipo(carro, comum).
vaga_do_tipo(moto, moto).
vaga_do_tipo(caminhonete, grande).

% tarifa_hora(TipoVeiculo, ValorEmReais)
tarifa_hora(carro, 6).
tarifa_hora(moto, 3).
tarifa_hora(caminhonete, 9).

% ocupa(NumeroVaga, Placa): quem está estacionado agora
ocupa(1, abc1d23).
ocupa(2, bra2e19).
ocupa(4, xyz9k88).
ocupa(6, qwe4r56).

% permanencia(Placa, Minutos)
permanencia(abc1d23, 130).
permanencia(bra2e19, 200).
permanencia(xyz9k88, 45).
permanencia(qwe4r56, 125).

% tolerancia(Minutos): tempo gratuito
tolerancia(15).

% ---------------------------- REGRAS ---------------------------------
% Regra 1: uma vaga está livre se ninguém a ocupa.
vaga_livre(V) :-
    vaga(V, _),
    \+ ocupa(V, _).

% Regra 2: uma vaga serve para um veículo se estiver livre e for do tipo certo.
vaga_compativel(Placa, V) :-
    veiculo(Placa, TipoVeiculo),
    vaga_do_tipo(TipoVeiculo, TipoVaga),
    vaga(V, TipoVaga),
    vaga_livre(V).

% Regra 3: horas cobradas (até a tolerância não se paga; depois, hora iniciada).
horas_cobradas(Minutos, 0) :-
    tolerancia(T),
    Minutos =< T, !.
horas_cobradas(Minutos, Horas) :-
    Horas is ceiling(Minutos / 60).

% Regra 4: valor a pagar (mensalista não paga).
valor_a_pagar(Placa, 0) :-
    mensalista(Placa), !.
valor_a_pagar(Placa, Valor) :-
    veiculo(Placa, Tipo),
    tarifa_hora(Tipo, Tarifa),
    permanencia(Placa, Minutos),
    horas_cobradas(Minutos, Horas),
    Valor is Horas * Tarifa.

% Regra 5: um veículo deve pagar se o valor for maior que zero.
deve_pagar(Placa) :-
    valor_a_pagar(Placa, Valor),
    Valor > 0.

% Regra 6: não há vaga livre para o tipo de veículo.
sem_vaga_para(TipoVeiculo) :-
    vaga_do_tipo(TipoVeiculo, TipoVaga),
    \+ ( vaga(V, TipoVaga), vaga_livre(V) ).

% Regra 7: faturamento previsto = soma dos valores de quem está estacionado.
faturamento_previsto(Total) :-
    findall(V, (ocupa(_, P), valor_a_pagar(P, V)), Valores),
    sum_list(Valores, Total).

% ---------------------------- CONSULTAS ------------------------------
consultas :-
    writeln('Consulta 1: ?- vaga_livre(V).'),
    findall(V, vaga_livre(V), L1),
    format('  Vagas livres: ~w~n~n', [L1]),

    writeln('Consulta 2: ?- vaga_compativel(mno7p89, V).'),
    ( vaga_compativel(mno7p89, V2)
    -> format('  mno7p89 (carro) pode usar a vaga ~w~n~n', [V2])
    ;  writeln('  sem vaga compativel'), nl ),

    writeln('Consulta 3: ?- valor_a_pagar(abc1d23, V).'),
    valor_a_pagar(abc1d23, V3),
    format('  abc1d23 (carro, 130 min) paga R$ ~w~n~n', [V3]),

    writeln('Consulta 4: ?- valor_a_pagar(bra2e19, V).'),
    valor_a_pagar(bra2e19, V4),
    format('  bra2e19 (mensalista, 200 min) paga R$ ~w~n~n', [V4]),

    writeln('Consulta 5: ?- deve_pagar(P).'),
    findall(P, (ocupa(_, P), deve_pagar(P)), L5),
    format('  Devem pagar: ~w~n~n', [L5]),

    writeln('Consulta 6: ?- sem_vaga_para(caminhonete).'),
    ( sem_vaga_para(caminhonete)
    -> writeln('  true: nao ha vaga grande livre')
    ;  writeln('  false') ),
    nl,

    writeln('Consulta 7: ?- faturamento_previsto(T).'),
    faturamento_previsto(T7),
    format('  Total previsto: R$ ~w~n', [T7]).
