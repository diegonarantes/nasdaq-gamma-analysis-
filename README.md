# Sistema de Análise de Exposição Gamma (GEX)

## 🚀 Sistema Automatizado de Análise Pré-Mercado para Nasdaq

Este repositório contém um sistema automatizado que coleta, processa e apresenta diariamente dados de exposição Gamma (GEX) para análise institucional antes da abertura do mercado americano.

---

## 📊 Status

⏳ **Aguardando primeira execução automática...**

O sistema está configurado para executar automaticamente todos os dias úteis às 13:00 UTC (antes da abertura do mercado às 9:30 AM ET).

---

## ⚙️ Configuração Inicial

Para ativar o sistema, você precisa configurar sua chave de API:

### 1. Obtenha uma Chave de API Gratuita

Acesse [Alpha Vantage](https://www.alphavantage.co/support/#api-key) e obtenha sua chave gratuita.

### 2. Configure o Secret no GitHub

1. Vá para **Settings** > **Secrets and variables** > **Actions**
2. Clique em **New repository secret**
3. Nome: `ALPHA_VANTAGE_API_KEY`
4. Valor: Cole sua chave de API
5. Clique em **Add secret**

### 3. Execute Manualmente (Opcional)

Para testar imediatamente:

1. Vá para a aba **Actions**
2. Selecione **Análise Diária de GEX**
3. Clique em **Run workflow**

---

## 📖 Documentação

- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Arquitetura completa do sistema
- **[api_research_notes.md](api_research_notes.md)** - Pesquisa de APIs e fontes de dados

---

## 🛠️ Tecnologias

- **Python 3.11** - Processamento de dados
- **GitHub Actions** - Automação
- **Alpha Vantage API** - Fonte de dados de opções
- **Matplotlib** - Visualização de dados

---

## 📅 Próxima Atualização

O sistema executará automaticamente na próxima sessão de mercado. Após a primeira execução, esta página será atualizada com a análise completa.

---

## ⚠️ Disclaimer

Este sistema é apenas para fins educacionais e informativos. Não constitui aconselhamento financeiro.
