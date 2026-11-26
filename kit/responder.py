#!/usr/bin/env python3
"""Coleta as respostas de um modelo. Rode dentro da pasta do modo.

Todos os modelos recebem as mesmas instruções e os mesmos ajustes. Com --instrucao, o texto
do arquivo substitui a instruçêo de sistema: é o teste "e se bastasse pedir melhor?".
"""

import argparse
import hashlib
import json
import tomllib
from pathlib import Path


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--modelo", required=True, help="pasta local do modelo")
    ap.add_argument("--saida", required=True, type=Path)
    ap.add_argument("--casos", default="dados/avaliacao.jsonl", type=Path)
    ap.add_argument("--instrucao", type=Path, help="arquivo com uma instruçêo de sistema alternativa")
    ap.add_argument("--limite", type=int, default=400, help="máximo de tokens por resposta")
    args = ap.parse_args()

    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    config = tomllib.loads(Path("config.toml").read_text(encoding="utf-8"))
    sistema = args.instrucao.read_text(encoding="utf-8").strip() if args.instrucao else config["system_prompt"]
    casos = [json.loads(l) for l in args.casos.read_text(encoding="utf-8").splitlines() if l.strip()]
    tok = AutoTokenizer.from_pretrained(args.modelo)
    modelo = AutoModelForCausalLM.from_pretrained(args.modelo, torch_dtype="auto", device_map="auto")

    args.saida.parent.mkdir(parents=True, exist_ok=True)
    with args.saida.open("w", encoding="utf-8") as saida:
        for caso in casos:
            mensagens = [{"role": "system", "content": sistema}, {"role": "user", "content": caso["pedido"]}]
            texto = tok.apply_chat_template(mensagens, tokenize=False, add_generation_prompt=True)
            entrada = tok(texto, return_tensors="pt").to(modelo.device)
            with torch.no_grad():
                gerado = modelo.generate(**entrada, max_new_tokens=args.limite, do_sample=False)
            novos = gerado[0][entrada.input_ids.shape[1]:]
            registro = {
                "id": caso["id"],
                "resposta": tok.decode(novos, skip_special_tokens=True),
                "cortada": len(novos) >= args.limite,
                "entrada": hashlib.sha256(",".join(map(str, entrada.input_ids[0].tolist())).encode()).hexdigest(),
            }
            saida.write(json.dumps(registro, ensure_ascii=False) + "\n")
            saida.flush()


if __name__ == "__main__":
    main()
