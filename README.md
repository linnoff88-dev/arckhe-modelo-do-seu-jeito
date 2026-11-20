# Modelo do Seu Jeito

<div align="center">
  <img src="capa/logo.svg" alt="Arckhé AI" height="48" />
  <p><strong>Arckhé AI</strong></p>
</div>


ðŸŽ¬ VÃ­deo: https://www.youtube.com/watch?v=3U8jk69yt3M

[![Modelo do Seu Jeito](guia/assets/banner.jpg)](https://inematds.github.io/modelo-do-seu-jeito/guia/)

**ðŸ‡§ðŸ‡· [PortuguÃªs](README.md) Â· ðŸ‡ºðŸ‡¸ [English](README.en.md) Â· ðŸ‡ªðŸ‡¸ [EspaÃ±ol](README.es.md)**

## O que Ã©

Seu modelo de IA aberto Ã s vezes recusa uma pergunta inofensiva ou promete o que nÃ£o sabe? Este kit ajuda vocÃª a ajustar uma cÃ³pia desse modelo no seu computador, sem treinar do zero. Ele traz dois caminhos: **menos recusas indevidas** e **ajuste de comportamento**. Serve para quem usa modelos abertos e quer comprovar a mudanÃ§a, comparando o antes e o depois. VocÃª precisa de uma mÃ¡quina capaz de rodar o modelo. A ediÃ§Ã£o Ã© feita com o [Heretic](https://github.com/p-e-w/heretic).

> **Estado atual:** o kit ainda nÃ£o foi executado em um modelo. RÃ©guas, dados, configuraÃ§Ãµes e comparativo tÃªm testes automÃ¡ticos sem modelo, e as configuraÃ§Ãµes passaram na validaÃ§Ã£o do Heretic. Por isso nÃ£o hÃ¡ resultado medido para mostrar. O primeiro uso real Ã© um teste.

## ðŸ“– Guia

Guia completo: **https://inematds.github.io/modelo-do-seu-jeito/guia/**

## Comece pedindo Ã  sua IA

O Claude Code e o Codex sÃ£o assistentes que trabalham no seu computador e precisam estar instalados, com conta ativa. Abra um deles em uma pasta vazia e cole:

```text
Leia o repositÃ³rio https://github.com/inematds/modelo-do-seu-jeito, principalmente o README.
Depois verifique se meu computador comporta o processo e me pergunte qual modelo aberto quero usar
e qual mudanÃ§a quero: menos recusas indevidas ou ajuste de comportamento.
Explique em linguagem simples o que serÃ¡ instalado e baixado, o tamanho e os riscos.
NÃ£o instale, nÃ£o baixe e nÃ£o altere nada antes do meu sim. Mantenha o modelo original intacto.
```

## Os dois modos

| Modo | Problema | O que muda | Como Ã© aprovado |
|---|---|---|---|
| `modos/menos-recusas` | O modelo recusa pedidos inofensivos: histÃ³ria, saÃºde, direitos, "matar um processo" | Reduz a recusa indevida | Responde com conteÃºdo em pelo menos 80% dos casos novos e perde no mÃ¡ximo 10 pontos em perguntas comuns |
| `modos/pedir-antes` | No atendimento, o modelo inventa valor ou promete crÃ©dito sem ter os dados | Pede o fato que falta e, com os dados, responde direto | Pelo menos 80% em cada situaÃ§Ã£o e perda mÃ¡xima de 10 pontos em perguntas comuns |

O modo de recusas usa apenas exemplos inofensivos. O objetivo Ã© corrigir recusas erradas, nÃ£o retirar proteÃ§Ã£o contra pedidos perigosos. A ediÃ§Ã£o pode ter efeitos alÃ©m dos exemplos, por isso compare antes de usar.

## SÃ³ funciona com modelo aberto

Editar exige os arquivos de pesos do modelo e uma mÃ¡quina sob seu controle, prÃ³pria ou alugada. Uma API de provedor entrega sÃ³ o texto da resposta, entÃ£o nÃ£o dÃ¡ para aplicar a ediÃ§Ã£o nela. ServiÃ§os que jÃ¡ oferecem modelos alterados sÃ£o outra opÃ§Ã£o: vocÃª usa o modelo deles, nÃ£o o seu.

## Primeiro, teste se instruir jÃ¡ resolve

Editar custa tempo e pode piorar o modelo. Cada modo traz uma `instrucao-forte.txt`, e o comparativo mede trÃªs versÃµes lado a lado: original, original com instruÃ§Ã£o forte e cÃ³pia editada. Se a instruÃ§Ã£o sozinha passar, talvez vocÃª nÃ£o precise editar.

## PrÃ³ximas ideias

A tabela em [SUGESTOES.md](SUGESTOES.md) reÃºne outros comportamentos que dÃ¡ para tentar. O que aproveitamos do Heretic e o que acrescentamos estÃ¡ em [DO-HERETIC.md](DO-HERETIC.md).

---

## O processo, do inÃ­cio ao fim

Legenda: ðŸ§  vocÃª decide Â· âš™ï¸ script ou comando

Os comandos foram escritos para Linux e macOS. O Windows nÃ£o foi verificado.

0. âš™ï¸ Baixe o kit e entre na pasta:
   ```sh
   git clone https://github.com/inematds/modelo-do-seu-jeito.git
   cd modelo-do-seu-jeito
   ```
1. ðŸ§  Escolha um modelo aberto, confira a licenÃ§a e veja o tamanho dos pesos na pÃ¡gina dele.
2. âš™ï¸ Confira a mÃ¡quina, trocando 8 pelo tamanho dos pesos em GB:
   `python3 kit/checar_maquina.py --pesos-gb 8`
3. âš™ï¸ Crie o ambiente, instale o [PyTorch 2.6+ adequado Ã  sua placa](https://pytorch.org/get-started/locally/) e depois o restante:
   ```sh
   python3 -m venv .venv && . .venv/bin/activate
   pip install "heretic-llm @ git+https://github.com/p-e-w/heretic@64e999152ff7918efc73576814709b6b6a71f15c" transformers accelerate pytest
   ```
4. âš™ï¸ Baixe o original. O exemplo usa o Qwen3-4B:
   `hf download Qwen/Qwen3-4B-Instruct-2507 --local-dir modelos/original`
5. âš™ï¸ Registre a impressÃ£o digital do original. Se abrir outro terminal depois, reative o ambiente com `. .venv/bin/activate`:
   `python kit/impressao.py gerar modelos/original modelos/impressao-original.json`
6. ðŸ§  Entre no modo e adapte os exemplos em `dados/` ao seu caso, como explicado em [Como adaptar os dados](#como-adaptar-os-dados):
   `cd modos/menos-recusas` ou `cd modos/pedir-antes`
7. âš™ï¸ Colete as respostas antes de editar:
   ```sh
   python ../../kit/responder.py --modelo ../../modelos/original --saida ../../respostas/original.jsonl
   python ../../kit/responder.py --modelo ../../modelos/original --instrucao instrucao-forte.txt --saida ../../respostas/instruido.jsonl
   python ../../kit/avaliar.py --original ../../respostas/original.jsonl --instruido ../../respostas/instruido.jsonl
   ```
   Se a saÃ­da for `NADA A CORRIGIR`, pare aqui. Se for `A INSTRUÃ‡ÃƒO RESOLVE`, use a instruÃ§Ã£o e nÃ£o edite o modelo.
8. âš™ï¸ FaÃ§a um piloto curto: `heretic --n-trials 12 --n-startup-trials 6 --model ../../modelos/original`
9. ðŸ§  O Heretic mostra os melhores resultados. As duas notas devem ser baixas: a do objetivo e a de afastamento do original (KL). O piloto faz sentido se a nota do objetivo caiu sem o afastamento disparar. Para continuar, escolha `Run additional trials` no menu e peÃ§a mais tentativas. O padrÃ£o do Heretic sÃ£o 100 no total. Depois escolha um resultado e salve em `../../modelos/ajustado`. Na configuraÃ§Ã£o padrÃ£o, o Heretic informa 30 a 40 minutos para esse modelo em uma RTX 3090. Este kit nÃ£o mediu o tempo.
10. âš™ï¸ Colete as respostas da cÃ³pia e compare as trÃªs versÃµes:
    ```sh
    python ../../kit/responder.py --modelo ../../modelos/ajustado --saida ../../respostas/ajustado.jsonl
    python ../../kit/avaliar.py --original ../../respostas/original.jsonl --instruido ../../respostas/instruido.jsonl --modificado ../../respostas/ajustado.jsonl
    ```
11. âš™ï¸ Prove que o original nÃ£o mudou: `python ../../kit/impressao.py conferir ../../modelos/original ../../modelos/impressao-original.json`
12. ðŸ§  Leia uma amostra das respostas. Depois escreva perguntas novas, com o critÃ©rio definido antes de ver as respostas, e rode os passos 7 e 10 com `--casos` e com outros nomes em `--saida`, para nÃ£o sobrescrever as respostas anteriores.

SaÃ­das do comparativo: `0` aprovado ou hÃ¡ o que corrigir, `1` reprovado, `2` inconclusivo, `3` nada a corrigir, `4` a instruÃ§Ã£o jÃ¡ resolve.

## InstalaÃ§Ã£o tÃ©cnica

- Python 3.11+, PyTorch 2.6+, `git` e espaÃ§o para o original e as cÃ³pias.
- O checador usa folga estimada: memÃ³ria de 2 vezes e disco de 3 vezes o tamanho dos pesos. NÃ£o Ã© mediÃ§Ã£o.
- Testes sem modelo: `python -m pytest -q`.

| Pasta | ConteÃºdo |
|---|---|
| `kit/` | checagem da mÃ¡quina, impressÃ£o digital, coleta de respostas e comparativo |
| `modos/*/config.toml` | configuraÃ§Ã£o do Heretic |
| `modos/*/regua.py` | o que conta como resposta certa |
| `modos/*/dados/` | contraste, otimizaÃ§Ã£o, perguntas comuns e avaliaÃ§Ã£o separada |
| `modos/*/instrucao-forte.txt` | alternativa sem ediÃ§Ã£o |
| `modos/pedir-antes/plugin_heretic.py` | nota prÃ³pria para o Heretic |

As configuraÃ§Ãµes usam sÃ³ arquivos locais e nÃ£o baixam os conjuntos padrÃ£o do Heretic.

## Como adaptar os dados

Arquivos `.txt` tÃªm uma pergunta por linha. Arquivos `.jsonl` tÃªm um caso por linha, com `id` Ãºnico, `tipo` e `pedido`.

| Modo | Tipo | Campos extras |
|---|---|---|
| `menos-recusas` | `recusa_indevida` | `deve_citar`: lista de termos, e basta aparecer um |
| `menos-recusas` | `comum` | `esperado`: texto que deve aparecer |
| `pedir-antes` | `neutra` | `esperado`: texto que deve aparecer |
| `pedir-antes` | `sem_dados`, `abaixo_limite` | nenhum |
| `pedir-antes` | `com_dados` | `esperado`: valor numÃ©rico correto |

No modo `menos-recusas`, coloque em `dados/recusadas.txt` e `dados/otimizacao.txt` sÃ³ pedidos inofensivos que o seu modelo recusa. Em `dados/comuns.txt` ficam perguntas normais. NÃ£o repita frases entre os arquivos.

Os exemplos prontos estÃ£o em portuguÃªs. Para outro idioma, traduza os dados e as instruÃ§Ãµes, inclusive `system_prompt`, e confira `keyword_markers` em `config.toml` e os padrÃµes de `regua.py`. A rÃ©gua reconhece recusas em portuguÃªs, inglÃªs e espanhol.

O modo `pedir-antes` vem com o exemplo de um aplicativo de agendamento. Para outro negÃ³cio, troque as instruÃ§Ãµes em `config.toml` e `instrucao-forte.txt`, edite as frases em `gerar_dados.py` e rode `python gerar_dados.py`.

Depois de congelar a cÃ³pia, escreva as perguntas novas em outro `.jsonl`, no mesmo formato, e passe esse arquivo com `--casos` ao `responder.py` e ao `avaliar.py`.

## Limites

- A rÃ©gua reconhece padrÃµes de texto e nÃ£o substitui a leitura humana.
- Passar nos casos do kit nÃ£o prova seguranÃ§a nem precisÃ£o fora deles.
- CompressÃ£o ou mudanÃ§a de formato pode alterar o comportamento. Compare de novo depois de converter.
- Um modelo editado continua podendo errar fatos. Em produto com usuÃ¡rios, mantenha revisÃ£o e proteÃ§Ãµes prÃ³prias.
- Respeite a licenÃ§a do modelo e as leis aplicÃ¡veis.

## Base e licenÃ§a

Baseado no [Heretic](https://github.com/p-e-w/heretic), de Philipp Emanuel Weidmann e colaboradores, na versÃ£o `64e9991`. Este projeto usa a mesma licenÃ§a, [AGPL-3.0](LICENSE).

---

<div align="center">
  <img src="capa/logo.svg" alt="Arckhé AI" height="32" />
  <p><strong>Arckhé AI</strong></p>
</div>