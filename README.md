# Automação de Relatórios

Sistema desenvolvido em Python para importação, tratamento e análise de dados de vendas, com geração de dashboard interativo e exportação de relatórios em Excel.

## Dashboard online

Acesse o projeto:

https://automacao-relatorios.streamlit.app/

## Funcionalidades

- Upload de arquivos CSV pelo dashboard
- Reconhecimento automático de diferentes nomes de colunas
- Padronização e tratamento dos dados
- Validação de registros e arquivos
- Dashboard interativo com indicadores e gráficos
- Análise de faturamento, vendas, clientes e ticket médio
- Exportação dos dados tratados e análises para Excel
- Arquivo CSV de exemplo para testes
- Mensagens amigáveis para erros de preenchimento ou formato

## Tecnologias utilizadas

- Python
- Pandas
- Streamlit
- Plotly
- OpenPyXL

## Fluxo do projeto

```text
CSV
 ↓
Leitura dos dados
 ↓
ETL e padronização
 ↓
Validação e tratamento
 ↓
Análise dos dados
 ↓
Dashboard
 ↓
Exportação para Excel
```

## Arquivos principais

```text
automacao-relatorios/
│
├── app.py                  # Interface e dashboard
├── etl.py                  # Leitura, padronização e tratamento dos dados
├── relatorio_excel.py      # Geração do relatório em Excel
├── requirements.txt        # Dependências do projeto
├── README.md               # Documentação
├── .gitignore              # Arquivos ignorados pelo Git
│
└── dados/
    └── clientes_teste.csv  # Arquivo fictício para testes
```

## Arquivos CSV aceitos

O sistema aceita arquivos CSV criados pelo usuário, desde que contenham as informações obrigatórias de:

- Cliente
- Produto
- Quantidade
- Preço ou valor unitário
- Data

Os nomes das colunas não precisam ser exatamente iguais. O sistema reconhece diferentes variações de nomes e realiza a padronização automaticamente.

A categoria é opcional.

### Exemplo

```text
data,nome_cliente,produto_vendido,categoria,qtd,preco
05/01/2026,Cliente 001,Consignado,Crédito,2,1200
12/01/2026,Cliente 002,Consórcio,Investimentos,1,2500
18/02/2026,Cliente 004,Seguro,Seguros,2,800
```

Os dados utilizados no arquivo de exemplo são fictícios.

## Tratamento de erros

O sistema realiza validações antes de processar os dados.

Entre os casos tratados estão:

- Arquivo CSV vazio
- Colunas obrigatórias ausentes
- Arquivo inválido ou incompatível
- Dados com formato incorreto
- Registros sem informações essenciais
- Registros com data, quantidade ou preço inválidos
- Valores negativos

Quando um problema é encontrado, o dashboard apresenta uma mensagem explicando o que precisa ser corrigido.

## Como executar localmente

Clone o repositório e instale as dependências:

```bash
python -m venv .venv
```

No Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Execute o dashboard:

```bash
streamlit run app.py
```

Depois, abra o endereço fornecido pelo Streamlit no navegador.

## Objetivo do projeto

O projeto foi desenvolvido para praticar conceitos de:

- Python
- ETL
- Manipulação e tratamento de dados
- Análise de dados
- Visualização de informações
- Desenvolvimento de dashboards
- Automação de relatórios
- Exportação de dados para Excel

## Status

Projeto funcional e disponível online para testes.
