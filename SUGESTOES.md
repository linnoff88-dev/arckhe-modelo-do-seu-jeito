# Sugestões de comportamentos para ajustar

Nenhuma linha abaixo foi testada neste projeto. "Pronta" significa que o Heretic traz uma configuração para isso.

| Comportamento | Exemplo do problema | Ponto de partida no Heretic | Como faríamos | O que medir |
|---|---|---|---|---|
| **Recusas** | Recusa pergunta inofensiva | Pronta: `config.default.toml`, com dados próprios neste kit | Modo `menos-recusas` | Resposta com conteúdo nos casos novos |
| **Bajulação** | Concorda fácil demais, elogia tudo | Pronta: `config.nosyco.toml` | Trocar os exemplos pelo seu contexto | Corrige uma afirmação errada do usuário? |
| **Texto genérico de IA** | "Ótima pergunta!", frases infladas | Pronta: `config.noslop.toml` | Listar as expressões que você quer evitar | Frequência das expressões e qualidade do texto |
| **Formato** | Texto longo quando bastava pouco | Parcial: `config.terse.toml` encurta respostas | Contrastar instruções de formato | Tamanho e se a resposta continua completa |
| **Tom** | Formal, casual ou seco demais | Sem receita: use o contraste de instruções | Mesmas perguntas com dois tons opostos | Leitura humana e classificador de tom |
| **Persona** | Não age no papel desejado | Sem receita: use o contraste de instruções | Exemplos com o papel certo e o errado | Mantém o papel sem inventar fatos? |
| **Linguagem** | Vocabulário ou idioma fora do desejado | Sem receita: use o contraste de instruções | Pares no estilo desejado e no indesejado | Lista de termos e leitura humana |
| **Avisos** | "Como uma IA...", ressalvas em excesso | Parcial: nota por palavras (`KeywordRate`) | Marcar essas frases como o que deve cair | Queda dos avisos, mantendo os realmente úteis |
| **Foco** | Dá atenção ao que não importa | Sem receita: exige nota própria | Criar uma régua do que deve aparecer | Cobertura dos pontos pedidos |
| **Humor** | Piadas fora de hora | Pronta: `config.nohumor.toml` | Usar em assistente de trabalho | Humor nas respostas e qualidade geral |
| **Emoção** | Tom emocional inadequado | Pronta: `config.emotions.toml` | Ajustar os conjuntos de exemplos | Classificador de emoção e leitura humana |

## Como escolher

1. Comece testando uma instrução forte, porque ela é mais barata e fácil de desfazer.
2. Edite só o que se repete e que a instrução não resolveu.
3. Mude um comportamento por vez, sempre a partir do original.
4. Defina antes o que não pode piorar.

Um novo comportamento precisa de exemplos contrastantes, uma nota, perguntas comuns e casos separados para avaliação. A pasta `modos/pedir-antes` serve de modelo.
