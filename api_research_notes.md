# Pesquisa de APIs para Sistema de Análise de GEX

## 1. Polygon.io - Options API

### Visão Geral
- **Cobertura**: Todas as 17 exchanges de opções dos EUA (incluindo CBOE, NASDAQ, NYSE)
- **Fonte de Dados**: Conexão direta com OPRA (Options Price Reporting Authority)
- **Volume**: ~3 TB de dados de opções processados diariamente

### Endpoints Relevantes

#### Option Chain Snapshot
- **URL**: `GET /v3/snapshot/options/{underlyingAsset}`
- **Descrição**: Retorna snapshot completo de todos os contratos de opções para um ticker subjacente
- **Dados Incluídos**:
  - **Gregas**: Delta, Gamma, Theta, Vega
  - **Volatilidade Implícita**
  - **Open Interest**
  - **Preço de Break-even**
  - **Últimas cotações e trades**
  - **Dados do ativo subjacente**

#### Parâmetros de Filtro
- `strike_price`: Filtrar por preço de strike
- `expiration_date`: Filtrar por data de expiração (formato YYYY-MM-DD)
- `contract_type`: Filtrar por tipo (call/put)
- `order`: Ordenação (asc/desc)
- `limit`: Limite de resultados (max 250)
- `sort`: Campo de ordenação

### Planos e Acesso
- **Plano Gratuito**: Dados atrasados em 15 minutos
- **Planos Pagos**: Dados em tempo real
- **Planos Business**: Incluem FMV (Fair Market Value) proprietário

### Dados Retornados (Exemplo)
```json
{
  "details": {
    "contract_type": "call",
    "strike_price": 150,
    "expiration_date": "2022-01-21"
  },
  "greeks": {
    "delta": 1,
    "gamma": 0,
    "theta": 0.00229,
    "vega": 0
  },
  "implied_volatility": 5,
  "open_interest": 1543,
  "underlying_asset": {
    "price": 147,
    "ticker": "AAPL"
  }
}
```

### Limitações Identificadas
- **Cálculo de GEX**: A API fornece as gregas individuais, mas NÃO calcula a exposição Gamma agregada dos market makers
- **Necessidade**: Precisaremos calcular o GEX manualmente a partir dos dados brutos
- **Fórmula GEX**: GEX = Open Interest × Gamma × 100 (multiplicador) × ±1 (positivo para calls, negativo para puts)

### Horário de Mercado
- **Regular Market Hours**: Segunda a Sexta, 9:30 AM - 4:00 PM ET
- **Timestamps**: Unix timestamps em UTC (necessário converter para ET)

---

## Próximos Passos de Pesquisa

1. **Investigar APIs alternativas**:
   - Tradier API (mencionada como tendo dados de gregas via ORATS)
   - CBOE DataShop
   - APIs gratuitas ou de menor custo

2. **Verificar dados de fluxo de ordens**:
   - Polygon.io também tem dados de trades/quotes
   - Investigar se há APIs específicas para order flow

3. **Avaliar viabilidade de cálculo próprio**:
   - Confirmar se é possível calcular GEX com precisão a partir dos dados da API
   - Identificar quais dados adicionais são necessários (ex: posição dos market makers)


---

## 2. Tradier API - Options Market Data

### Visão Geral
- **Parceria**: Dados de gregas fornecidos via ORATS (Options Research & Technology Services)
- **Acesso**: Disponível para titulares de conta Tradier Brokerage
- **Tipo**: API de corretora com dados de mercado integrados

### Endpoint Principal

#### Get Options Chains
- **URL**: `GET /v1/markets/options/chains`
- **Descrição**: Retorna cadeia de opções para um símbolo subjacente e data de expiração específicos

#### Parâmetros Obrigatórios
- `symbol`: Símbolo do ativo subjacente (ex: AAPL)
- `expiration`: Data de expiração no formato YYYY-MM-DD (ex: 2021-04-16)

#### Parâmetros Opcionais
- `greeks`: boolean (padrão: false) - Quando true, inclui cálculos de gregas

### Dados de Gregas Disponíveis

Quando `greeks=true`, o objeto `greeks` inclui:

| Grega | Tipo | Descrição |
|-------|------|-----------|
| **delta** | float | Sensibilidade do preço da opção à variação do ativo subjacente |
| **gamma** | float | Taxa de mudança do delta |
| **theta** | float | Decaimento temporal da opção |
| **vega** | float | Sensibilidade à volatilidade implícita |
| **rho** | float | Sensibilidade à taxa de juros |
| **phi** | float | Sensibilidade ao dividendo |
| **bid_iv** | float | Volatilidade implícita no bid |
| **mid_iv** | float | Volatilidade implícita no mid |
| **ask_iv** | float | Volatilidade implícita no ask |

