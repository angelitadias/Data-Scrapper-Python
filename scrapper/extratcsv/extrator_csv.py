import pandas as pd
import glob
import os

arquivos_csv = glob.glob("*.csv")

if not arquivos_csv:
    print("Nenhum arquivo .csv encontrado no diretório atual.")
else:
    for arquivo in arquivos_csv:
        print(f"\nLendo arquivo: {arquivo}")

        try:
            df = pd.read_csv(arquivo, encoding="utf-8", low_memory=False)

            # Compatível com versões antigas do pandas
            estatisticas = df.describe(include='all').transpose()

            # Adiciona Coeficiente de Variação (CV) para variáveis numéricas
            for col in df.select_dtypes(include='number').columns:
                mean = estatisticas.loc[col, 'mean'] if 'mean' in estatisticas.columns else None
                std = estatisticas.loc[col, 'std'] if 'std' in estatisticas.columns else None
                if mean and mean != 0:
                    estatisticas.loc[col, 'CV'] = std / mean
                else:
                    estatisticas.loc[col, 'CV'] = None

            textos_resumo = []
            for col in estatisticas.index:
                tipo = df[col].dtype
                resumo = f"Coluna '{col}' ({tipo}): "
                if pd.api.types.is_numeric_dtype(df[col]):
                    resumo += f"média={estatisticas.loc[col, 'mean']:.2f}, desvio padrão={estatisticas.loc[col, 'std']:.2f}, CV={estatisticas.loc[col, 'CV']:.2f}"
                else:
                    resumo += f"únicos={estatisticas.loc[col, 'unique']}, valor mais frequente='{estatisticas.loc[col, 'top']}', frequência={estatisticas.loc[col, 'freq']}"
                textos_resumo.append(resumo)

            texto_df = pd.DataFrame({'Resumo': textos_resumo})

            nome_saida = f"estatisticas_{os.path.splitext(arquivo)[0]}.csv"
            with open(nome_saida, "w", encoding="utf-8-sig") as f:
                f.write("# Estatísticas Descritivas\n")
            estatisticas.to_csv(nome_saida, mode="a", encoding="utf-8-sig")
            with open(nome_saida, "a", encoding="utf-8-sig") as f:
                f.write("\n# Resumo textual das variáveis\n")
            texto_df.to_csv(nome_saida, mode="a", index=False, encoding="utf-8-sig")

            print(f"Estatísticas e resumo salvos em '{nome_saida}'")

        except Exception as e:
            print(f"Erro ao processar '{arquivo}': {e}")




