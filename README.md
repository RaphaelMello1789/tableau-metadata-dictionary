# Tableau Metadata Dictionary

Este projeto tem como objetivo **extrair e documentar metadados de campos calculados** a partir de arquivos **Tableau (.twb / .twbx)**, gerando um **dicionário de dados em CSV** que pode ser usado para governança, documentação, auditoria ou análises técnicas.

A ideia central é facilitar a leitura, padronização e reutilização de campos calculados criados em dashboards Tableau.

---

## 🎯 Objetivo do Projeto

- Ler arquivos Tableau `.twb` ou `.twbx`
- Extrair campos calculados definidos no workbook
- Filtrar campos por **prefixos padronizados**
- Gerar um **CSV estruturado** com os metadados dos campos

Este projeto pode ser usado como:
- Apoio à **governança de dados**
- Documentação técnica de dashboards
- Base para análises de padronização de KPIs
- Ferramenta auxiliar para times de BI / Analytics Engineering

---

## 🛠️ Pré-requisitos

- Python **3.9+**
- Ambiente virtual (recomendado)
- Bibliotecas Python:
  - `pandas`

---
## 🛠️ Padrão de desenvolvimento adotado

("kpi_", "hp_", "prmt_", "filter_", "dt_", "aux_", "fmt_", "var_")
