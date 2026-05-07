import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

import pandas as pd
import streamlit as st

from app.database import SessionLocal
from app.models import HistoricoPreco, ProdutoMonitorado


def formatar_moeda(valor):
    if valor is None:
        return "-"
    return f"R$ {float(valor):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def formatar_percentual(valor):
    if valor is None:
        return "-"
    return f"{float(valor):.2f}%".replace(".", ",")


st.set_page_config(page_title="Monitor de Precos", layout="wide")
st.title("Monitor de Preços")

session = SessionLocal()

try:
    produtos = (
        session.query(ProdutoMonitorado)
        .filter_by(ativo=True)
        .order_by(ProdutoMonitorado.nome.asc())
        .all()
    )

    if not produtos:
        st.warning("Nenhum produto monitorado cadastrado ainda.")
        st.stop()

    mapa_produtos = {
        f"{produto.id} - {produto.nome} ({produto.loja})": produto
        for produto in produtos
    }

    produto_escolhido = st.selectbox("Selecione um produto monitorado", list(mapa_produtos.keys()))
    produto = mapa_produtos[produto_escolhido]

    historicos = (
        session.query(HistoricoPreco)
        .filter_by(produto_id=produto.id)
        .order_by(HistoricoPreco.data_coleta.asc())
        .all()
    )

    if not historicos:
        st.info("Ainda nao existe historico para este produto.")
        st.stop()

    df = pd.DataFrame(
        [
            {
                "data_coleta": h.data_coleta,
                "preco_atual": float(h.preco_atual),
                "preco_original": float(h.preco_original) if h.preco_original is not None else None,
                "desconto_percentual": float(h.desconto_percentual) if h.desconto_percentual is not None else None,
                "variacao_absoluta": float(h.variacao_absoluta) if h.variacao_absoluta is not None else None,
                "variacao_percentual": float(h.variacao_percentual) if h.variacao_percentual is not None else None,
                "atingiu_preco_alvo": h.atingiu_preco_alvo,
                "disponivel": h.disponivel,
                "observacao": h.observacao,
            }
            for h in historicos
        ]
    )

    ultimo = historicos[-1]
    menor_preco = df["preco_atual"].min()
    maior_preco = df["preco_atual"].max()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Preço atual", formatar_moeda(ultimo.preco_atual))
    col2.metric("Menor preço", formatar_moeda(menor_preco))
    col3.metric("Maior preço", formatar_moeda(maior_preco))
    col4.metric("Preço alvo", formatar_moeda(produto.preco_alvo))

    col5, col6 = st.columns(2)
    col5.metric("Variação absoluta", formatar_moeda(ultimo.variacao_absoluta))
    col6.metric("Variação percentual", formatar_percentual(ultimo.variacao_percentual))

    if ultimo.atingiu_preco_alvo:
        st.success("Preço-alvo atingido nesta coleta.")
    elif produto.preco_alvo is not None:
        st.info("Preço-alvo ainda não foi atingido.")

    st.subheader("Evolução do preço")
    st.line_chart(df.set_index("data_coleta")["preco_atual"])

    st.subheader("Histórico detalhado")
    st.dataframe(df, use_container_width=True)
finally:
    session.close()