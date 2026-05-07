from decimal import Decimal

from app.database import SessionLocal
from app.models import ProdutoMonitorado


def ler_decimal_opcional(texto: str):
    texto = texto.strip()
    if not texto:
        return None
    return Decimal(texto.replace(",", "."))


if __name__ == "__main__":
    print("=== Cadastro de produto monitorado ===")

    nome = input("Nome do produto: ").strip()
    loja = input("Loja: ").strip()
    url = input("URL publica do produto: ").strip()
    categoria = input("Categoria (opcional): ").strip() or None

    seletor_titulo = input("Seletor CSS do titulo [h1]: ").strip() or "h1"
    seletor_preco = input("Seletor CSS do preco atual: ").strip()
    seletor_preco_original = input("Seletor CSS do preco original (opcional): ").strip() or None
    seletor_disponibilidade = input("Seletor CSS da disponibilidade (opcional): ").strip() or None

    preco_alvo_texto = input("Preco alvo (opcional): ")
    preco_alvo = ler_decimal_opcional(preco_alvo_texto)

    session = SessionLocal()
    try:
        produto = ProdutoMonitorado(
            nome=nome,
            loja=loja,
            url=url,
            categoria=categoria,
            seletor_titulo=seletor_titulo,
            seletor_preco=seletor_preco,
            seletor_preco_original=seletor_preco_original,
            seletor_disponibilidade=seletor_disponibilidade,
            preco_alvo=preco_alvo,
            ativo=True,
        )

        session.add(produto)
        session.commit()
        session.refresh(produto)

        print(f"Produto cadastrado com sucesso. ID: {produto.id}")
    finally:
        session.close()