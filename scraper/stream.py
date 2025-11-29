import streamlit as st
import pandas as pd
import glob
import os

st.set_page_config(layout="wide")
DATA_DIR = "data"

def converter_data(col):
    try:
        return pd.to_datetime(col, errors="coerce", utc=False)
    except:
        return col

#Ler os arquvios
def ler_arquivo(arquivo):
    try:
        if arquivo.endswith(".csv"):
            return pd.read_csv(arquivo, engine="pyarrow")
        elif arquivo.endswith(".xlsx"):
            return pd.read_excel(arquivo)
    except Exception as e:
        st.error(f"Erro ao ler {arquivo}: {e}")
        return pd.DataFrame()

#carregar todos os dados
@st.cache_data(show_spinner=True)
def carregar_dados():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        return pd.DataFrame()

    arquivos = glob.glob(os.path.join(DATA_DIR, "*.csv")) + \
               glob.glob(os.path.join(DATA_DIR, "*.xlsx"))

    if not arquivos:
        return pd.DataFrame()

    lista_df = []
    
    for arq in arquivos:
        df = ler_arquivo(arq)
        if df.empty:
            continue

        df["source_file"] = os.path.basename(arq)

        #Converte coluna Date
        if "Date" in df.columns:
            df["Date"] = converter_data(df["Date"])

        #Cria colunas Year e Month se não existirem
        if "Date" in df.columns:
            df["Year"] = df["Date"].dt.year
            df["Month"] = df["Date"].dt.month

        lista_df.append(df)

    if not lista_df:
        return pd.DataFrame()

    df_final = pd.concat(lista_df, ignore_index=True)

    #Remove registros sem data
    if "Date" in df_final.columns:
        df_final = df_final.dropna(subset=["Date"])

    return df_final

#carregar os dados
df = carregar_dados()

st.sidebar.header("Filtros Interativos")

if df.empty:
    st.warning("Nenhum dado encontrado na pasta 'data'.")
    st.stop()

#Filtro: seleção de Arquivos
st.sidebar.subheader("Seleção de Arquivos")
arquivos = sorted(df["source_file"].unique())
arquivos_sel = st.sidebar.multiselect("Selecione os arquivos:", arquivos, default=arquivos)

df = df[df["source_file"].isin(arquivos_sel)]

#Filtro: datas
if "Date" not in df.columns:
    st.error("Nenhuma coluna 'Date' encontrada nos arquivos!")
    st.stop()

st.sidebar.subheader("Período")
data_min = df["Date"].min().date()
data_max = df["Date"].max().date()

data_inicio = st.sidebar.date_input("Data inicial", data_min)
data_fim = st.sidebar.date_input("Data final", data_max)

df = df[(df["Date"].dt.date >= data_inicio) & (df["Date"].dt.date <= data_fim)]

#Filtro: Ano e Mês
if "Year" in df.columns:
    anos = sorted(df["Year"].dropna().unique())
    anos_sel = st.sidebar.multiselect("Ano:", anos, default=anos)
    df = df[df["Year"].isin(anos_sel)]

if "Month" in df.columns:
    meses = sorted(df["Month"].dropna().unique())
    meses_sel = st.sidebar.multiselect("Mês:", meses, default=meses)
    df = df[df["Month"].isin(meses_sel)]

st.title(" Dashboard de Progresso e KPIs")

if df.empty:
    st.warning("Nenhum dado encontrado para os filtros aplicados.")
    st.stop()

st.header("Visão Geral do Período")

#Campos possíveis
campo_turnover = "Turnover_Total_M€"
campo_ebitda = "EBITDA_Total_M€"
campo_lucro = "Lucro_Liquido_M€"

faturamento = df[campo_turnover].sum() if campo_turnover in df else 0
ebitda = df[campo_ebitda].sum() if campo_ebitda in df else 0
lucro = df[campo_lucro].sum() if campo_lucro in df else 0

ultimo = df.sort_values("Date").iloc[-1]
num_lojas = ultimo.get("Num_Lojas_Totais", "N/A")
num_colab = ultimo.get("Num_Colaboradores", "N/A")

col1, col2, col3 = st.columns(3)
col1.metric("Faturamento Total", f"€ {faturamento:,.2f} M")
col2.metric("EBITDA Total", f"€ {ebitda:,.2f} M")
col3.metric("Lucro Líquido Total", f"€ {lucro:,.2f} M")

col4, col5 = st.columns(2)
col4.metric("Número de Lojas", num_lojas)
col5.metric("Número de Colaboradores", num_colab)

#GRÁFICOS
st.header("Visualizações")

if campo_turnover in df:
    st.subheader("Faturamento ao longo do tempo")
    st.line_chart(df.set_index("Date")[campo_turnover])

if {"Receita_Alimentar_M€", "Receita_HWB_M€", "Receita_Internacional_M€"}.issubset(df.columns):
    st.subheader("Comparativo de Receitas por Ano")
    tmp = df.groupby("Year")[["Receita_Alimentar_M€", "Receita_HWB_M€", "Receita_Internacional_M€"]].sum()
    st.bar_chart(tmp)

if {"EBITDA_Total_M€", "Lucro_Liquido_M€"}.issubset(df.columns):
    st.subheader("EBITDA x Lucro Líquido")
    st.line_chart(df.set_index("Date")[["EBITDA_Total_M€", "Lucro_Liquido_M€"]])

#gráfico de dispersão
if campo_turnover in df and campo_ebitda in df:
    st.subheader(f"Dispersão entre {campo_turnover} e {campo_ebitda}")
    df_clean = df.dropna(subset=[campo_turnover, campo_ebitda])  #remover valores nulos
    st.scatter_chart(df_clean[[campo_turnover, campo_ebitda]])

st.header("Dados Detalhados")
st.dataframe(df)
