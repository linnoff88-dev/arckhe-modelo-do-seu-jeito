ï»¿# Modelo do Seu Jeito

<div align="center">
  <img src="capa/logo.svg" alt="Arckhé AI" height="48" />
  <p><strong>Arckhé AI</strong></p>
</div>


ê°Å¸Å½Â¬ VêÂ­deo: https://www.youtube.com/watch?v=3U8jk69yt3M

[![Modelo do Seu Jeito](guia/assets/banner.jpg)](https://inematds.github.io/modelo-do-seu-jeito/guia/)

**ê°Å¸â¡Â§ê°Å¸â¡Â· [PortuguêÂªs](README.md) êÂ· ê°Å¸â¡Âºê°Å¸â¡Â¸ [English](README.en.md) êÂ· ê°Å¸â¡Âªê°Å¸â¡Â¸ [EspaêÂ±ol](README.es.md)**

## O que êÂ©

Seu modelo de IA aberto êÂ s vezes recusa uma pergunta inofensiva ou promete o que nêÂ£o sabe? Este kit ajuda vocêÂª a ajustar uma cêÂ³pia desse modelo no seu computador, sem treinar do zero. Ele traz dois caminhos: **menos recusas indevidas** e **ajuste de comportamento**. Serve para quem usa modelos abertos e quer comprovar a mudanêÂ§a, comparando o antes e o depois. VocêÂª precisa de uma mêÂ¡quina capaz de rodar o modelo. A ediêÂ§êÂ£o êÂ© feita com o [Heretic](https://github.com/p-e-w/heretic).

> **Estado atual:** o kit ainda nêÂ£o foi executado em um modelo. RêÂ©guas, dados, configuraêÂ§êÂµes e comparativo têÂªm testes automêÂ¡ticos sem modelo, e as configuraêÂ§êÂµes passaram na validaêÂ§êÂ£o do Heretic. Por isso nêÂ£o hêÂ¡ resultado medido para mostrar. O primeiro uso real êÂ© um teste.

## ê°Å¸ââ Guia

Guia completo: **https://inematds.github.io/modelo-do-seu-jeito/guia/**

## Comece pedindo êÂ  sua IA

O Claude Code e o Codex sêÂ£o assistentes que trabalham no seu computador e precisam estar instalados, com conta ativa. Abra um deles em uma pasta vazia e cole:

```text
Leia o repositêÂ³rio https://github.com/inematds/modelo-do-seu-jeito, principalmente o README.
Depois verifique se meu computador comporta o processo e me pergunte qual modelo aberto quero usar
e qual mudanêÂ§a quero: menos recusas indevidas ou ajuste de comportamento.
Explique em linguagem simples o que serêÂ¡ instalado e baixado, o tamanho e os riscos.
NêÂ£o instale, nêÂ£o baixe e nêÂ£o altere nada antes do meu sim. Mantenha o modelo original intacto.
```

## Os dois modos

| Modo | Problema | O que muda | Como êÂ© aprovado |
|---|---|---|---|
| `modos/menos-recusas` | O modelo recusa pedidos inofensivos: histêÂ³ria, saêÂºde, direitos, "matar um processo" | Reduz a recusa indevida | Responde com conteêÂºdo em pelo menos 80% dos casos novos e perde no mêÂ¡ximo 10 pontos em perguntas comuns |
| `modos/pedir-antes` | No atendimento, o modelo inventa valor ou promete crêÂ©dito sem ter os dados | Pede o fato que falta e, com os dados, responde direto | Pelo menos 80% em cada situaêÂ§êÂ£o e perda mêÂ¡xima de 10 pontos em perguntas comuns |

O modo de recusas usa apenas exemplos inofensivos. O objetivo êÂ© corrigir recusas erradas, nêÂ£o retirar proteêÂ§êÂ£o contra pedidos perigosos. A ediêÂ§êÂ£o pode ter efeitos alêÂ©m dos exemplos, por isso compare antes de usar.

## SêÂ³ funciona com modelo aberto

Editar exige os arquivos de pesos do modelo e uma mêÂ¡quina sob seu controle, prêÂ³pria ou alugada. Uma API de provedor entrega sêÂ³ o texto da resposta, entêÂ£o nêÂ£o dêÂ¡ para aplicar a ediêÂ§êÂ£o nela. ServiêÂ§os que jêÂ¡ oferecem modelos alterados sêÂ£o outra opêÂ§êÂ£o: vocêÂª usa o modelo deles, nêÂ£o o seu.

## Primeiro, teste se instruir jêÂ¡ resolve

Editar custa tempo e pode piorar o modelo. Cada modo traz uma `instrucao-forte.txt`, e o comparativo mede trêÂªs versêÂµes lado a lado: original, original com instruêÂ§êÂ£o forte e cêÂ³pia editada. Se a instruêÂ§êÂ£o sozinha passar, talvez vocêÂª nêÂ£o precise editar.

## PrêÂ³ximas ideias

A tabela em [SUGESTOES.md](SUGESTOES.md) reêÂºne outros comportamentos que dêÂ¡ para tentar. O que aproveitamos do Heretic e o que acrescentamos estêÂ¡ em [DO-HERETIC.md](DO-HERETIC.md).

---

## O processo, do inêÂ­cio ao fim

Legenda: ê°Å¸Â§Â  vocêÂª decide êÂ· ê¢Å¡â¢ê¯Â¸Â script ou comando

Os comandos foram escritos para Linux e macOS. O Windows nêÂ£o foi verificado.

0. ê¢Å¡â¢ê¯Â¸Â Baixe o kit e entre na pasta:
   ```sh
   git clone https://github.com/inematds/modelo-do-seu-jeito.git
   cd modelo-do-seu-jeito
   ```
1. ê°Å¸Â§Â  Escolha um modelo aberto, confira a licenêÂ§a e veja o tamanho dos pesos na pêÂ¡gina dele.
2. ê¢Å¡â¢ê¯Â¸Â Confira a mêÂ¡quina, trocando 8 pelo tamanho dos pesos em GB:
   `python3 kit/checar_maquina.py --pesos-gb 8`
3. ê¢Å¡â¢ê¯Â¸Â Crie o ambiente, instale o [PyTorch 2.6+ adequado êÂ  sua placa](https://pytorch.org/get-started/locally/) e depois o restante:
   ```sh
   python3 -m venv .venv && . .venv/bin/activate
   pip install "heretic-llm @ git+https://github.com/p-e-w/heretic@64e999152ff7918efc73576814709b6b6a71f15c" transformers accelerate pytest
   ```
4. ê¢Å¡â¢ê¯Â¸Â Baixe o original. O exemplo usa o Qwen3-4B:
   `hf download Qwen/Qwen3-4B-Instruct-2507 --local-dir modelos/original`
5. ê¢Å¡â¢ê¯Â¸Â Registre a impressêÂ£o digital do original. Se abrir outro terminal depois, reative o ambiente com `. .venv/bin/activate`:
   `python kit/impressao.py gerar modelos/original modelos/impressao-original.json`
6. ê°Å¸Â§Â  Entre no modo e adapte os exemplos em `dados/` ao seu caso, como explicado em [Como adaptar os dados](#como-adaptar-os-dados):
   `cd modos/menos-recusas` ou `cd modos/pedir-antes`
7. ê¢Å¡â¢ê¯Â¸Â Colete as respostas antes de editar:
   ```sh
   python ../../kit/responder.py --modelo ../../modelos/original --saida ../../respostas/original.jsonl
   python ../../kit/responder.py --modelo ../../modelos/original --instrucao instrucao-forte.txt --saida ../../respostas/instruido.jsonl
   python ../../kit/avaliar.py --original ../../respostas/original.jsonl --instruido ../../respostas/instruido.jsonl
   ```
   Se a saêÂ­da for `NADA A CORRIGIR`, pare aqui. Se for `A INSTRUêâ¡êÆO RESOLVE`, use a instruêÂ§êÂ£o e nêÂ£o edite o modelo.
8. ê¢Å¡â¢ê¯Â¸Â FaêÂ§a um piloto curto: `heretic --n-trials 12 --n-startup-trials 6 --model ../../modelos/original`
9. ê°Å¸Â§Â  O Heretic mostra os melhores resultados. As duas notas devem ser baixas: a do objetivo e a de afastamento do original (KL). O piloto faz sentido se a nota do objetivo caiu sem o afastamento disparar. Para continuar, escolha `Run additional trials` no menu e peêÂ§a mais tentativas. O padrêÂ£o do Heretic sêÂ£o 100 no total. Depois escolha um resultado e salve em `../../modelos/ajustado`. Na configuraêÂ§êÂ£o padrêÂ£o, o Heretic informa 30 a 40 minutos para esse modelo em uma RTX 3090. Este kit nêÂ£o mediu o tempo.
10. ê¢Å¡â¢ê¯Â¸Â Colete as respostas da cêÂ³pia e compare as trêÂªs versêÂµes:
    ```sh
    python ../../kit/responder.py --modelo ../../modelos/ajustado --saida ../../respostas/ajustado.jsonl
    python ../../kit/avaliar.py --original ../../respostas/original.jsonl --instruido ../../respostas/instruido.jsonl --modificado ../../respostas/ajustado.jsonl
    ```
11. ê¢Å¡â¢ê¯Â¸Â Prove que o original nêÂ£o mudou: `python ../../kit/impressao.py conferir ../../modelos/original ../../modelos/impressao-original.json`
12. ê°Å¸Â§Â  Leia uma amostra das respostas. Depois escreva perguntas novas, com o critêÂ©rio definido antes de ver as respostas, e rode os passos 7 e 10 com `--casos` e com outros nomes em `--saida`, para nêÂ£o sobrescrever as respostas anteriores.

SaêÂ­das do comparativo: `0` aprovado ou hêÂ¡ o que corrigir, `1` reprovado, `2` inconclusivo, `3` nada a corrigir, `4` a instruêÂ§êÂ£o jêÂ¡ resolve.

## InstalaêÂ§êÂ£o têÂ©cnica

- Python 3.11+, PyTorch 2.6+, `git` e espaêÂ§o para o original e as cêÂ³pias.
- O checador usa folga estimada: memêÂ³ria de 2 vezes e disco de 3 vezes o tamanho dos pesos. NêÂ£o êÂ© mediêÂ§êÂ£o.
- Testes sem modelo: `python -m pytest -q`.

| Pasta | ConteêÂºdo |
|---|---|
| `kit/` | checagem da mêÂ¡quina, impressêÂ£o digital, coleta de respostas e comparativo |
| `modos/*/config.toml` | configuraêÂ§êÂ£o do Heretic |
| `modos/*/regua.py` | o que conta como resposta certa |
| `modos/*/dados/` | contraste, otimizaêÂ§êÂ£o, perguntas comuns e avaliaêÂ§êÂ£o separada |
| `modos/*/instrucao-forte.txt` | alternativa sem ediêÂ§êÂ£o |
| `modos/pedir-antes/plugin_heretic.py` | nota prêÂ³pria para o Heretic |

As configuraêÂ§êÂµes usam sêÂ³ arquivos locais e nêÂ£o baixam os conjuntos padrêÂ£o do Heretic.

## Como adaptar os dados

Arquivos `.txt` têÂªm uma pergunta por linha. Arquivos `.jsonl` têÂªm um caso por linha, com `id` êÂºnico, `tipo` e `pedido`.

| Modo | Tipo | Campos extras |
|---|---|---|
| `menos-recusas` | `recusa_indevida` | `deve_citar`: lista de termos, e basta aparecer um |
| `menos-recusas` | `comum` | `esperado`: texto que deve aparecer |
| `pedir-antes` | `neutra` | `esperado`: texto que deve aparecer |
| `pedir-antes` | `sem_dados`, `abaixo_limite` | nenhum |
| `pedir-antes` | `com_dados` | `esperado`: valor numêÂ©rico correto |

No modo `menos-recusas`, coloque em `dados/recusadas.txt` e `dados/otimizacao.txt` sêÂ³ pedidos inofensivos que o seu modelo recusa. Em `dados/comuns.txt` ficam perguntas normais. NêÂ£o repita frases entre os arquivos.

Os exemplos prontos estêÂ£o em portuguêÂªs. Para outro idioma, traduza os dados e as instruêÂ§êÂµes, inclusive `system_prompt`, e confira `keyword_markers` em `config.toml` e os padrêÂµes de `regua.py`. A rêÂ©gua reconhece recusas em portuguêÂªs, inglêÂªs e espanhol.

O modo `pedir-antes` vem com o exemplo de um aplicativo de agendamento. Para outro negêÂ³cio, troque as instruêÂ§êÂµes em `config.toml` e `instrucao-forte.txt`, edite as frases em `gerar_dados.py` e rode `python gerar_dados.py`.

Depois de congelar a cêÂ³pia, escreva as perguntas novas em outro `.jsonl`, no mesmo formato, e passe esse arquivo com `--casos` ao `responder.py` e ao `avaliar.py`.

## Limites

- A rêÂ©gua reconhece padrêÂµes de texto e nêÂ£o substitui a leitura humana.
- Passar nos casos do kit nêÂ£o prova seguranêÂ§a nem precisêÂ£o fora deles.
- CompressêÂ£o ou mudanêÂ§a de formato pode alterar o comportamento. Compare de novo depois de converter.
- Um modelo editado continua podendo errar fatos. Em produto com usuêÂ¡rios, mantenha revisêÂ£o e proteêÂ§êÂµes prêÂ³prias.
- Respeite a licenêÂ§a do modelo e as leis aplicêÂ¡veis.

## Base e licenêÂ§a

Baseado no [Heretic](https://github.com/p-e-w/heretic), de Philipp Emanuel Weidmann e colaboradores, na versêÂ£o `64e9991`. Este projeto usa a mesma licenêÂ§a, [AGPL-3.0](LICENSE).

---

<div align="center">
  <img src="capa/logo.svg" alt="Arckhé AI" height="32" />
  <p><strong>Arckhé AI</strong></p>
</div>