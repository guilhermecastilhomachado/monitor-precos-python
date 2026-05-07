from app.database import SessionLocal
from app.models import ProdutoMonitorado


if __name__ == "__main__":
    session = SessionLocal()
    try:
        produtos = session.query(ProdutoMonitorado).order_by(ProdutoMonitorado.id.asc()).all()

        if not produtos:
            print("Nenhum produto monitorado cadastrado.")
        else:
            print("=== Produtos monitorados ===")
            for produto in produtos:
                print(
                    f"ID: {produto.id} | "
                    f"Nome: {produto.nome} | "
                    f"Loja: {produto.loja} | "
                    f"Categoria: {produto.categoria or '-'} | "
                    f"Preco alvo: {produto.preco_alvo if produto.preco_alvo is not None else '-'} | "
                    f"Ativo: {produto.ativo}"
                )
    finally:
        session.close()