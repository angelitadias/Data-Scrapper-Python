import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard Financeiro 2020–2024", layout="wide")
@st.cache_data
def load_data():
    df = pd.read_csv("dados_empresa_2020_2024.csv", parse_dates=["Date"])
    df["Year"] = df["Date"].dt.year
    return df

df = load_data()


#Titulo
st.title("Dashboard Financeiro — 2020 a 2024")
st.markdown("Análise consolidada de desempenho: Receita, EBITDA, CAPEX, Lojas e Capital Humano")


#KPIs PRINCIPAIS
latest = df[df["Year"] == 2024].iloc[-1]

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Faturação Total (M€)", f"{latest['Turnover_Total_M€']:.2f}")
col2.metric("EBITDA (M€)", f"{latest['EBITDA_Total_M€']:.2f}")
col3.metric("Margem EBITDA (%)", f"{latest['EBITDA_Margin_pct']:.1f}")
col4.metric("Lojas Totais", f"{int(latest['Num_Lojas_Totais']):,}".replace(",", "."))
col5.metric("Colaboradores", f"{int(latest['Num_Colaboradores']):,}".replace(",", "."))


#G1 — Evolução da Faturação Total
fig_turnover = px.line(
    df.groupby("Year")["Turnover_Total_M€"].mean().reset_index(),
    x="Year",
    y="Turnover_Total_M€",
    markers=True,
    title="Evolução da Faturação Total (M€)"
)
st.plotly_chart(fig_turnover, use_container_width=True)


#G2 — Receita por Segmento
receita_seg = df.groupby("Year")[["Receita_Alimentar_M€", "Receita_HWB_M€", "Receita_Internacional_M€"]].mean().reset_index()
fig_segmentos = px.bar(
    receita_seg,
    x="Year",
    y=["Receita_Alimentar_M€", "Receita_HWB_M€", "Receita_Internacional_M€"],
    barmode="group",
    title="Receita por Segmento (M€)"
)
st.plotly_chart(fig_segmentos, use_container_width=True)


#G3 — Margem EBITDA (%)
fig_margin = px.line(
    df.groupby("Year")["EBITDA_Margin_pct"].mean().reset_index(),
    x="Year",
    y="EBITDA_Margin_pct",
    markers=True,
    title="Margem EBITDA (%)"
)
st.plotly_chart(fig_margin, use_container_width=True)


#G4 — Lojas e Colaboradores
col6, col7 = st.columns(2)

with col6:
    lojas = df.groupby("Year")["Num_Lojas_Totais"].max().reset_index()
    fig_lojas = px.bar(lojas, x="Year", y="Num_Lojas_Totais", title="Total de Lojas (por ano)")
    st.plotly_chart(fig_lojas, use_container_width=True)

with col7:
    colabs = df.groupby("Year")["Num_Colaboradores"].max().reset_index()
    fig_colabs = px.line(colabs, x="Year", y="Num_Colaboradores", markers=True, title="Evolução de Colaboradores")
    st.plotly_chart(fig_colabs, use_container_width=True)


#RODAPÉ
st.markdown("---")
st.caption("Fonte: Dados simulados (2020–2024) — para uso demonstrativo em dashboards Streamlit.")
