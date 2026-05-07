from app.database import SessionLocal
from app.models import ProdutoMonitorado
from app.services.coletor import coletar_produto


if __name__ == "__main__":
    session = SessionLocal()

    try:
        produtos = (
            session.query(ProdutoMonitorado)
            .filter_by(ativo=True)
            .order_by(ProdutoMonitorado.id.asc())
            .all()
        )
    finally:
        session.close()

    if not produtos:
        print("Nenhum produto ativo encontrado para coleta.")
        raise SystemExit(0)

    sucessos = []
    erros = []

    print("=== Executando coleta em lote ===")

    for produto in produtos:
        try:
            historico = coletar_produto(produto.id)
            sucessos.append(
                {
                    "produto_id": produto.id,
                    "nome": produto.nome,
                    "preco_atual": historico.preco_atual,
                    "atingiu_preco_alvo": historico.atingiu_preco_alvo,
                }
            )
            print(
                f"[OK] Produto ID {produto.id} - {produto.nome} | "
                f"Preco: {historico.preco_atual} | "
                f"Atingiu alvo: {historico.atingiu_preco_alvo}"
            )
        except Exception as erro:
            erros.append(
                {
                    "produto_id": produto.id,
                    "nome": produto.nome,
                    "erro": str(erro),
                }
            )
            print(f"[ERRO] Produto ID {produto.id} - {produto.nome} | Erro: {erro}")

    print("\n=== Resumo da coleta ===")
    print(f"Sucessos: {len(sucessos)}")
    print(f"Erros: {len(erros)}")

    if erros:
        print("\n=== Produtos com erro ===")
        for erro in erros:
            print(
                f"Produto ID {erro['produto_id']} - {erro['nome']} | "
                f"Erro: {erro['erro']}"
            )