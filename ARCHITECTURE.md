# Arquitetura do Sistema de Análise de Gamma no GitHub

Este documento descreve a arquitetura para um sistema automatizado que coleta, processa e apresenta diariamente dados de exposição Gamma (GEX) para análise pré-abertura da Nasdaq (NQ).

## 1. Visão Geral

O sistema será construído em um repositório GitHub e utilizará GitHub Actions para automação. O fluxo de trabalho principal consiste em:

1.  **Coleta de Dados**: Um script Python busca dados brutos de uma API de mercado.
2.  **Processamento de Dados**: Outro script Python processa os dados brutos para calcular os níveis de GEX.
3.  **Armazenamento de Dados**: Os dados brutos e processados são armazenados no repositório.
4.  **Apresentação**: Os resultados são apresentados em um arquivo Markdown, que pode ser a página principal do repositório (README.md).

## 2. Componentes do Sistema

O sistema será composto pelos seguintes componentes:

| Componente | Tecnologia | Responsabilidade |
|---|---|---|
| **Fonte de Dados** | API Externa (Alpha Vantage para protótipo) | Fornecer dados da cadeia de opções, incluindo gregas e open interest. |
| **Coletor de Dados** | Script Python (`collect_data.py`) | Fazer requisições à API e salvar os dados brutos em formato JSON. |
| **Processador de Dados** | Script Python (`process_data.py`) | Carregar os dados brutos, calcular GEX, identificar níveis chave (Call/Put Wall, Gamma Flip) e salvar os dados processados. |
| **Orquestrador** | GitHub Actions (`.github/workflows/daily_analysis.yml`) | Executar os scripts de coleta e processamento em um horário agendado e fazer o commit dos novos dados. |
| **Visualizador** | Arquivo Markdown (`README.md` ou `ANALYSIS.md`) | Exibir os dados processados de forma clara e concisa, utilizando tabelas e, potencialmente, gráficos. |

## 3. Fluxo de Dados

O fluxo de dados seguirá os seguintes passos:

1.  **Agendamento**: O GitHub Actions é acionado diariamente em um horário pré-definido (ex: 08:00 UTC).
2.  **Execução do Coletor**: O script `collect_data.py` é executado, buscando os dados da API para o ticker relevante (ex: QQQ).
3.  **Armazenamento Bruto**: A resposta da API é salva em um arquivo, por exemplo: `data/raw/YYYY-MM-DD_QQQ.json`.
4.  **Execução do Processador**: O script `process_data.py` é executado, carregando o arquivo de dados brutos recém-criado.
5.  **Cálculos**: O script calcula o GEX por strike, GEX total, Call Wall, Put Wall e o nível de Gamma Flip.
6.  **Armazenamento Processado**: Os resultados são salvos em um arquivo estruturado, por exemplo: `data/processed/YYYY-MM-DD_QQQ.json`.
7.  **Atualização da Apresentação**: Um script final atualiza o arquivo `README.md` com os dados do dia.
8.  **Commit**: O GitHub Actions faz o commit dos novos arquivos de dados e do `README.md` atualizado para o repositório.

## 4. Estrutura de Diretórios

O repositório terá a seguinte estrutura:

```
.github/
  workflows/
    daily_analysis.yml
data/
  raw/
    .gitkeep
  processed/
    .gitkeep
src/
  collect_data.py
  process_data.py
  update_readme.py
.gitignore
ARCHITECTURE.md
README.md
requirements.txt
```

## 5. Tecnologias e Bibliotecas

- **Linguagem**: Python 3.11
- **Bibliotecas Python**:
  - `requests`: Para requisições HTTP à API de dados.
  - `pandas`: Para manipulação e análise eficiente dos dados da cadeia de opções.
  - `matplotlib` ou `plotly`: Para a geração de gráficos da exposição Gamma (opcional, mas recomendado).
- **Automação**: GitHub Actions.

Este design modular permite a fácil substituição da fonte de dados (de Alpha Vantage para uma API paga no futuro) e a expansão da análise com o mínimo de alterações na estrutura central do sistema.

