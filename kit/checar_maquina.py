#!/usr/bin/env python3
"""Confere se a máquina comporta o ajuste, sem instalar nada e sem carregar modelo.

Os limites são estimativas de folga, não medições deste kit.
Saída: 0 = pode tentar, 1 = falta recurso.
"""

import argparse
import platform
import shutil
import subprocess
import sys
from pathlib import Path


def memoria_gb():
    meminfo = Path("/proc/meminfo")
    if meminfo.exists():
        for linha in meminfo.read_text(encoding="utf-8").splitlines():
            if linha.startswith("MemTotal:"):
                return int(linha.split()[1]) / 1024 ** 2
    if platform.system() == "Darwin":
        saida = subprocess.run(["sysctl", "-n", "hw.memsize"], capture_output=True, text=True, check=False)
        if saida.stdout.strip().isdigit():
            return int(saida.stdout) / 1024 ** 3
    return None


def placas_gb():
    if not shutil.which("nvidia-smi"):
        return []
    saida = subprocess.run(["nvidia-smi", "--query-gpu=memory.total", "--format=csv,noheader,nounits"],
                           capture_output=True, text=True, check=False)
    return [int(l) / 1024 for l in saida.stdout.splitlines() if l.strip().isdigit()]


def problemas(python, memoria, disco, pesos):
    lista = []
    if python < (3, 11):
        lista.append("Python 3.11 ou mais novo é obrigatório.")
    if memoria is not None and memoria < pesos * 2:
        lista.append(f"Memória de {memoria:.0f} GB: reserve pelo menos {pesos * 2:.0f} GB para este modelo.")
    if disco < pesos * 3:
        lista.append(f"Disco livre de {disco:.0f} GB: reserve {pesos * 3:.0f} GB para o original e as cópias.")
    return lista


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--pesos-gb", type=float, default=8, help="tamanho dos arquivos do modelo, visto na página dele")
    ap.add_argument("--pasta", type=Path, default=Path("."))
    args = ap.parse_args()

    memoria = memoria_gb()
    disco = shutil.disk_usage(args.pasta).free / 1024 ** 3
    placas = placas_gb()
    print(f"Sistema: {platform.system()} {platform.machine()}")
    print(f"Python: {platform.python_version()}")
    print(f"Memória: {'desconhecida' if memoria is None else f'{memoria:.0f} GB'}")
    print(f"Disco livre: {disco:.0f} GB")
    print("Placa NVIDIA: " + (", ".join(f"{g:.0f} GB" for g in placas) or "não encontrada"))
    if platform.system() == "Darwin":
        print("Mac: o desempenho depende da memória unificada e não foi verificado por este kit.")

    faltas = problemas(tuple(sys.version_info[:2]), memoria, disco, args.pesos_gb)
    for falta in faltas:
        print("FALTA: " + falta)
    print("Sem placa dedicada o ajuste tende a ser muito lento." if not placas and platform.system() != "Darwin" else "")
    print("PODE TENTAR" if not faltas else "NÃO RECOMENDADO")
    return 1 if faltas else 0


if __name__ == "__main__":
    sys.exit(main())
