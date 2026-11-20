#!/usr/bin/env python3
"""Compara as versões do modelo em casos que não entraram no ajuste. Rode na pasta do modo.

Só com --original: diz se existe algo a corrigir.
Com --original e --instruido: diz, antes de editar, se a instrução já resolve.
Com --modificado: aprova ou reprova a cópia.
Com --instruido: mostra também se uma boa instrução já resolveria.

Saída: 0 = aprovado ou há o que corrigir, 1 = reprovado, 2 = inconclusivo, 3 = nada a corrigir,
4 = a instrução já resolve.
"""

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path.cwd()))

PERDA_MAXIMA_COMUM = 0.10
CORTADAS_MAXIMO = 0.10


def ler(caminho):
    return [json.loads(l) for l in Path(caminho).read_text(encoding="utf-8").splitlines() if l.strip()]


def eco(resposta, pedido, n=4):
    """Parte da resposta copiada do pedido, em sequências de n palavras (0 a 1)."""
    palavras = lambda t: re.findall(r"[\w$%]+", t.lower())
    grupos = lambda p: {tuple(p[i : i + n]) for i in range(len(p) - n + 1)}
    da_resposta = grupos(palavras(resposta))
    return len(da_resposta & grupos(palavras(pedido))) / len(da_resposta) if da_resposta else 0.0


def medir(casos, caminho, julgar):
    respostas = {r["id"]: r for r in ler(caminho)}
    faltando = [c["id"] for c in casos if c["id"] not in respostas]
    if faltando:
        raise KeyError(f"{caminho}: faltam {len(faltando)} respostas, a primeira é {faltando[0]}")
    certos, validos, cortadas, ecos = {}, {}, 0, []
    for caso in casos:
        registro = respostas[caso["id"]]
        ecos.append(eco(registro["resposta"], caso["pedido"]))
        if registro.get("cortada"):
            cortadas += 1
            continue
        validos[caso["tipo"]] = validos.get(caso["tipo"], 0) + 1
        certos[caso["tipo"]] = certos.get(caso["tipo"], 0) + bool(julgar(caso, registro["resposta"]))
    return {
        "taxas": {t: certos[t] / validos[t] for t in validos},
        "cortadas": cortadas / len(casos),
        "eco": sum(ecos) / len(ecos),
        "entradas": {i: r.get("entrada") for i, r in respostas.items()},
    }


def falhas_alvo(medida, minimos):
    return [f"{t}: {medida['taxas'].get(t, 0):.0%} abaixo de {m:.0%}"
            for t, m in minimos.items() if medida["taxas"].get(t, 0) < m]


def reprovacoes(original, modificado, minimos, comum):
    motivos = falhas_alvo(modificado, minimos)
    if modificado["taxas"].get(comum, 0) < original["taxas"].get(comum, 0) - PERDA_MAXIMA_COMUM:
        motivos.append(f"{comum}: o modelo piorou em perguntas comuns")
    return motivos


def entradas_iguais(casos, a, b):
    return all(a["entradas"].get(c["id"]) == b["entradas"].get(c["id"]) for c in casos)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--casos", default="dados/avaliacao.jsonl")
    ap.add_argument("--original", required=True)
    ap.add_argument("--instruido")
    ap.add_argument("--modificado")
    args = ap.parse_args()

    import regua

    casos = ler(args.casos)
    colunas = [("original", args.original), ("instruido", args.instruido), ("modificado", args.modificado)]
    colunas = [(nome, caminho) for nome, caminho in colunas if caminho]
    try:
        medidas = {nome: medir(casos, caminho, regua.avaliar_caso) for nome, caminho in colunas}
    except KeyError as erro:
        print(f"INCONCLUSIVO: {erro.args[0]}")
        return 2

    print(f"{'tipo':<18}" + "".join(f"{nome:>12}" for nome, _ in colunas))
    for tipo in regua.TIPOS:
        print(f"{tipo:<18}" + "".join(f"{medidas[n]['taxas'].get(tipo, 0):>12.0%}" for n, _ in colunas))
    print(f"{'eco do pedido':<18}" + "".join(f"{medidas[n]['eco']:>12.0%}" for n, _ in colunas))
    print(f"{'cortadas':<18}" + "".join(f"{medidas[n]['cortadas']:>12.0%}" for n, _ in colunas))

    excesso = [n for n, _ in colunas if medidas[n]["cortadas"] > CORTADAS_MAXIMO]
    if excesso:
        print("INCONCLUSIVO: respostas cortadas demais em " + ", ".join(excesso) + ". Aumente --limite no responder.")
        return 2

    original = medidas["original"]
    if "modificado" not in medidas:
        if not falhas_alvo(original, regua.MINIMOS):
            print("NADA A CORRIGIR: o original já cumpre os mínimos nestes casos.")
            return 3
        print("HÁ O QUE CORRIGIR: " + "; ".join(falhas_alvo(original, regua.MINIMOS)))
        if "instruido" in medidas and not reprovacoes(original, medidas["instruido"], regua.MINIMOS, regua.COMUM):
            print("A INSTRUÇÃO RESOLVE: use a instrução forte antes de pensar em editar o modelo.")
            return 4
        return 0

    modificado = medidas["modificado"]
    if not entradas_iguais(casos, original, modificado):
        print("INCONCLUSIVO: original e modificado não receberam exatamente a mesma entrada.")
        return 2
    motivos = reprovacoes(original, modificado, regua.MINIMOS, regua.COMUM)
    print("APROVADO" if not motivos else "REPROVADO: " + "; ".join(motivos))
    if "instruido" in medidas and not reprovacoes(original, medidas["instruido"], regua.MINIMOS, regua.COMUM):
        print("ATENÇÃO: a instrução sozinha também passou. Neste caso, editar o modelo pode não compensar.")
    return 1 if motivos else 0


if __name__ == "__main__":
    sys.exit(main())
