from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from app.database import Base


class ProdutoMonitorado(Base):
    __tablename__ = "produtos_monitorados"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(150), nullable=False)
    loja = Column(String(100), nullable=False)
    url = Column(Text, nullable=False, unique=True)
    categoria = Column(String(100), nullable=True)

    seletor_titulo = Column(String(255), nullable=False, default="h1")
    seletor_preco = Column(String(255), nullable=False)
    seletor_preco_original = Column(String(255), nullable=True)
    seletor_disponibilidade = Column(String(255), nullable=True)

    preco_alvo = Column(Numeric(10, 2), nullable=True)
    ativo = Column(Boolean, nullable=False, default=True)
    data_cadastro = Column(DateTime, nullable=False, default=datetime.utcnow)

    historicos = relationship(
        "HistoricoPreco",
        back_populates="produto",
        cascade="all, delete-orphan"
    )


class HistoricoPreco(Base):
    __tablename__ = "historicos_precos"

    id = Column(Integer, primary_key=True, index=True)
    produto_id = Column(Integer, ForeignKey("produtos_monitorados.id"), nullable=False)

    titulo_coletado = Column(String(255), nullable=True)
    preco_atual = Column(Numeric(10, 2), nullable=False)
    preco_original = Column(Numeric(10, 2), nullable=True)
    desconto_percentual = Column(Numeric(5, 2), nullable=True)
    disponivel = Column(Boolean, nullable=False, default=True)
    observacao = Column(String(255), nullable=True)

    data_coleta = Column(DateTime, nullable=False, default=datetime.utcnow)

    produto = relationship("ProdutoMonitorado", back_populates="historicos")