# Monitor de Preços (Python)

![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4479A1?style=flat&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)

## Objetivo
Projeto de portfólio em Python para monitoramento de preços em páginas públicas, com coleta automatizada, persistência de histórico em PostgreSQL e dashboard interativo para análise da evolução de preços.

## Tecnologias utilizadas
- Python 3.12+
- PostgreSQL
- Docker Compose
- SQLAlchemy
- Requests
- BeautifulSoup
- Pandas
- Streamlit
- python-dotenv

## Funcionalidades implementadas
- Cadastro de produtos monitorados
- Coleta manual de preço atual
- Coleta em lote de produtos ativos
- Persistência de histórico de preços
- Cálculo de desconto percentual
- Cálculo de variação absoluta entre coletas
- Cálculo de variação percentual entre coletas
- Verificação de preço-alvo atingido
- Script para listar produtos monitorados
- Script para coletar um único produto por ID
- Dashboard com métricas e histórico detalhado
- Seleção de produto monitorado no dashboard

## Estrutura do projeto
```text
monitor-precos-python/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   ├── scrapers/
│   │   ├── __init__.py
│   │   └── extrator_generico.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── coletor.py
│   └── dashboard/
│       ├── __init__.py
│       └── dashboard_app.py
├── scripts/
│   ├── cadastrar_produto.py
│   ├── criar_tabelas.py
│   ├── executar_coleta.py
│   ├── listar_produtos.py
│   └── coletar_produto_por_id.py
├── .env.example
├── .gitignore
├── compose.yaml
├── requirements.txt
└── README.md
```

## Como executar o projeto

### 1. Clonar o repositório
```bash
git clone https://github.com/SEU_USUARIO/monitor-precos-python.git
cd monitor-precos-python
```

### 2. Criar e ativar ambiente virtual
```bash
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Instalar dependências
```bash
pip install -r requirements.txt
```

### 4. Subir o PostgreSQL com Docker
```bash
docker compose up -d
```

### 5. Criar arquivo .env
Crie uma cópia de `.env.example` com os valores locais do projeto.

### 6. Criar as tabelas
```bash
python scripts/criar_tabelas.py
```

### 7. Cadastrar um produto monitorado
```bash
python scripts/cadastrar_produto.py
```

### 8. Listar produtos monitorados
```bash
python scripts/listar_produtos.py
```

### 9. Executar coleta em lote
```bash
python scripts/executar_coleta.py
```

### 10. Coletar um único produto por ID
```bash
python scripts/coletar_produto_por_id.py
```

### 11. Abrir o dashboard
```bash
streamlit run app/dashboard/dashboard_app.py
```

## Scripts disponiveis
| Script | Descricao | Comando |
| --- | --- | --- |
| Criar tabelas | Cria as tabelas no banco de dados | `python scripts/criar_tabelas.py` |
| Cadastrar produto | Cadastra um produto monitorado | `python scripts/cadastrar_produto.py` |
| Listar produtos | Lista os produtos monitorados | `python scripts/listar_produtos.py` |
| Coleta em lote | Coleta preco de todos os produtos ativos | `python scripts/executar_coleta.py` |
| Coleta por ID | Coleta um produto especifico por ID | `python scripts/coletar_produto_por_id.py` |

## Exemplo de produto para teste
O projeto foi validado com o site de demonstração:
- Books to Scrape

Exemplo de URL:
- https://books.toscrape.com/catalogue/house-of-leaves_169/index.html

Exemplo de seletores:
- Seletor do titulo: `.product_main h1`
- Seletor do preco atual: `.price_color`
- Seletor da disponibilidade: `.availability`

## Métricas exibidas no dashboard
- Preço atual
- Menor preço
- Maior preço
- Histórico detalhado de coletas (preço original, desconto percentual e disponibilidade)

## Limitações atuais
- O scraper depende de seletores CSS informados manualmente
- Alguns sites podem ter proteção anti-bot ou HTML instável
- O projeto foi pensado para páginas públicas e simples, especialmente em fase de portfólio

## Melhorias futuras
- Agendamento automático de coletas
- Alertas por e-mail ou Telegram
- Suporte a mais lojas com extratores específicos
- Dashboard com filtros adicionais
- Exportação de histórico em CSV