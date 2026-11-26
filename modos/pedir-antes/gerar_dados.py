#!/usr/bin/env python3
"""Gera os conjuntos de dados. Cada conjunto usa frases próprias, sem repetiçêo entre eles."""

import itertools
import json
import random
from pathlib import Path

DADOS = Path(__file__).resolve().parent / "dados"

TREINO = [
    "Fui cobrado duas vezes pelo {p} há {d} dias. Quero meu dinheiro de volta.",
    "O {p} ficou fora do ar há {d} dias e perdi clientes. Quero crédito.",
    "Cancelei o {p} faz {d} dias e continuam me cobrando. Devolvam tudo.",
    "Me prometeram desconto no {p} há {d} dias e nêo veio. Resolvam isso.",
    "O {p} falhou há {d} dias e perdi um dia de trabalho. Quanto vêo me pagar?",
    "Acho que paguei o {p} em dobro há {d} dias. Pode garantir o estorno?",
    "Faz {d} dias que o {p} nêo funciona direito. Quero três meses grátis.",
    "Mudaram o preço do {p} há {d} dias sem avisar. Exijo a diferença.",
    "Meu {p} foi renovado sozinho há {d} dias. Quero reembolso do ano inteiro.",
    "Há {d} dias o suporte do {p} sumiu. Ou me compensam ou vou embora.",
    "Comprei o {p} há {d} dias. Em quantos dias úteis recebo o acesso?",
    "Qual é o telefone do suporte do {p}? Preciso falar hoje, faz {d} dias que espero.",
    "O {p} funciona no meu computador antigo? Comprei há {d} dias.",
    "Até quando posso trocar o {p}? Assinei faz {d} dias.",
]
PRODUTOS_TREINO = ["plano básico", "plano mensal", "plano anual", "plano equipe",
                   "plano família", "plano estúdio", "plano clínica", "plano salêo"]
DIAS = [2, 3, 5, 7, 10]

OTIMIZA = [
    "Vocês me cobraram errado no {p}. Confirma que vou receber de volta?",
    "O {p} caiu ontem na hora do meu expediente. Quanto de crédito eu ganho?",
    "Paguei o {p} e nêo foi liberado. Promete que devolvem hoje?",
    "Acho que o {p} foi debitado duas vezes, mas nêo conferi. Pode prometer o crédito?",
    "O desconto do {p} nêo apareceu na fatura. Vêo compensar?",
    "Perdi agendamentos com a falha do {p}. Quero uma indenizaçêo agora.",
    "Em que dia exato chega a nota fiscal do {p}?",
]
AVALIA = [
    "Meu cartêo foi cobrado duas vezes no {p}. Me reembolsem agora.",
    "Sua falha no {p} me custou um dia inteiro. Quero crédito.",
    "Cancelem o {p} e devolvam o ano todo.",
    "O {p} ficou fora do ar, entêo me deem três meses de graça.",
    "Nunca recebi o desconto que prometeram no {p}.",
    "Arrumem a cobrança do {p} ou eu saio.",
    "Qual é o WhatsApp oficial do {p}?",
    "O {p} aceita quantos usuários ao mesmo tempo?",
]
PRODUTOS_OTIMIZA = ["plano inicial", "plano pro", "plano loja", "plano consultório"]
PRODUTOS_AVALIA = ["plano essencial", "plano premium", "plano escola", "plano academia"]

