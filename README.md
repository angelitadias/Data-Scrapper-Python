
# DATA SCRAPPER EM PYTHON

# 📊 Data Scraper - MC Sonae

**Objetivo:** Automatizar a coleta de informações sobre projetos internos da empresa **MC Sonae**, centralizando dados dispersos para melhorar a comunicação, transparência e acompanhamento entre equipes.

---

## 🚀 Visão Geral

Este projeto é um **Data Scraper desenvolvido em Python** que coleta dados de diferentes fontes internas (ex: intranet, planilhas online, sistemas de gestão de projetos) com o objetivo de:

- Identificar todos os projetos em andamento;
- Unificar informações de status, responsáveis, prazos e entregas;
- Facilitar o acesso centralizado por times e gestores;
- Mitigar a falha de comunicação recorrente na organização.

---

## 🛠️ Tecnologias Utilizadas

- `Python 3.x`
- `BeautifulSoup` / `Selenium` — para raspagem de dados web
- `Pandas` — para tratamento e organização dos dados
- `Google Sheets API` — integração com fontes de dados
- `CSV` — armazenamento temporário/local
---

## 📥 Fontes de Dados

- Planilhas compartilhadas entre equipes
- Diretórios comuns com arquivos Excel ou PDFs

---

## 🔁 Funcionamento

1. **Extração:** o scraper acessa as fontes pré-configuradas e coleta os dados relevantes (títulos de projetos, responsáveis, status, prazos).
2. **Transformação:** os dados são limpos, organizados e convertidos para um formato padronizado.
3. **Carga (opcional):** os dados podem ser exportados para:
   - Um banco de dados interno
   - Uma dashboard visual (ex: Power BI, Google Data Studio)
   - Uma planilha unificada para consulta geral



