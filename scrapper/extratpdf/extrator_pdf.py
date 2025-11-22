import pdfplumber
import pandas as pd
import os
from datetime import datetime

def extrair_texto_e_tabelas(pdf_path):
    """Extrai texto e todas as tabelas de um PDF."""
    texto_total = ""
    tabelas_dfs = []

    with pdfplumber.open(pdf_path) as pdf:
        for pagina in pdf.pages:
            texto_pagina = pagina.extract_text()
            if texto_pagina:
                texto_total += texto_pagina + "\n"

            tabelas = pagina.extract_tables()
            for tabela in tabelas:
                try:
                    df_temp = pd.DataFrame(tabela[1:], columns=tabela[0])
                    tabelas_dfs.append(df_temp)
                except Exception:
                    pass

    return texto_total.strip(), tabelas_dfs


def calcular_estatisticas(df):
    """Retorna estatísticas descritivas completas (numéricas e categóricas)."""
    try:
        estat = df.describe(include='all').transpose()
        estat["coef_var"] = df.select_dtypes(include='number').std() / df.select_dtypes(include='number').mean()
        return estat
    except Exception:
        return pd.DataFrame()


def processar_pdfs(pasta="."):
    """Processa todos os PDFs da pasta e salva resultados em CSV."""
    resultados_texto = []
    resultados_tabelas = []

    arquivos_pdf = [f for f in os.listdir(pasta) if f.lower().endswith(".pdf")]
    if not arquivos_pdf:
        print("Nenhum arquivo PDF encontrado na pasta.")
        return

    for pdf in arquivos_pdf:
        caminho_pdf = os.path.join(pasta, pdf)
        print(f"\n🔍 Processando: {pdf}")

        texto, tabelas = extrair_texto_e_tabelas(caminho_pdf)
        data_extracao = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Salva texto
        resultados_texto.append({
            "Arquivo": pdf,
            "DataExtracao": data_extracao,
            "Texto": texto if texto else "Nenhum texto encontrado."
        })

        # Processa tabelas e estatísticas
        for i, tabela in enumerate(tabelas):
            tabela["Arquivo"] = pdf
            tabela["Pagina/Tabela"] = f"tabela_{i+1}"

            estat = calcular_estatisticas(tabela)
            if not estat.empty:
                estat["Arquivo"] = pdf
                estat["Pagina/Tabela"] = f"tabela_{i+1}"
                resultados_tabelas.append(estat)

    # Cria DataFrames consolidados
    texto_df = pd.DataFrame(resultados_texto)
    tabelas_df = pd.concat(resultados_tabelas, ignore_index=True) if resultados_tabelas else pd.DataFrame()

    # Salva CSVs finais
    texto_df.to_csv("resultado_textos.csv", index=False, encoding="utf-8-sig")
    print("\nTexto extraído salvo em: resultado_textos.csv")

    if not tabelas_df.empty:
        tabelas_df.to_csv("resultado_tabelas_estatisticas.csv", index=False, encoding="utf-8-sig")
        print("Tabelas e estatísticas salvas em: resultado_tabelas_estatisticas.csv")
    else:
        print("Nenhuma tabela com dados numéricos encontrada para análise.")


if __name__ == "__main__":
    processar_pdfs(".")

