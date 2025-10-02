"""
Script para gerar gráfico de visualização da exposição Gamma (GEX).
"""

import os
import sys
import json
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from datetime import datetime
from pathlib import Path

# Configurar estilo do matplotlib
plt.style.use('seaborn-v0_8-darkgrid')

def load_latest_processed_data(symbol):
    """
    Carrega o arquivo de dados processados mais recente.
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
    
    print(f"Carregando dados de: {latest_file}")
    
    try:
        with open(latest_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except Exception as e:
        print(f"Erro ao carregar arquivo: {e}")
        return None

def generate_gex_chart(data):
    """
    Gera gráfico de barras da exposição Gamma por strike.
    """
    if not data or 'gex_by_strike' not in data:
        print("Dados insuficientes para gerar gráfico.")
        return None
    
    gex_data = data['gex_by_strike']
    levels = data['key_levels']
    symbol = data['symbol']
    date = data['date']
    
    # Preparar dados para o gráfico
    strikes = []
    gex_values = []
    colors = []
    
    for item in gex_data:
        strikes.append(item['strike'])
        gex_values.append(item['gex'])
        # Cor verde para GEX positivo (calls), vermelho para negativo (puts)
        colors.append('#2ecc71' if item['gex'] > 0 else '#e74c3c')
    
    # Criar figura
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # Plotar barras
    bars = ax.bar(strikes, gex_values, color=colors, alpha=0.7, edgecolor='black', linewidth=0.5)
    
    # Adicionar linha zero
    ax.axhline(y=0, color='black', linestyle='-', linewidth=1)
    
    # Marcar níveis chave
    if levels['call_wall']['strike']:
        ax.axvline(x=levels['call_wall']['strike'], color='green', linestyle='--', 
                   linewidth=2, label=f"Call Wall: ${levels['call_wall']['strike']:.2f}")
    
    if levels['put_wall']['strike']:
        ax.axvline(x=levels['put_wall']['strike'], color='red', linestyle='--', 
                   linewidth=2, label=f"Put Wall: ${levels['put_wall']['strike']:.2f}")
    
    if levels['gamma_flip']:
        ax.axvline(x=levels['gamma_flip'], color='orange', linestyle='--', 
                   linewidth=2, label=f"Gamma Flip: ${levels['gamma_flip']:.2f}")
    
    # Configurar labels e título
    ax.set_xlabel('Strike Price ($)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Gamma Exposure (GEX)', fontsize=12, fontweight='bold')
    ax.set_title(f'Exposição Gamma (GEX) - {symbol}\n{date}', 
                 fontsize=16, fontweight='bold', pad=20)
    
    # Adicionar legenda
    ax.legend(loc='upper right', fontsize=10)
    
    # Adicionar grid
    ax.grid(True, alpha=0.3)
    
    # Adicionar informação do regime
    regime_text = f"Regime: {levels['market_regime']}\nTotal GEX: {levels['total_gex']:,.0f}"
    ax.text(0.02, 0.98, regime_text, transform=ax.transAxes, 
            fontsize=10, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    # Ajustar layout
    plt.tight_layout()
    
    return fig

def save_chart(fig, symbol):
    """
    Salva o gráfico como imagem.
    """
    if not fig:
        print("Nenhum gráfico para salvar.")
        return False
    
    # Criar diretório se não existir
    os.makedirs('charts', exist_ok=True)
    
    today = datetime.now().strftime('%Y-%m-%d')
    filename = f"charts/{today}_{symbol}_gex.png"
    
    try:
        fig.savefig(filename, dpi=150, bbox_inches='tight')
        print(f"Gráfico salvo em: {filename}")
        
        # Também salvar como latest para fácil acesso
        latest_filename = f"charts/latest_{symbol}_gex.png"
        fig.savefig(latest_filename, dpi=150, bbox_inches='tight')
        print(f"Gráfico também salvo em: {latest_filename}")
        
        return True
    except Exception as e:
        print(f"Erro ao salvar gráfico: {e}")
        return False
    finally:
        plt.close(fig)

def main():
    """
    Função principal do script.
    """
    symbol = os.getenv('TARGET_SYMBOL', 'QQQ')
    
    print(f"=== Gerador de Gráficos GEX ===")
    print(f"Símbolo: {symbol}")
    print(f"Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Carregar dados processados
    data = load_latest_processed_data(symbol)
    if not data:
        print("\n✗ Falha ao carregar dados processados.")
        sys.exit(1)
    
    # Gerar gráfico
    print("Gerando gráfico...")
    fig = generate_gex_chart(data)
    
    # Salvar gráfico
    if fig:
        success = save_chart(fig, symbol)
        if success:
            print("\n✓ Gráfico gerado com sucesso!")
            sys.exit(0)
        else:
            print("\n✗ Falha ao salvar gráfico.")
            sys.exit(1)
    else:
        print("\n✗ Falha ao gerar gráfico.")
        sys.exit(1)

if __name__ == '__main__':
    main()
