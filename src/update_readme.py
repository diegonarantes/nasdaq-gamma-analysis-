"""
Script para atualizar o README.md com os resultados da análise diária.
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path

def load_latest_processed_data(symbol):
    """
    Carrega o arquivo de dados processados mais recente.
    
    Args:
        symbol (str): Símbolo do ativo
    
    Returns:
        dict: Dados processados
    """
    processed_dir = Path('data/processed')
    
    if not processed_dir.exists():
        print("Diretório de dados processados não encontrado.")
        return None
    
    files = list(processed_dir.glob(f"*_{symbol}.json"))
    
    if not files:
        print(f"Nenhum arquivo processado encontrado para {symbol}.")
        return None
    
    latest_file = max(files, key=lambda p: p.stat().st_mtime)
    
    print(f"Carregando dados processados de: {latest_file}")
    
    try:
        with open(latest_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except Exception as e:
        print(f"Erro ao carregar arquivo: {e}")
        return None

def generate_readme_content(data):
    """
    Gera o conteúdo do README.md com base nos dados processados.
    
    Args:
        data (dict): Dados processados
    
    Returns:
        str: Conteúdo do README em Markdown
    """
    if not data:
        return None
    
    symbol = data['symbol']
    date = data['date']
    levels = data['key_levels']
    
    # Determinar viés de mercado
    regime = levels['market_regime']
    regime_emoji = "🟢" if regime == "Positive Gamma" else "🔴"
    
    # Interpretação do regime
    if regime == "Positive Gamma":
        interpretation = """
**Interpretação**: O mercado está em regime de **Gamma Positivo**. Neste cenário, os market makers 
tendem a negociar **contra a tendência** (compram em quedas, vendem em altas) para se proteger. 
Isso **suprime a volatilidade** e cria um efeito de "imã" nos preços, mantendo o mercado em um range.

**Estratégia Sugerida**: Buscar operações de reversão nos níveis de Call Wall (resistência) e Put Wall (suporte).
"""
    else:
        interpretation = """
**Interpretação**: O mercado está em regime de **Gamma Negativo**. Neste cenário, os market makers 
tendem a negociar **a favor da tendência** (compram em altas, vendem em quedas) para se proteger. 
Isso **amplifica a volatilidade** e acelera os movimentos, podendo levar a "gamma squeezes".

**Estratégia Sugerida**: Operar a favor do rompimento. Se o preço romper o Gamma Flip, espera-se movimento acelerado.
"""
    
    content = f"""# Análise de Exposição Gamma (GEX) - {symbol}

## 📊 Última Atualização: {date}

---

## 🎯 Níveis Chave Identificados

| Nível | Valor | Descrição |
|-------|-------|-----------|
| **Call Wall** 📈 | ${levels['call_wall']['strike']:.2f} | Resistência forte - Maior concentração de Gamma de CALLs |
| **Put Wall** 📉 | ${levels['put_wall']['strike']:.2f} | Suporte forte - Maior concentração de Gamma de PUTs |
| **Gamma Flip** ⚡ | ${levels['gamma_flip']:.2f} | Ponto de mudança de regime de volatilidade |

---

## {regime_emoji} Regime de Mercado

**Status Atual**: {regime}

**Total GEX**: {levels['total_gex']:,.0f}

{interpretation}

---

## 📈 Visualização da Exposição Gamma

![GEX Chart](charts/latest_{symbol}_gex.png)

*Gráfico atualizado automaticamente. Barras verdes representam CALLs (GEX positivo), barras vermelhas representam PUTs (GEX negativo).*

---

## 📖 Como Usar Esta Análise

### Antes da Abertura do Mercado (9:30 AM ET)

1. **Verifique o Regime de Mercado** (Gamma Positivo ou Negativo)
2. **Identifique os Níveis Chave** (Call Wall, Put Wall, Gamma Flip)
3. **Observe o Preço Pré-Mercado** em relação aos níveis

### Durante os Primeiros 90 Minutos

#### Se o mercado está em **Gamma Positivo**:
- Espere reversões nos níveis de Call Wall e Put Wall
- O preço tende a ser "puxado" de volta para dentro do range
- Volatilidade suprimida

#### Se o mercado está em **Gamma Negativo**:
- Espere movimentos direcionais acelerados
- Rompimentos tendem a continuar
- Volatilidade amplificada

---

## 🔧 Sobre Este Sistema

Este sistema automatizado coleta dados de opções diariamente e calcula a exposição Gamma (GEX) 
dos market makers para identificar zonas de alta probabilidade de suporte, resistência e mudança 
de regime de volatilidade.

**Fonte de Dados**: Alpha Vantage API  
**Atualização**: Diária, via GitHub Actions  
**Cálculo**: GEX = Open Interest × Gamma × 100 × ±1

---

## ⚠️ Disclaimer

Esta análise é apenas para fins educacionais e informativos. Não constitui aconselhamento financeiro. 
Sempre faça sua própria pesquisa e consulte um profissional qualificado antes de tomar decisões de investimento.

---

*Última atualização automática: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC*
"""
    
    return content

def update_readme(content):
    """
    Atualiza o arquivo README.md com o novo conteúdo.
    
    Args:
        content (str): Novo conteúdo do README
    
    Returns:
        bool: True se bem-sucedido, False caso contrário
    """
    if not content:
        print("Nenhum conteúdo para atualizar.")
        return False
    
    try:
        with open('README.md', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("README.md atualizado com sucesso!")
        return True
    except Exception as e:
        print(f"Erro ao atualizar README: {e}")
        return False

def main():
    """
    Função principal do script.
    """
    symbol = os.getenv('TARGET_SYMBOL', 'QQQ')
    
    print(f"=== Atualizador de README ===")
    print(f"Símbolo: {symbol}")
    print(f"Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Carregar dados processados
    data = load_latest_processed_data(symbol)
    if not data:
        print("\n✗ Falha ao carregar dados processados.")
        sys.exit(1)
    
    # Gerar conteúdo do README
    content = generate_readme_content(data)
    
    # Atualizar README
    success = update_readme(content)
    
    if success:
        print("\n✓ README atualizado com sucesso!")
        sys.exit(0)
    else:
        print("\n✗ Falha ao atualizar README.")
        sys.exit(1)

if __name__ == '__main__':
    main()