### Outros Dados Retornados
- Preços (last, bid, ask, open, high, low, close)
- Volume e open interest
- Strike price e tipo de contrato
- Datas de expiração
- Underlying symbol

### Vantagens
- **Gregas calculadas**: Não precisa calcular manualmente (fornecidas pela ORATS)
- **Dados completos**: Inclui preços, volume, open interest
- **Integração**: API de corretora permite trading além de dados

### Limitações Identificadas
- **Requisito de Conta**: Necessário ter conta na Tradier Brokerage
- **Dados em Tempo Real**: Disponível apenas para titulares de conta
- **Custo**: Precisa verificar se há custos adicionais para acesso à API
- **Sem GEX Agregado**: Assim como Polygon, fornece gregas individuais mas não o GEX total do mercado

### Observação Importante
A documentação menciona: "Greek and IV data is included courtesy of ORATS. Please check out their APIs for more in-depth options data."

Isso sugere que para análises mais profundas (como GEX agregado), seria necessário acessar diretamente a API da ORATS.

---

## 3. ORATS (Options Research & Technology Services)

### Nota de Investigação
- **Fonte Original**: ORATS é o provedor dos dados de gregas para Tradier
- **Próximo Passo**: Investigar se ORATS oferece:
  - API pública com dados de exposição Gamma agregada
  - Cálculos de GEX por strike
  - Níveis de Call Wall / Put Wall / Gamma Flip
  - Preços e planos de acesso



### ORATS API - Preços (Individual)

| Plano | Preço | Descrição | Limites |
|-------|-------|-----------|---------|
| **Delayed Data API** | $99/mês | Perfeito para começar | 20.000 requisições/mês |
| **Live Data API** | $199/mês | Melhor para traders ativos | 100.000 requisições/mês |
| **Live Intraday API** | $399/mês | Acesso a todos os endpoints ORATS | 1.000.000 requisições/mês |

### Dados Incluídos (Delayed Data API - $99/mês)
- ✅ Tickers
- ✅ Strikes + Near EOD History
- ✅ Strikes by OPRA + Near EOD History
- ✅ Monies Implied + Near EOD History
- ✅ Monies Forecast + Near EOD History
- ✅ SMV Summaries + Near EOD History
- ✅ Core Data + Near EOD History
- ✅ Daily Price
- ✅ Historical Volatility
- ✅ Dividend History
- ✅ Earnings History

### Observação Crítica
Após análise da documentação ORATS, **NÃO foi identificado nenhum endpoint específico para cálculo de GEX (Gamma Exposure) agregado** ou níveis de Call Wall/Put Wall/Gamma Flip.

A ORATS fornece:
- ✅ Gregas individuais por contrato (delta, gamma, theta, vega, rho)
- ✅ Open Interest por strike
- ✅ Volume por strike
- ❌ **NÃO fornece**: GEX agregado calculado

**Conclusão**: Mesmo com ORATS, precisaremos calcular o GEX manualmente.

---

## 4. Alpha Vantage - Options Data API

### Visão Geral
- **Cobertura**: Dados de opções dos EUA
- **Histórico**: 15+ anos de dados históricos
- **Plano Gratuito**: Disponível com limitações

### Endpoints Disponíveis

#### 1. Realtime Options (Premium)
- **Função**: `REALTIME_OPTIONS`
- **Tipo**: Dados em tempo real
- **Status**: **Premium** (pago)

#### 2. Historical Options (Trending - Popular)
- **Função**: `HISTORICAL_OPTIONS`
- **Tipo**: Dados históricos completos
- **Status**: Disponível no plano gratuito com limitações

### Dados Retornados (Historical Options)

A API retorna a cadeia completa de opções para um símbolo específico em uma data específica, incluindo:

- **Volatilidade Implícita (IV)**
- **Gregas Comuns**: delta, gamma, theta, vega, rho
- **Preços**: bid, ask, last
- **Volume e Open Interest**
- **Strike prices**
- **Datas de expiração**

### Parâmetros da API

