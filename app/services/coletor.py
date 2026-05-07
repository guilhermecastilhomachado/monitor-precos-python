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


def calcular_variacao_absoluta(preco_atual: Decimal, preco_anterior: Decimal | None) -> Decimal | None:
    if preco_anterior is None:
        return None

    variacao = preco_atual - preco_anterior
    return variacao.quantize(Decimal("0.01"))


def calcular_variacao_percentual(preco_atual: Decimal, preco_anterior: Decimal | None) -> Decimal | None:
    if preco_anterior is None or preco_anterior == 0:
        return None

    variacao = ((preco_atual - preco_anterior) / preco_anterior) * Decimal("100")
    return variacao.quantize(Decimal("0.01"))


def verificar_preco_alvo(produto: ProdutoMonitorado, preco_atual: Decimal) -> bool:
    if produto.preco_alvo is None:
        return False

    return preco_atual <= produto.preco_alvo


def montar_observacao(produto: ProdutoMonitorado, atingiu_preco_alvo: bool) -> str | None:
    if atingiu_preco_alvo:
        return f"Preco alvo atingido para o produto {produto.nome}."
    return None


def coletar_produto(produto_id: int) -> HistoricoPreco:
    session = SessionLocal()
    try:
        produto = session.query(ProdutoMonitorado).filter_by(id=produto_id, ativo=True).first()

        if not produto:
            raise ValueError(f"Produto monitorado nao encontrado ou inativo: {produto_id}")

        ultimo_historico = (
            session.query(HistoricoPreco)
            .filter_by(produto_id=produto.id)
            .order_by(HistoricoPreco.data_coleta.desc())
            .first()
        )

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

        preco_anterior = ultimo_historico.preco_atual if ultimo_historico else None
        atingiu_preco_alvo = verificar_preco_alvo(produto, dados["preco_atual"])

        historico = HistoricoPreco(
            produto_id=produto.id,
            titulo_coletado=dados["titulo"] or produto.nome,
            preco_atual=dados["preco_atual"],
            preco_original=dados["preco_original"],
            desconto_percentual=calcular_desconto(dados["preco_original"], dados["preco_atual"]),
            variacao_absoluta=calcular_variacao_absoluta(dados["preco_atual"], preco_anterior),
            variacao_percentual=calcular_variacao_percentual(dados["preco_atual"], preco_anterior),
            atingiu_preco_alvo=atingiu_preco_alvo,
            disponivel=dados["disponivel"],
            observacao=montar_observacao(produto, atingiu_preco_alvo),
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