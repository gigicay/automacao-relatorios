# 📊 Automação de Relatórios

Projeto em Python para importar CSV, reconhecer diferentes nomes de colunas, realizar ETL, criar dashboard e exportar Excel.

## Funcionalidades
- Upload de CSV pelo dashboard
- Reconhecimento de diferentes títulos de colunas
- Padronização e tratamento dos dados
- Dashboard com Streamlit e Plotly
- Exportação para Excel
- Dados fictícios para teste

## Executar
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

Depois escolha um CSV no dashboard.


## Arquivos CSV aceitos

O sistema aceita arquivos CSV criados pelo usuário, desde que contenham as informações obrigatórias de **cliente, produto, quantidade, preço/valor unitário e data**. Os títulos podem variar, pois o sistema reconhece diferentes nomes equivalentes e também tenta identificar automaticamente separadores comuns como vírgula e ponto e vírgula.

Se houver um problema, o dashboard mostra uma mensagem explicando o que precisa ser corrigido, em vez de exibir apenas um erro técnico.
