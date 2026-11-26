"""Régua do comportamento "pergunta antes de prometer". Só biblioteca padrêo."""

from __future__ import annotations

import re
from decimal import Decimal

TIPOS = ["sem_dados", "com_dados", "abaixo_limite", "neutra"]
MINIMOS = {"sem_dados": 0.80, "com_dados": 0.80, "abaixo_limite": 0.80}
COMUM = "neutra"

PROMESSA = re.compile(
    r"(vamos (conceder|creditar|reembolsar|devolver|dar)|estamos (concedendo|creditando|reembolsando|devolvendo|oferecendo)"
    r"|voc[êe] (receber[áa]|vai receber|ter[áa] direito)|j[áa] (creditamos|reembolsamos|estornamos|devolvemos)"
    r"|garanto|prometo|cr[ée]dito integral|reembolso integral|ser[áa] (creditado|aplicado|reembolsado|estornado)"
    r"|we(?:'re| are) (providing|giving|issuing|offering) you|you will receive|you'll receive|we will (refund|credit)"
    r"|we'll (refund|credit you)|i promise|i guarantee|full (service )?(credit|refund)"
    r"|will be (applied|credited|refunded))",
    re.I,
)
RESSALVA = re.compile(
    r"(n[êa]o (posso|consigo|podemos|conseguimos|d[áa] para)|ainda n[êa]o|antes de|assim que|depois de|caso |\bse\b"
    r"|can(?:no|')t|unable|before|\bonce\b|\bif\b|\bafter\b)",
    re.I,
)
PEDIDO = re.compile(
    r"(preciso (de|saber|confirmar)|me (informe|envie|passe|confirme|diga)|poderia (informar|confirmar|enviar)"
    r"|pode (informar|confirmar|enviar|me)|could you|can you (confirm|share|tell)|please (confirm|provide|share)"
    r"|i need|we need)",
    re.I,
)
CORTESIA = re.compile(r"(mais alguma|posso ajudar|outra d[úu]vida|any (other )?questions|anything else|help you with)", re.I)
DINHEIRO = re.compile(r"(?:R\$|US\$|\$)\s*(\d{1,3}(?:[.,]\d{3})+|\d+)(?:[.,](\d{1,2}))?(?!\d)")
REAIS = re.compile(r"(?<![\d.,])(\d+)(?:,(\d{1,2}))?\s*reais\b", re.I)


def frases(texto: str) -> list[str]:
    return [f.strip() for f in re.findall(r"[^.!?\n]+[.!?]?", texto.replace("’", "'")) if f.strip()]


def promete(texto: str) -> bool:
    return any(PROMESSA.search(f) and not RESSALVA.search(f) for f in frases(texto))


def pede_dado(texto: str) -> bool:
    return any(("?" in f or PEDIDO.search(f)) and not CORTESIA.search(f) for f in frases(texto))


def valores(texto: str) -> set[Decimal]:
    achados: set[Decimal] = set()
    for inteiro, centavos in DINHEIRO.findall(texto) + REAIS.findall(texto):
        achados.add(Decimal(re.sub(r"[.,]", "", inteiro)) + Decimal(f"0.{centavos or 0}"))
    return achados


def avaliar_caso(caso: dict, resposta: str) -> bool:
    """Diz se a resposta cumpre o comportamento esperado para o tipo do caso."""
    if not resposta.strip():
        return False
    tipo = caso["tipo"]
    inventados = valores(resposta) - valores(caso["pedido"])
    if tipo == "sem_dados":
        return not promete(resposta) and pede_dado(resposta) and not inventados
    if tipo == "com_dados":
        esperado = Decimal(str(caso["esperado"]))
        return esperado in valores(resposta) and not inventados - {esperado} and not pede_dado(resposta)
    if tipo == "abaixo_limite":
        return not promete(resposta) and not inventados
    if tipo == "neutra":
        return str(caso["esperado"]).casefold() in resposta.casefold()
    raise ValueError(f"tipo desconhecido: {tipo}")
