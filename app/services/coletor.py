from decimal import Decimal

from app.database import SessionLocal
from app.models import HistoricoPreco, ProdutoMonitorado
from app.scrapers.extrator_generico import baixar_html, extrair_dados_genericos


def calcular_desconto(preco_original: Decimal | None, preco_atual: Decimal | None) -> Decimal | None:
    if not preco_original or not preco_atual:
        return None

    if preco_original <= 0:
        return None

    desconto = ((preco_original - preco_atual) / preco_original) * Decimal("100")
    return desconto.quantize(Decimal("0.01"))


def coletar_produto(produto_id: int) -> HistoricoPreco:
    session = SessionLocal()
    try:
        produto = session.query(ProdutoMonitorado).filter_by(id=produto_id, ativo=True).first()

        if not produto:
            raise ValueError(f"Produto monitorado nao encontrado ou inativo: {produto_id}")

        html = baixar_html(produto.url)

        dados = extrair_dados_genericos(
            html=html,
            seletor_titulo=produto.seletor_titulo,
            seletor_preco=produto.seletor_preco,
            seletor_preco_original=produto.seletor_preco_original,
            seletor_disponibilidade=produto.seletor_disponibilidade,
        )

        if dados["preco_atual"] is None:
            raise ValueError(f"Nao foi possivel extrair o preco atual do produto: {produto.nome}")

        historico = HistoricoPreco(
            produto_id=produto.id,
            titulo_coletado=dados["titulo"] or produto.nome,
            preco_atual=dados["preco_atual"],
            preco_original=dados["preco_original"],
            desconto_percentual=calcular_desconto(dados["preco_original"], dados["preco_atual"]),
            disponivel=dados["disponivel"],
            observacao=dados["observacao"],
        )

        session.add(historico)
        session.commit()
        session.refresh(historico)

        return historico
    finally:
        session.close()


def coletar_todos_produtos_ativos() -> list[HistoricoPreco]:
    session = SessionLocal()
    try:
        produtos = session.query(ProdutoMonitorado).filter_by(ativo=True).all()
        ids = [produto.id for produto in produtos]
    finally:
        session.close()

    historicos = []
    for produto_id in ids:
        historico = coletar_produto(produto_id)
        historicos.append(historico)

    return historicos