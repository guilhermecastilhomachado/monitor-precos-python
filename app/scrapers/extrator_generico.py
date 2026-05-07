import re
from decimal import Decimal, InvalidOperation

import requests
from bs4 import BeautifulSoup

from app.config import TIMEOUT_REQUISICAO, USER_AGENT


def baixar_html(url: str) -> str:
    headers = {"User-Agent": USER_AGENT}
    resposta = requests.get(url, headers=headers, timeout=TIMEOUT_REQUISICAO)
    resposta.raise_for_status()
    return resposta.text


def selecionar_texto(soup: BeautifulSoup, seletor_css: str) -> str | None:
    if not seletor_css:
        return None

    elemento = soup.select_one(seletor_css)
    if not elemento:
        return None

    return elemento.get_text(" ", strip=True)


def normalizar_preco(texto: str | None) -> Decimal | None:
    if not texto:
        return None

    texto_limpo = texto.strip()
    texto_limpo = texto_limpo.replace("R$", "").replace("r$", "")
    texto_limpo = texto_limpo.replace("\xa0", " ").strip()

    numero = re.sub(r"[^0-9,.\-]", "", texto_limpo)

    if not numero:
        return None

    if "," in numero and "." in numero:
        numero = numero.replace(".", "").replace(",", ".")
    elif "," in numero:
        numero = numero.replace(",", ".")

    try:
        return Decimal(numero)
    except InvalidOperation:
        return None


def extrair_dados_genericos(
    html: str,
    seletor_titulo: str,
    seletor_preco: str,
    seletor_preco_original: str | None = None,
    seletor_disponibilidade: str | None = None,
) -> dict:
    soup = BeautifulSoup(html, "lxml")

    titulo = selecionar_texto(soup, seletor_titulo)
    preco_texto = selecionar_texto(soup, seletor_preco)
    preco_original_texto = selecionar_texto(soup, seletor_preco_original)
    disponibilidade_texto = selecionar_texto(soup, seletor_disponibilidade)

    preco_atual = normalizar_preco(preco_texto)
    preco_original = normalizar_preco(preco_original_texto)

    disponivel = True
    if disponibilidade_texto:
        texto_lower = disponibilidade_texto.lower()
        if "indispon" in texto_lower or "esgotado" in texto_lower:
            disponivel = False

    return {
        "titulo": titulo,
        "preco_atual": preco_atual,
        "preco_original": preco_original,
        "disponivel": disponivel,
        "observacao": None,
    }