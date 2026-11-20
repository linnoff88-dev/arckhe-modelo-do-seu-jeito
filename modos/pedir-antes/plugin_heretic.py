"""Scorer do Heretic: fração de casos em que o modelo fere a regra de perguntar antes."""

import json
import sys
from pathlib import Path

from pydantic import BaseModel, Field

sys.path.insert(0, str(Path(__file__).resolve().parent))

from heretic.scorer import Context, Score, Scorer  # noqa: E402
from heretic.utils import Prompt, print  # noqa: E402
from regua import avaliar_caso  # noqa: E402


class Settings(BaseModel):
    arquivo: str = Field(
        default="dados/otimizacao.jsonl",
        description="JSONL com os casos usados durante a otimização.",
    )


class PromessaSemDados(Scorer):
    settings: Settings

    @property
    def score_name(self) -> str:
        return "Falhas de perguntar antes"

    def init(self, ctx: Context) -> None:
        linhas = Path(self.settings.arquivo).read_text(encoding="utf-8").splitlines()
        self.casos = [json.loads(linha) for linha in linhas if linha.strip()]
        sistema = self.heretic_settings.system_prompt
        self.prompts = [Prompt(system=sistema, user=c["pedido"]) for c in self.casos]
        print(f"* [bold]{len(self.casos)}[/] casos carregados")

    def get_score(self, ctx: Context) -> Score:
        respostas = ctx.get_responses(self.prompts)
        falhas = sum(
            not avaliar_caso(caso, resposta)
            for caso, resposta in zip(self.casos, respostas, strict=True)
        )
        texto = f"{falhas}/{len(self.casos)}"
        return Score(
            value=falhas / len(self.casos),
            rich_display=f"[bold]{texto}[/]",
            md_display=texto,
        )
