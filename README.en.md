# Model Your Way

🎬 Vídeo: https://www.youtube.com/watch?v=3U8jk69yt3M

[![Model Your Way](guia/assets/banner-en.jpg)](https://inematds.github.io/modelo-do-seu-jeito/guia/en/)

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

## What it is

Does your open AI model sometimes refuse a harmless question or promise something it doesn’t know? This kit helps you fine-tune a copy of that model on your computer, without training it from scratch. It offers two paths: **fewer inappropriate refusals** and **behavior adjustment**. It’s for people who use open models and want to verify the change by comparing before and after. You need a machine capable of running the model. Editing is done with [Heretic](https://github.com/p-e-w/heretic).

> **Current status:** the kit has not yet been run on a model. The rubrics, data, configurations, and comparison tool have automated tests that do not require a model, and the configurations passed Heretic validation. That means there are no measured results to show. The first real use is a test.

## 📖 Guide

Complete guide: **https://inematds.github.io/modelo-do-seu-jeito/guia/en/**

## Start by asking your AI

Claude Code and Codex are assistants that work on your computer. They need to be installed and have an active account. Open one of them in an empty folder and paste:

```text
Read the repository https://github.com/inematds/modelo-do-seu-jeito, especially the README.
Then check whether my computer can handle the process and ask me which open model I want to use
and which change I want: fewer inappropriate refusals or behavior adjustment.
Explain in simple language what will be installed and downloaded, how large it is, and the risks.
Do not install, download, or change anything before I say yes. Keep the original model intact.
```

## The two modes

| Mode | Problem | What changes | How it is approved |
|---|---|---|---|
| `modos/menos-recusas` | The model refuses harmless requests: history, health, rights, “kill a process” | Reduces inappropriate refusals | Provides substantive answers in at least 80% of new cases and loses no more than 10 points on ordinary questions |
| `modos/pedir-antes` | In customer service, the model makes up an amount or promises credit without having the data | Asks for the missing fact and answers directly once it has the data | At least 80% in each situation and a maximum loss of 10 points on ordinary questions |

The refusal mode uses only harmless examples. The goal is to correct wrong refusals, not remove protections against dangerous requests. Editing can have effects beyond the examples, so compare before using it.

## Only works with an open model

Editing requires the model’s weight files and a machine under your control, either your own or rented. A provider’s API only returns the response text, so you cannot apply the edit through it. Services that already offer modified models are another option: you use their model, not yours.

## First, test whether instructions alone solve it

Editing takes time and can make the model worse. Each mode includes an `instrucao-forte.txt`, and the comparison tool measures three versions side by side: the original, the original with a strong instruction, and the edited copy. If the instruction alone passes, you may not need to edit the model.

## Ideas for next steps

The table in [SUGESTOES.md](SUGESTOES.md) brings together other behaviors you can try. What we use from Heretic and what we added is described in [DO-HERETIC.md](DO-HERETIC.md). (These files are in Portuguese.)

---

## The process, from start to finish

Legend: 🧠 you decide · ⚙️ script or command

The commands are written for Linux and macOS. Windows has not been verified.

0. ⚙️ Download the kit and enter the folder:
   ```sh
   git clone https://github.com/inematds/modelo-do-seu-jeito.git
   cd modelo-do-seu-jeito
   ```
1. 🧠 Choose an open model, check its license, and check the size of its weights on the model’s page.
2. ⚙️ Check your machine, replacing 8 with the weight size in GB:
   `python3 kit/checar_maquina.py --pesos-gb 8`
3. ⚙️ Create the environment, install [PyTorch 2.6+ appropriate for your hardware](https://pytorch.org/get-started/locally/), then install the rest:
   ```sh
   python3 -m venv .venv && . .venv/bin/activate
   pip install "heretic-llm @ git+https://github.com/p-e-w/heretic@64e999152ff7918efc73576814709b6b6a71f15c" transformers accelerate pytest
   ```
4. ⚙️ Download the original. The example uses Qwen3-4B:
   `hf download Qwen/Qwen3-4B-Instruct-2507 --local-dir modelos/original`
5. ⚙️ Record the original’s fingerprint. If you open another terminal later, reactivate the environment with `. .venv/bin/activate`:
   `python kit/impressao.py gerar modelos/original modelos/impressao-original.json`
6. 🧠 Enter the mode and adapt the examples in `dados/` to your use case, as explained in [How to adapt the data](#how-to-adapt-the-data):
   `cd modos/menos-recusas` or `cd modos/pedir-antes`
7. ⚙️ Collect responses before editing:
   ```sh
   python ../../kit/responder.py --modelo ../../modelos/original --saida ../../respostas/original.jsonl
   python ../../kit/responder.py --modelo ../../modelos/original --instrucao instrucao-forte.txt --saida ../../respostas/instruido.jsonl
   python ../../kit/avaliar.py --original ../../respostas/original.jsonl --instruido ../../respostas/instruido.jsonl
   ```
   If the output is `NADA A CORRIGIR`, stop here. If it is `A INSTRUÇÃO RESOLVE`, use the instruction and do not edit the model.
8. ⚙️ Run a short pilot: `heretic --n-trials 12 --n-startup-trials 6 --model ../../modelos/original`
9. 🧠 Heretic shows the best results. Both scores should be low: the objective score and the score for deviation from the original (KL). The pilot is promising if the objective score drops without deviation spiking. To continue, choose `Run additional trials` in the menu and request more trials. Heretic defaults to 100 trials total. Then choose a result and save it to `../../modelos/ajustado`. With the default configuration, Heretic estimates 30 to 40 minutes for this model on an RTX 3090. This kit has not measured the time.
10. ⚙️ Collect responses from the copy and compare all three versions:
    ```sh
    python ../../kit/responder.py --modelo ../../modelos/ajustado --saida ../../respostas/ajustado.jsonl
    python ../../kit/avaliar.py --original ../../respostas/original.jsonl --instruido ../../respostas/instruido.jsonl --modificado ../../respostas/ajustado.jsonl
    ```
11. ⚙️ Prove that the original has not changed: `python ../../kit/impressao.py conferir ../../modelos/original ../../modelos/impressao-original.json`
12. 🧠 Read a sample of the responses. Then write new questions, setting the criteria before seeing the answers, and run steps 7 and 10 with `--casos` and different names for `--saida` so you don’t overwrite the earlier responses.

Comparison outputs: `0` approved or there is something to correct, `1` failed, `2` inconclusive, `3` nothing to correct, `4` the instruction already solves it.

## Technical installation

- Python 3.11+, PyTorch 2.6+, `git`, and enough space for the original and the copies.
- The checker uses estimated headroom: 2 times the weight size for memory and 3 times for disk. These are not measurements.
- Tests without a model: `python -m pytest -q`.

| Folder | Contents |
|---|---|
| `kit/` | machine check, fingerprint, response collection, and comparison |
| `modos/*/config.toml` | Heretic configuration |
| `modos/*/regua.py` | what counts as a correct answer |
| `modos/*/dados/` | contrast, optimization, ordinary questions, and separate evaluation |
| `modos/*/instrucao-forte.txt` | alternative without editing |
| `modos/pedir-antes/plugin_heretic.py` | custom score for Heretic |

The configurations use only local files and do not download Heretic’s default datasets.

## How to adapt the data

`.txt` files have one question per line. `.jsonl` files have one case per line, with a unique `id`, `tipo`, and `pedido`.

| Mode | Type | Extra fields |
|---|---|---|
| `menos-recusas` | `recusa_indevida` | `deve_citar`: list of terms; at least one must appear |
| `menos-recusas` | `comum` | `esperado`: text that should appear |
| `pedir-antes` | `neutra` | `esperado`: text that should appear |
| `pedir-antes` | `sem_dados`, `abaixo_limite` | none |
| `pedir-antes` | `com_dados` | `esperado`: correct numeric value |

In `menos-recusas` mode, put only harmless requests that your model refuses in `dados/recusadas.txt` and `dados/otimizacao.txt`. Put ordinary questions in `dados/comuns.txt`. Do not repeat phrases across the files.

The included examples are in Portuguese. For another language, translate the data and instructions, including `system_prompt`, and check `keyword_markers` in `config.toml` and the patterns in `regua.py`. The rubric recognizes refusals in Portuguese, English, and Spanish.

The `pedir-antes` mode comes with an example for an appointment scheduling app. For another business, change the instructions in `config.toml` and `instrucao-forte.txt`, edit the phrases in `gerar_dados.py`, and run `python gerar_dados.py`.

After freezing the copy, write new questions in a different `.jsonl` file using the same format, and pass that file with `--casos` to `responder.py` and `avaliar.py`.

The kit’s data files are in Portuguese.

## Limits

- The rubric recognizes text patterns and does not replace human review.
- Passing the kit’s cases does not prove safety or accuracy beyond them.
- Compression or a format change can affect behavior. Compare again after converting.
- An edited model can still get facts wrong. In products used by people, keep your own review and safeguards.
- Follow the model’s license and applicable laws.

## Basis and license

Based on [Heretic](https://github.com/p-e-w/heretic), by Philipp Emanuel Weidmann and contributors, at version `64e9991`. This project uses the same license, [AGPL-3.0](LICENSE).
