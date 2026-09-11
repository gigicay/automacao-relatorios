import pandas as pd
import unicodedata
import re

SINONIMOS = {
    "cliente": ["cliente", "nome_cliente", "nome do cliente", "nomecliente", "customer", "cliente_nome", "nome", "comprador"],
    "produto": ["produto", "produto_vendido", "produto vendido", "item", "item_vendido", "servico", "serviço", "descricao_produto", "descrição produto"],
    "quantidade": ["quantidade", "qtd", "qtde", "quant", "volume", "units", "unidades", "quantidade_vendida", "qtd_vendida"],
    "preco": ["preco", "preço", "valor", "valor_unitario", "valor unitario", "valor_unitário", "preco_unitario", "preço unitário", "preço_unitário"],
    "data": ["data", "data_venda", "data venda", "dt_venda", "dt venda", "date", "data_da_venda"],
    "categoria": ["categoria", "tipo", "segmento", "grupo", "classificacao", "classificação"],
}

OBRIGATORIAS = ["cliente", "produto", "quantidade", "preco", "data"]


def normalizar_nome(texto):
    texto = str(texto).strip().lower()
    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    texto = re.sub(r"[^a-z0-9]+", "_", texto)
    return texto.strip("_")


def encontrar_coluna(colunas, possibilidades):
    normalizadas = {normalizar_nome(c): c for c in colunas}
    for possibilidade in possibilidades:
        chave = normalizar_nome(possibilidade)
        if chave in normalizadas:
            return normalizadas[chave]
    return None


def ler_csv(arquivo):
    try:
        arquivo.seek(0)
        return pd.read_csv(
            arquivo,
            encoding="utf-8-sig",
            sep=None,
            engine="python",
        )
    except UnicodeDecodeError:
        try:
            arquivo.seek(0)
            return pd.read_csv(
                arquivo,
                encoding="latin-1",
                sep=None,
                engine="python",
            )
        except Exception as e:
            raise ValueError(f"ARQUIVO_INVALIDO|{e}")
    except (pd.errors.ParserError, UnicodeError, ValueError) as e:
        try:
            arquivo.seek(0)
            return pd.read_csv(
                arquivo,
                encoding="latin-1",
                sep=None,
                engine="python",
            )
        except Exception:
            raise ValueError(f"ARQUIVO_INVALIDO|{e}")


def converter_numero(serie):
    def converter(valor):
        if pd.isna(valor):
            return None

        texto = str(valor).strip()
        if not texto:
            return None

        texto = (
            texto.replace("R$", "")
            .replace("r$", "")
            .replace("$", "")
            .replace(" ", "")
            .replace("'", "")
        )

        # Aceita 1.234,56 e 1234.56.
        if "," in texto:
            texto = texto.replace(".", "").replace(",", ".")

        try:
            return float(texto)
        except ValueError:
            return None

    return serie.apply(converter)


def executar_etl(arquivo):
    df_original = ler_csv(arquivo)

    if df_original.empty:
        raise ValueError("ARQUIVO_INVALIDO|O CSV está vazio.")

    mapeamento = {}
    faltantes = []

    for padronizada, possibilidades in SINONIMOS.items():
        coluna = encontrar_coluna(df_original.columns, possibilidades)
        if coluna:
            mapeamento[coluna] = padronizada
        elif padronizada in OBRIGATORIAS:
            faltantes.append(padronizada)

    if faltantes:
        raise ValueError("COLUNAS_FALTANTES|" + ",".join(faltantes))

    df = df_original.rename(columns=mapeamento).copy()

    if "categoria" not in df.columns:
        df["categoria"] = "Não informado"

    df["data"] = pd.to_datetime(df["data"], errors="coerce", dayfirst=True)
    df["quantidade"] = converter_numero(df["quantidade"])
    df["preco"] = converter_numero(df["preco"])

    df["cliente"] = df["cliente"].fillna("").astype(str).str.strip()
    df["produto"] = df["produto"].fillna("").astype(str).str.strip()
    df["categoria"] = df["categoria"].fillna("Não informado").astype(str).str.strip()

    antes = len(df)

    df = df.dropna(subset=["data", "quantidade", "preco"])
    df = df[(df["quantidade"] >= 0) & (df["preco"] >= 0)]
    df = df[(df["cliente"] != "") & (df["produto"] != "")]

    descartadas = antes - len(df)

    if df.empty:
        raise ValueError("SEM_DADOS_VALIDOS|Nenhum registro válido permaneceu após o tratamento.")

    df["valor_total"] = df["quantidade"] * df["preco"]
    df["mes"] = df["data"].dt.strftime("%Y-%m")

    resultado = df.sort_values("data").reset_index(drop=True)
    resultado.attrs["linhas_descartadas"] = descartadas

    return resultado, mapeamento
