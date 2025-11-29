
# DATA SCRAPPER EM PYTHON

# 📊 Data Scraper - MC Sonae

**Objetivo:** Automatizar a coleta de informações sobre projetos internos da empresa **MC Sonae**, centralizando dados dispersos para melhorar a comunicação, transparência e acompanhamento entre equipes.

---

## 🚀 Visão Geral

Este projeto é um **Data Scraper desenvolvido em Python** que coleta dados de diferentes fontes internas com o objetivo de:

- Identificar todos os projetos em andamento;
- Unificar informações de status, responsáveis, prazos e entregas;
- Facilitar o acesso centralizado por times e gestores;
- Mitigar a falha de comunicação recorrente na organização.

---

## 🛠️ Tecnologias Utilizadas

- `Python 3.x` - Linguagem base para automação e análise de dados
- `Pandas` - para tratamento e organização dos dados
- `Google Sheets API` - integração com fontes de dados e manipulação de dados em planilhas Google
- `CSV` - armazenamento e leitura de dados em formato simples de texto
- `python-docx` - Manipulação de documentos Word (.docx)
- `pdfplumber` - xtração de texto e tabelas de arquivos PDF
- `openpyxl` - Manipulação de arquivos Excel (.xlsx)
- `tabulate` - Exibição de dados tabulares no terminal
- `tqdm` - Exibição de barra de progresso em loops
- `streamlit` - Criação de interfaces web interativas para visualização de dados
---

## 📥 Fontes de Dados

- Planilhas compartilhadas entre equipes
- Diretórios comuns com arquivos Excel ou PDFs
- Dados sinteticos
---

## 🔁 Funcionamento

1. **Extração:** o scraper acessa as fontes pré-configuradas e coleta os dados relevantes (títulos de projetos, tabelas, status, prazos).
2. **Transformação:** os dados são limpos, organizados e convertidos para um formato padronizado(.csv).
3. **Carga (opcional):** os dados podem ser exportados para:
   - Um banco de dados interno
   - Uma dashboard visual (ex: Stremlit)
   - Uma planilha unificada para consulta geral
