import pandas as pd
import os
from tabulate import tabulate

def processar_excel(caminho_arquivo):
    try:
        xls = pd.ExcelFile(caminho_arquivo)
        print(f"\nLendo arquivo: {caminho_arquivo}")
        print("   Abas encontradas:", xls.sheet_names)

        dados_completos = []

        for aba in xls.sheet_names:
            print(f"\nLendo aba: {aba}")
            df = pd.read_excel(caminho_arquivo, sheet_name=aba)

            # Mostra primeiras linhas (apenas para visualização)
            print(tabulate(df.head(5), headers="keys", tablefmt="grid"))

            # Estatísticas descritivas gerais
            estatisticas = df.describe(include="all").transpose()
            
            # Coeficiente de variação para colunas numéricas
            for col in df.select_dtypes(include="number").columns:
                media = df[col].mean()
                desvio = df[col].std()
                estatisticas.loc[col, "coef_var"] = desvio / media if media != 0 else None

            # Inclui o nome do arquivo e da aba
            estatisticas["arquivo"] = os.path.basename(caminho_arquivo)
            estatisticas["aba"] = aba

            dados_completos.append(estatisticas)

        # Concatena todas as abas em um único DataFrame
        consolidado = pd.concat(dados_completos, axis=0)
        return consolidado

    except Exception as e:
        print(f"Erro ao processar '{caminho_arquivo}': {e}")
        return None


def extrair_de_todos_excel(pasta="."):
    """
    Lê todos os arquivos .xlsx na pasta especificada e gera um CSV consolidado.
    """
    arquivos = [f for f in os.listdir(pasta) if f.lower().endswith(".xlsx")]
    
    if not arquivos:
        print("Nenhum arquivo .xlsx encontrado na pasta.")
        return

    todos_dados = []

    for arquivo in arquivos:
        caminho = os.path.join(pasta, arquivo)
        resultado = processar_excel(caminho)
        if resultado is not None:
            todos_dados.append(resultado)

    if todos_dados:
        final = pd.concat(todos_dados, axis=0)
        nome_saida = "dados_processados_consolidados.csv"
        final.to_csv(nome_saida, index=True, encoding="utf-8-sig")
        print(f"\n Arquivo CSV final salvo como: {nome_saida}")
        print(tabulate(final.head(10), headers="keys", tablefmt="grid"))
    else:
        print("Nenhum dado foi processado.")


if __name__ == "__main__":
    # Executa o processamento de todos os arquivos Excel na pasta atual
    extrair_de_todos_excel(".")