| Parâmetro | Tipo | Obrigatório | Descrição |
|-----------|------|-------------|-----------|
| `function` | string | Sim | `HISTORICAL_OPTIONS` |
| `symbol` | string | Sim | Símbolo do ativo (ex: IBM) |
| `date` | date | Opcional | Data específica (YYYY-MM-DD). Se não fornecida, retorna sessão anterior |
| `datatype` | string | Opcional | `json` ou `csv` (padrão: json) |
| `apikey` | string | Sim | Chave da API (gratuita disponível) |

### Exemplo de Chamada
```
https://www.alphavantage.co/query?function=HISTORICAL_OPTIONS&symbol=IBM&date=2017-11-15&apikey=YOUR_API_KEY
```

### Vantagens
- ✅ **Plano Gratuito Disponível**: Não requer pagamento inicial
- ✅ **Gregas Incluídas**: Delta, gamma, theta, vega, rho já calculados
- ✅ **Dados Históricos**: 15+ anos de histórico
- ✅ **Fácil de Usar**: API REST simples

### Limitações
- ⚠️ **Rate Limits no Plano Gratuito**: Limitação de requisições por minuto/dia
- ⚠️ **Dados Históricos**: Não é tempo real no plano gratuito
- ⚠️ **Sem GEX Agregado**: Fornece gregas individuais, não exposição agregada
- ⚠️ **Precisa de Data Específica**: Requer especificar a data para cada consulta

### Plano Gratuito
- **Custo**: $0
- **Limitações**: 
  - 25 requisições por dia (API calls)
  - Dados atrasados (não tempo real para opções)
- **Suficiente para**: Desenvolvimento, testes, análises históricas

---

## CONCLUSÕES DA PESQUISA DE APIs

### Situação Atual do Mercado

Após extensa pesquisa nas principais APIs de dados de opções do mercado americano, chegamos a uma conclusão importante: **nenhuma API pública fornece diretamente os cálculos de GEX (Gamma Exposure) agregado, Call Wall, Put Wall ou Gamma Flip**.

### O Que as APIs Fornecem

Todas as APIs pesquisadas (Polygon.io, Tradier, ORATS, Alpha Vantage) fornecem os **dados brutos necessários**:

1. **Gregas individuais por contrato** (delta, gamma, theta, vega)
2. **Open Interest por strike**
3. **Volume por strike**
4. **Preços e volatilidade implícita**

### O Que Precisamos Calcular

Para replicar a análise de plataformas como SpotGamma, precisaremos calcular:

1. **GEX por Strike**: `GEX = Open Interest × Gamma × 100 × ±1`
   - Positivo para CALLs (market makers short calls)
   - Negativo para PUTs (market makers short puts)

2. **GEX Total**: Soma de todos os strikes

3. **Call Wall**: Strike com maior concentração de Gamma de CALLs

4. **Put Wall**: Strike com maior concentração de Gamma de PUTs

5. **Gamma Flip / Volatility Trigger**: Nível onde GEX muda de positivo para negativo

### Recomendação de API para o Sistema

Com base na análise custo-benefício:

| Critério | Recomendação | Justificativa |
|----------|--------------|---------------|
| **Para Desenvolvimento/Testes** | **Alpha Vantage (Gratuito)** | Plano gratuito com gregas incluídas, suficiente para prototipar |
| **Para Produção (Dados Atrasados)** | **Polygon.io Starter** ou **ORATS Delayed ($99/mês)** | Dados confiáveis, limites adequados |
| **Para Produção (Tempo Real)** | **Polygon.io Options Plan** ou **ORATS Live ($199/mês)** | Dados em tempo real para análise pré-mercado |

### Estratégia de Implementação

**Fase 1 - Prototipagem (Gratuita)**
- Usar Alpha Vantage para desenvolver e testar os algoritmos de cálculo de GEX
- Validar os cálculos com dados históricos
- Construir o pipeline de processamento

**Fase 2 - Produção (Paga)**
- Migrar para Polygon.io ou ORATS para dados mais confiáveis
- Implementar cache para otimizar uso de API calls
- Automatizar coleta diária via GitHub Actions

**Fase 3 - Otimização**
- Considerar armazenar dados históricos localmente
- Reduzir dependência de APIs para análises retrospectivas
- Implementar fallback entre múltiplas APIs

---

## PRÓXIMAS AÇÕES

1. ✅ **Pesquisa de APIs concluída**
2. ⏭️ **Projetar arquitetura do sistema**
3. ⏭️ **Desenvolver algoritmos de cálculo de GEX**
4. ⏭️ **Implementar coleta de dados via API**
5. ⏭️ **Configurar automação no GitHub Actions**
6. ⏭️ **Criar dashboard de visualização**
