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


st.set_page_config(page_title="Monitor de Precos", layout="wide")
st.title("Monitor de Preços")

session = SessionLocal()

try:
    produtos = session.query(ProdutoMonitorado).filter_by(ativo=True).order_by(ProdutoMonitorado.nome.asc()).all()

    if not produtos:
        st.warning("Nenhum produto monitorado cadastrado ainda.")
        st.stop()

    opcoes = {
        f"{produto.id} - {produto.nome} ({produto.loja})": produto.id
        for produto in produtos
    }

    produto_escolhido = st.selectbox("Selecione um produto monitorado", list(opcoes.keys()))
    produto_id = opcoes[produto_escolhido]

    historicos = (
        session.query(HistoricoPreco)
        .filter_by(produto_id=produto_id)
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
                "disponivel": h.disponivel,
            }
            for h in historicos
        ]
    )

    ultimo = historicos[-1]
    menor_preco = df["preco_atual"].min()
    maior_preco = df["preco_atual"].max()

    col1, col2, col3 = st.columns(3)
    col1.metric("Preço atual", formatar_moeda(ultimo.preco_atual))
    col2.metric("Menor preço", formatar_moeda(menor_preco))
    col3.metric("Maior preço", formatar_moeda(maior_preco))

    st.subheader("Evolução do preço")
    st.line_chart(df.set_index("data_coleta")["preco_atual"])

    st.subheader("Histórico detalhado")
    st.dataframe(df, use_container_width=True)
finally:
    session.close()