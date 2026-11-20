# O que vem do Heretic

O [Heretic](https://github.com/p-e-w/heretic) é a ferramenta que altera o modelo. Este kit não copia nem substitui o programa: ele o instala como dependência, na versão `64e9991`, e acrescenta um jeito de preparar e comprovar a mudança.

## Como o Heretic funciona

1. Recebe dois conjuntos de exemplos: o comportamento desejado e o indesejado.
2. Observa a diferença interna do modelo entre os dois.
3. Altera uma cópia dos pesos usando um modificador. O padrão atual é o ARA, e também existe a abliteração.
4. Dá notas ao resultado: uma para o objetivo e outra para o quanto o modelo se afastou do original (KL).
5. Repete com o Optuna, que busca o melhor equilíbrio entre as notas.
6. Deixa você escolher um resultado e salvar, conversar com ele ou rodar benchmarks.

## O que usamos

| Recurso do Heretic | Uso neste kit |
|---|---|
| Modificador ARA | Os dois modos |
| `KeywordRate` | Nota de recusas indevidas |
| `KLDivergence` | Medida de afastamento nas perguntas comuns |
| Plugin de nota | `PromessaSemDados`, do modo de atendimento |
| Conjuntos em arquivo de texto | Dados locais, sem baixar os conjuntos padrão |
| Instrução por conjunto (`system_prompt`) | Contraste do modo de atendimento |
| Opções de linha de comando | Piloto com menos tentativas |

## O que acrescentamos

- Dados inofensivos para recusas indevidas, em português.
- Modo de comportamento para atendimento, com conferência do valor exato.
- Comparação em três versões: original, instrução forte e cópia editada.
- Casos separados para a aprovação final.
- Parada automática quando o original já cumpre os mínimos.
- Conferência de entrada idêntica e aviso de respostas cortadas.
- Impressão digital para provar que o original não mudou.

## Vale olhar no repositório

- `config.noslop.toml`, `config.nosyco.toml`, `config.terse.toml`, `config.nohumor.toml` e `config.emotions.toml`, que alimentam [SUGESTOES.md](SUGESTOES.md).
- `config.default.toml`, com todas as opções.
- `src/heretic/scorers/`, como modelo para criar novas notas.
- O recurso de reprodução, que registra como refazer um modelo.

## Crédito e licença

Heretic é de Philipp Emanuel Weidmann e colaboradores, sob AGPL-3.0-or-later. Este projeto também usa AGPL-3.0. O plugin depende das interfaces do Heretic.

Citação sugerida pelo projeto: Weidmann, Philipp Emanuel. *Heretic: Training-free language model modification*. GitHub, 2025. https://github.com/p-e-w/heretic
