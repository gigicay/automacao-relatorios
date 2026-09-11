from pathlib import Path
import streamlit as st
import pandas as pd
import plotly.express as px
from etl import executar_etl
from relatorio_excel import gerar_excel

st.set_page_config(
    page_title="Relatório de Vendas",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Visual ----------
st.markdown("""
<style>
.stApp {
    background: #101827;
    color: #E8EEF8;
}
[data-testid="stHeader"] {
    background: #101827;
}
[data-testid="stSidebar"] {
    background: #0B1220;
    border-right: 1px solid #24334B;
}
[data-testid="stSidebar"] * {
    color: #DCE6F5;
}
.block-container {
    padding-top: 2.2rem;
    padding-bottom: 2.5rem;
    max-width: 1450px;
}
h1, h2, h3 {
    color: #F4F7FC !important;
}
.main-title {
    font-size: 2.05rem;
    font-weight: 750;
    margin-bottom: .15rem;
}
.subtitle {
    color: #9FB0C9;
    font-size: 1rem;
    margin-bottom: 1.35rem;
}
.section-title {
    font-size: 1.12rem;
    font-weight: 650;
    color: #F0F4FA;
    margin: 1.35rem 0 .65rem;
}
.kpi {
    background: #17243A;
    border: 1px solid #2B4161;
    border-radius: 12px;
    padding: 1rem 1.1rem;
    min-height: 112px;
    box-shadow: 0 4px 14px rgba(0,0,0,.16);
}
.kpi-label {
    color: #9FB0C9;
    font-size: .84rem;
    margin-bottom: .45rem;
}
.kpi-value {
    color: #F4F7FC;
    font-size: 1.5rem;
    font-weight: 720;
}
.info-box {
    background: #162238;
    border: 1px solid #2B4161;
    border-radius: 12px;
    padding: 1rem 1.15rem;
    color: #C5D1E3;
    margin-bottom: 1rem;
}
.step-box {
    background: #17243A;
    border: 1px solid #2B4161;
    border-radius: 10px;
    padding: .85rem 1rem;
    margin: .45rem 0;
}
.step-number {
    color: #76A7FF;
    font-weight: 750;
}
.small-note {
    color: #8FA2BC;
    font-size: .78rem;
}
div[data-testid="stFileUploader"] {
    background: #121D2F;
    border: 1px dashed #47668F;
    border-radius: 10px;
    padding: .45rem;
}
.stButton > button, .stDownloadButton > button {
    border-radius: 8px;
    font-weight: 600;
}
[data-testid="stDataFrame"] {
    border: 1px solid #2B4161;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">Dashboard de Vendas</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Visualize os principais indicadores e o desempenho do seu negócio.</div>',
    unsafe_allow_html=True,
)

# ---------- Sidebar / upload ----------
with st.sidebar:
    st.markdown("## Relatório de Vendas")
    st.caption("Análise · Tratamento · Insights")
    st.divider()

    st.markdown("### Envie o arquivo de vendas")
    st.markdown(
        '<div class="small-note">1. Prepare seu CSV com os dados de vendas.<br>'
        '2. Clique em Upload e selecione o arquivo.<br>'
        '3. O sistema identifica os nomes das colunas e trata os dados.</div>',
        unsafe_allow_html=True,
    )

    uploaded_file = st.file_uploader(
        "Arquivo CSV",
        type=["csv"],
        label_visibility="collapsed",
        help="O sistema aceita nomes de colunas equivalentes, como cliente/nome_cliente, quantidade/qtd e preco/valor.",
    )

    st.markdown("**Exemplos de colunas reconhecidas**")
    st.caption("cliente · nome_cliente · nome")
    st.caption("produto · produto_vendido · item")
    st.caption("quantidade · qtd · qtde")
    st.caption("preco · preço · valor · valor_unitario")
    st.caption("data · data_venda · dt_venda")
    st.caption("categoria · tipo · segmento (opcional)")

    exemplo = Path("dados/clientes_teste.csv")
    if exemplo.exists():
        with open(exemplo, "rb") as f:
            st.download_button(
                "Baixar arquivo de exemplo",
                f,
                file_name="clientes_teste.csv",
                mime="text/csv",
                use_container_width=True,
            )

if uploaded_file is None:
    st.markdown(
        '<div class="info-box"><strong>Como começar</strong><br>'
        'Use a área <strong>“Envie o arquivo de vendas”</strong> na lateral esquerda. '
        'Selecione um arquivo CSV e, assim que ele for carregado, o dashboard será preenchido automaticamente.</div>',
        unsafe_allow_html=True,
    )

    a, b, c = st.columns(3)
    with a:
        st.markdown('<div class="step-box"><span class="step-number">01</span><br><strong>Envie o CSV</strong><br><span class="small-note">Selecione o arquivo de vendas.</span></div>', unsafe_allow_html=True)
    with b:
        st.markdown('<div class="step-box"><span class="step-number">02</span><br><strong>Tratamento automático</strong><br><span class="small-note">Colunas e valores são padronizados.</span></div>', unsafe_allow_html=True)
    with c:
        st.markdown('<div class="step-box"><span class="step-number">03</span><br><strong>Analise e exporte</strong><br><span class="small-note">Veja os indicadores e gere o Excel.</span></div>', unsafe_allow_html=True)
    st.stop()

# ---------- ETL ----------
try:
    df, mapeamento = executar_etl(uploaded_file)
except ValueError as e:
    mensagem = str(e)

    if mensagem.startswith("COLUNAS_FALTANTES|"):
        faltantes = mensagem.split("|", 1)[1].split(",")
        nomes = {
            "cliente": "Cliente",
            "produto": "Produto",
            "quantidade": "Quantidade",
            "preco": "Preço ou valor unitário",
            "data": "Data",
        }
        lista = "".join(f"<li>{nomes.get(item, item)}</li>" for item in faltantes)
        st.error("O arquivo foi lido, mas faltam informações obrigatórias.")
        st.markdown(
            f"**Não consegui identificar:**<ul>{lista}</ul>",
            unsafe_allow_html=True,
        )
        st.info(
            "Confira os títulos das colunas. Exemplos aceitos: "
            "cliente/nome_cliente, produto/item, quantidade/qtd, "
            "preco/valor e data/data_venda."
        )
    elif mensagem.startswith("ARQUIVO_INVALIDO|"):
        st.error("Não consegui ler este arquivo como um CSV válido.")
        st.info(
            "Salve o arquivo no formato CSV e confira se a primeira linha "
            "contém os nomes das colunas."
        )
    elif mensagem.startswith("SEM_DADOS_VALIDOS|"):
        st.error("O arquivo foi lido, mas não encontrei registros válidos.")
        st.info(
            "Confira principalmente data, quantidade e preço. Esses campos "
            "precisam conter valores válidos."
        )
    else:
        st.error(f"Não foi possível processar o arquivo: {mensagem}")
    st.stop()
except Exception:
    st.error("Ocorreu um problema inesperado ao processar o arquivo.")
    st.info("Confira o formato do CSV e tente novamente.")
    st.stop()

if df.empty:
    st.warning("O arquivo foi lido, mas não existem registros válidos após o tratamento.")
    st.stop()

linhas_descartadas = df.attrs.get("linhas_descartadas", 0)
if linhas_descartadas:
    st.warning(
        f"{linhas_descartadas} linha(s) foram ignoradas porque tinham "
        "data, quantidade ou preço inválidos."
    )

with st.expander("Ver como o sistema reconheceu as colunas"):
    st.write(mapeamento)

# ---------- KPIs ----------
st.markdown('<div class="section-title">Resumo</div>', unsafe_allow_html=True)

total_vendas = len(df)
faturamento = float(df["valor_total"].sum())
ticket_medio = faturamento / total_vendas if total_vendas else 0
clientes = int(df["cliente"].nunique())

def brl(value):
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

k1, k2, k3, k4 = st.columns(4)
for col, label, value in [
    (k1, "Faturamento total", brl(faturamento)),
    (k2, "Total de vendas", f"{total_vendas:,}".replace(",", ".")),
    (k3, "Clientes atendidos", f"{clientes:,}".replace(",", ".")),
    (k4, "Ticket médio", brl(ticket_medio)),
]:
    with col:
        st.markdown(
            f'<div class="kpi"><div class="kpi-label">{label}</div>'
            f'<div class="kpi-value">{value}</div></div>',
            unsafe_allow_html=True,
        )

# ---------- Charts ----------
st.markdown('<div class="section-title">Análise de desempenho</div>', unsafe_allow_html=True)
left, right = st.columns(2)

with left:
    vendas_produto = (
        df.groupby("produto", as_index=False)["valor_total"]
        .sum()
        .sort_values("valor_total", ascending=False)
    )
    fig = px.bar(
        vendas_produto.head(10),
        x="produto", y="valor_total",
        title="Faturamento por produto",
        labels={"produto": "Produto", "valor_total": "Faturamento"},
    )
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#17243A",
        plot_bgcolor="#17243A",
        font_color="#DCE6F5",
        margin=dict(l=20, r=20, t=55, b=20),
        showlegend=False,
    )
    st.plotly_chart(fig, use_container_width=True)

with right:
    df_mes = df.groupby("mes", as_index=False)["valor_total"].sum().sort_values("mes")
    fig = px.line(
        df_mes, x="mes", y="valor_total", markers=True,
        title="Evolução do faturamento",
        labels={"mes": "Mês", "valor_total": "Faturamento"},
    )
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#17243A",
        plot_bgcolor="#17243A",
        font_color="#DCE6F5",
        margin=dict(l=20, r=20, t=55, b=20),
    )
    st.plotly_chart(fig, use_container_width=True)

cat = df.groupby("categoria", as_index=False)["valor_total"].sum().sort_values("valor_total", ascending=False)
fig = px.bar(
    cat, x="categoria", y="valor_total",
    title="Faturamento por categoria",
    labels={"categoria": "Categoria", "valor_total": "Faturamento"},
)
fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="#17243A",
    plot_bgcolor="#17243A",
    font_color="#DCE6F5",
    margin=dict(l=20, r=20, t=55, b=20),
    showlegend=False,
)
st.plotly_chart(fig, use_container_width=True)

# ---------- Data ----------
st.markdown('<div class="section-title">Dados tratados</div>', unsafe_allow_html=True)
display_df = df.copy()
if "data" in display_df:
    display_df["data"] = pd.to_datetime(display_df["data"]).dt.strftime("%d/%m/%Y")
if "preco" in display_df:
    display_df["preco"] = display_df["preco"].map(brl)
if "valor_total" in display_df:
    display_df["valor_total"] = display_df["valor_total"].map(brl)

st.dataframe(display_df, use_container_width=True, hide_index=True)

# ---------- Export ----------
st.markdown('<div class="section-title">Exportação</div>', unsafe_allow_html=True)
st.caption("O Excel reúne um resumo executivo, análise por produto/categoria e os dados tratados.")

excel_bytes = gerar_excel(df)
st.download_button(
    "Exportar relatório para Excel",
    data=excel_bytes,
    file_name="relatorio_vendas.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    use_container_width=False,
)
