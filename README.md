# 📈 Monitor de Preços (Python)

![Python](https://img.shields.io/badge/python-3.13-blue.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4479A1?style=flat&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=flat&logo=docker&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=Streamlit&logoColor=white)

## 🎯 Objetivo
Este é um projeto de portfólio desenvolvido para monitoramento automatizado de preços em e-commerces. O sistema realiza o *scraping* de páginas públicas, armazena os dados em um banco de dados relacional e apresenta uma interface visual para análise de tendências de mercado.

## 🛠️ Tecnologias e Ferramentas
* **Linguagem:** Python 3.13
* **Banco de Dados:** PostgreSQL (via Docker)
* **ORM:** SQLAlchemy
* **Coleta de Dados:** Requests & BeautifulSoup4
* **Processamento de Dados:** Pandas
* **Interface Gráfica:** Streamlit
* **Ambiente:** Docker Compose & PyCharm

## 🚀 Funcionalidades Atuais
- [x] **Cadastro de Produtos:** Registro de URLs e metadados dos produtos a serem monitorados.
- [x] **Motor de Coleta:** Script automatizado para extração de preços atuais e descontos.
- [x] **Histórico de Preços:** Persistência robusta para rastrear variações ao longo do tempo.
- [x] **Dashboard Interativo:** Visualização de métricas (Menor/Maior preço) e gráficos de evolução.

## 💻 Como Executar o Projeto

### 1. Configurar o Banco de Dados
Certifique-se de que o Docker Desktop está rodando e execute:
```bash
docker compose up -d
```

### 2. Ativar o ambiente virtual:
```bash
.\.venv\Scripts\Activate.ps1
```

### 3. Instalar as dependências:
```bash
pip install -r requirements.txt
```

### 4. Criar as tabelas:
```bash
python scripts/criar_tabelas.py
```

### 5. Cadastrar um produto monitorado:
```bash
python scripts/cadastrar_produto.py
```

### 6. Executar a coleta:
```bash
python scripts/executar_coleta.py
```

### 7. Abrir o dashboard:
```bash
streamlit run app/dashboard/app.py
```