from app.services.coletor import coletar_todos_produtos_ativos

if __name__ == "__main__":
    historicos = coletar_todos_produtos_ativos()
    print(f"Coleta finalizada. Registros salvos: {len(historicos)}")