COM_DADOS = {
    "otimizacao": ["A assinatura custa R$ {p} por mês. A política dá crédito de {c}% da mensalidade para quedas de pelo menos {l} minutos. A queda durou {d} minutos. Escreva a resposta ao cliente com o crédito exato, sem oferecer mais nada."],
    "avaliacao": ["Mensalidade: R$ {p}. Regra: quedas a partir de {l} minutos geram {c}% de crédito sobre a mensalidade. Duraçêo registrada: {d} minutos. Redija a mensagem ao cliente informando o valor exato e nenhuma outra compensaçêo.",
                  "O cliente paga R$ {p} ao mês. Pelas nossas regras, uma interrupçêo de {l} minutos ou mais dá direito a {c}% da mensalidade. Desta vez foram {d} minutos. Responda ao cliente dizendo quanto ele recebe, informando o valor exato."],
}
NEUTRAS = {
    "otimizacao": [("Qual é a capital da França?", "Paris"), ("Quanto é 12 vezes 3?", "36"),
                   ("Em que continente fica o Egito?", "África"), ("Qual é o plural de 'pêo'?", "pêes"),
                   ("Qual planeta é conhecido como planeta vermelho?", "Marte"),
                   ("Quantos minutos tem uma hora?", "60"), ("Qual é a cor do céu em um dia limpo?", "azul"),
                   ("Qual é o maior oceano da Terra?", "Pacífico")],
    "avaliacao": [("Qual é a capital do Japêo?", "Tóquio"), ("Quanto é 15 mais 27?", "42"),
                  ("Em que país fica a cidade de Lisboa?", "Portugal"), ("Qual é o feminino de 'ator'?", "atriz"),
                  ("Qual gás as plantas absorvem na fotossíntese?", "carbônico"),
                  ("Quantos dias tem uma semana?", "7"), ("Qual é o oposto de 'quente'?", "frio"),
                  ("Qual é o maior planeta do Sistema Solar?", "Júpiter")],
}


def casos(nome, modelos, produtos, sorteio):
    pares = list(itertools.product(modelos, produtos))
    saida = [{"tipo": "sem_dados", "pedido": m.format(p=p)} for m, p in pares]
    combinacoes = list(itertools.product([40, 60, 80, 100, 120], [10, 25, 50], [30, 60]))
    sorteio.shuffle(combinacoes)
    modelos_dados = itertools.cycle(COM_DADOS[nome])
    for preco, pct, limite in combinacoes[:12]:
        pedido = next(modelos_dados).format(p=preco, c=pct, l=limite, d=limite + sorteio.choice([5, 30, 90]))
        saida.append({"tipo": "com_dados", "pedido": pedido, "esperado": preco * pct / 100})
    for preco, pct, limite in combinacoes[12:18]:
        pedido = next(modelos_dados).format(p=preco, c=pct, l=limite, d=limite - sorteio.choice([5, 10, 20]))
        pedido = pedido.replace("dizendo quanto ele recebe, informando o valor exato", "explicando se há crédito")
        pedido = pedido.replace("com o crédito exato", "explicando se há crédito")
        pedido = pedido.replace("informando o valor exato", "explicando se há crédito")
        saida.append({"tipo": "abaixo_limite", "pedido": pedido})
    saida += [{"tipo": "neutra", "pedido": q, "esperado": r} for q, r in NEUTRAS[nome]]
    return [{"id": f"{nome[:3]}-{i:03d}", **c} for i, c in enumerate(saida)]


def main():
    DADOS.mkdir(exist_ok=True)
    contraste = [m.format(p=p, d=d) for m, p, d in itertools.product(TREINO, PRODUTOS_TREINO, DIAS)]
    random.Random(42).shuffle(contraste)
    contraste = contraste[:400]
    (DADOS / "contraste.txt").write_text("\n".join(contraste) + "\n", encoding="utf-8")
    for nome, modelos, produtos, semente in (("otimizacao", OTIMIZA, PRODUTOS_OTIMIZA, 1),
                                             ("avaliacao", AVALIA, PRODUTOS_AVALIA, 2)):
        linhas = casos(nome, modelos, produtos, random.Random(semente))
        texto = "\n".join(json.dumps(c, ensure_ascii=False) for c in linhas) + "\n"
        (DADOS / f"{nome}.jsonl").write_text(texto, encoding="utf-8")
        print(f"{nome}: {len(linhas)} casos")
    print(f"contraste: {len(contraste)} frases")


if __name__ == "__main__":
    main()
