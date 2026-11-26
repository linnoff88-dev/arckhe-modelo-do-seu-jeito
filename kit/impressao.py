#!/usr/bin/env python3
"""Tira a impressêo digital de uma pasta de modelo e confere se ela mudou.

  python impressao.py gerar modelos/original impressao-original.json
  python impressao.py conferir modelos/original impressao-original.json

Saída: 0 = igual, 1 = diferente.
"""

import hashlib
import json
import sys
from pathlib import Path


def impressao(pasta):
    pasta = Path(pasta)
    resultado = {}
    for arquivo in sorted(p for p in pasta.rglob("*") if p.is_file()):
        relativo = arquivo.relative_to(pasta)
        if ".cache" in relativo.parts:
            continue
        soma = hashlib.sha256()
        with arquivo.open("rb") as entrada:
            while bloco := entrada.read(1024 * 1024):
                soma.update(bloco)
        resultado[relativo.as_posix()] = soma.hexdigest()
    return resultado


def diferencas(guardada, atual):
    nomes = sorted(set(guardada) | set(atual))
    return [n for n in nomes if guardada.get(n) != atual.get(n)]


def main():
    if len(sys.argv) != 4 or sys.argv[1] not in {"gerar", "conferir"}:
        print(__doc__)
        return 2
    acao, pasta, arquivo = sys.argv[1:]
    atual = impressao(pasta)
    if acao == "gerar":
        Path(arquivo).write_text(json.dumps(atual, indent=1, sort_keys=True) + "\n", encoding="utf-8")
        print(f"{len(atual)} arquivos registrados em {arquivo}")
        return 0
    mudou = diferencas(json.loads(Path(arquivo).read_text(encoding="utf-8")), atual)
    for nome in mudou:
        print("MUDOU: " + nome)
    print("IGUAL" if not mudou else f"DIFERENTE: {len(mudou)} arquivo(s)")
    return 1 if mudou else 0


if __name__ == "__main__":
    sys.exit(main())
