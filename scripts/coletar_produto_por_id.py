from app.services.coletor import coletar_produto


if __name__ == "__main__":
    produto_id = int(input("Informe o ID do produto monitorado: ").strip())

    historico = coletar_produto(produto_id)

    print("Coleta realizada com sucesso.")
    print(f"Produto ID: {historico.produto_id}")
    print(f"Preco atual: {historico.preco_atual}")
    print(f"Preco original: {historico.preco_original}")
    print(f"Desconto percentual: {historico.desconto_percentual}")
    print(f"Variacao absoluta: {historico.variacao_absoluta}")
    print(f"Variacao percentual: {historico.variacao_percentual}")
    print(f"Atingiu preco alvo: {historico.atingiu_preco_alvo}")
    print(f"Disponivel: {historico.disponivel}")
    print(f"Observacao: {historico.observacao}")