"""
Script para processar dados de opções e calcular exposição Gamma (GEX).
Identifica níveis chave: Call Wall, Put Wall e Gamma Flip.
"""

import os
import sys
import json
import pandas as pd
from datetime import datetime
from pathlib import Path

def load_latest_raw_data(symbol):
    """
    Carrega o arquivo de dados brutos mais recente para o símbolo especificado.
    
    Args:
        symbol (str): Símbolo do ativo
    
    Returns:
        dict: Dados brutos carregados
    """
    raw_dir = Path('data/raw')
    
    if not raw_dir.exists():
        print("Diretório de dados brutos não encontrado.")
        return None
    
    # Buscar arquivos do símbolo
    files = list(raw_dir.glob(f"*_{symbol}.json"))
    
    if not files:
        print(f"Nenhum arquivo encontrado para {symbol}.")
        return None
    
    # Pegar o mais recente
    latest_file = max(files, key=lambda p: p.stat().st_mtime)
    
    print(f"Carregando dados de: {latest_file}")
    
    try:
        with open(latest_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except Exception as e:
        print(f"Erro ao carregar arquivo: {e}")
        return None

def parse_options_data(raw_data):
    """
    Converte os dados brutos da API em um DataFrame pandas.
    
    Args:
        raw_data (dict): Dados brutos da API
    
    Returns:
        pd.DataFrame: DataFrame com os dados de opções
    """
    if not raw_data or 'data' not in raw_data:
        print("Formato de dados inválido.")
        return None
    
    options_list = raw_data['data']
    
    if not options_list:
        print("Nenhum dado de opções encontrado.")
        return None
    
    df = pd.DataFrame(options_list)
    
    # Converter tipos de dados
    numeric_columns = ['strike', 'bid', 'ask', 'last', 'volume', 'open_interest',
                      'delta', 'gamma', 'theta', 'vega', 'rho', 'implied_volatility']
    
    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    print(f"Dados parseados: {len(df)} contratos de opções")
    return df

def calculate_gex(df):
    """
    Calcula a exposição Gamma (GEX) para cada strike.
    
    Fórmula: GEX = Open Interest × Gamma × 100 × ±1
    - Positivo para CALLs (market makers vendem calls, ficam short gamma)
    - Negativo para PUTs (market makers vendem puts, ficam short gamma)
    
    Args:
        df (pd.DataFrame): DataFrame com dados de opções
    
    Returns:
        pd.DataFrame: DataFrame com GEX calculado
    """
    if df is None or df.empty:
        return None
    
    # Filtrar apenas contratos com dados válidos
    df_clean = df[df['gamma'].notna() & df['open_interest'].notna()].copy()
    
    # Calcular GEX
    # Para CALLs: GEX positivo (MMs vendem calls, compram ativo para hedge)
    # Para PUTs: GEX negativo (MMs vendem puts, vendem ativo para hedge)
    df_clean['gex'] = df_clean.apply(
        lambda row: row['open_interest'] * row['gamma'] * 100 * (1 if row['type'] == 'call' else -1),
        axis=1
    )
    
    # Agrupar por strike e tipo
    gex_by_strike = df_clean.groupby(['strike', 'type']).agg({
        'gex': 'sum',
        'open_interest': 'sum',
        'gamma': 'mean',
        'volume': 'sum'
    }).reset_index()
    
    return gex_by_strike

def identify_key_levels(gex_df):
    """
    Identifica níveis chave: Call Wall, Put Wall e Gamma Flip.
    
    Args:
        gex_df (pd.DataFrame): DataFrame com GEX por strike
    
    Returns:
        dict: Dicionário com os níveis identificados
    """
    if gex_df is None or gex_df.empty:
        return None
    
    # Separar calls e puts
    calls = gex_df[gex_df['type'] == 'call']
    puts = gex_df[gex_df['type'] == 'put']
    
    # Call Wall: Strike com maior GEX positivo (maior concentração de calls)
    call_wall = calls.loc[calls['gex'].idxmax()] if not calls.empty else None
    
    # Put Wall: Strike com maior GEX negativo (maior concentração de puts)
    put_wall = puts.loc[puts['gex'].abs().idxmax()] if not puts.empty else None
    
    # GEX Total por strike (soma de calls e puts)
    total_gex_by_strike = gex_df.groupby('strike')['gex'].sum().reset_index()
    total_gex_by_strike = total_gex_by_strike.sort_values('strike')
    
    # Gamma Flip: Ponto onde GEX muda de positivo para negativo
    gamma_flip = None
    for i in range(len(total_gex_by_strike) - 1):
        current_gex = total_gex_by_strike.iloc[i]['gex']
        next_gex = total_gex_by_strike.iloc[i + 1]['gex']
        
        if current_gex > 0 and next_gex < 0:
            gamma_flip = total_gex_by_strike.iloc[i]['strike']
            break
        elif current_gex < 0 and next_gex > 0:
            gamma_flip = total_gex_by_strike.iloc[i + 1]['strike']
            break
    
    # GEX Total
    total_gex = gex_df['gex'].sum()
    
    levels = {
        'call_wall': {
            'strike': float(call_wall['strike']) if call_wall is not None else None,
            'gex': float(call_wall['gex']) if call_wall is not None else None
        },
        'put_wall': {
            'strike': float(put_wall['strike']) if put_wall is not None else None,
            'gex': float(put_wall['gex']) if put_wall is not None else None
        },
        'gamma_flip': float(gamma_flip) if gamma_flip is not None else None,
        'total_gex': float(total_gex),
        'market_regime': 'Positive Gamma' if total_gex > 0 else 'Negative Gamma'
    }
    
    return levels

def save_processed_data(gex_df, levels, symbol):
    """
    Salva os dados processados em arquivo JSON.
    
    Args:
        gex_df (pd.DataFrame): DataFrame com GEX calculado
        levels (dict): Níveis chave identificados
        symbol (str): Símbolo do ativo
    """
    os.makedirs('data/processed', exist_ok=True)
    
    today = datetime.now().strftime('%Y-%m-%d')
    filename = f"data/processed/{today}_{symbol}.json"
    
    # Preparar dados para salvar
    output = {
        'date': today,
        'symbol': symbol,
        'timestamp': datetime.now().isoformat(),
        'key_levels': levels,
        'gex_by_strike': gex_df.to_dict('records') if gex_df is not None else []
    }
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        
        print(f"\nDados processados salvos em: {filename}")
        return True
    except Exception as e:
        print(f"Erro ao salvar dados processados: {e}")
        return False

def main():
    """
    Função principal do script.
    """
    symbol = os.getenv('TARGET_SYMBOL', 'QQQ')
    
    print(f"=== Processador de Dados de Opções ===")
    print(f"Símbolo: {symbol}")
    print(f"Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 1. Carregar dados brutos
    raw_data = load_latest_raw_data(symbol)
    if not raw_data:
        print("\n✗ Falha ao carregar dados brutos.")
        sys.exit(1)
    
    # 2. Parsear dados
    df = parse_options_data(raw_data)
    if df is None:
        print("\n✗ Falha ao parsear dados.")
        sys.exit(1)
    
    # 3. Calcular GEX
    print("\nCalculando exposição Gamma...")
    gex_df = calculate_gex(df)
    
    # 4. Identificar níveis chave
    print("Identificando níveis chave...")
    levels = identify_key_levels(gex_df)
    
    if levels:
        print("\n=== NÍVEIS IDENTIFICADOS ===")
        print(f"Call Wall: ${levels['call_wall']['strike']:.2f}" if levels['call_wall']['strike'] else "Call Wall: N/A")
        print(f"Put Wall: ${levels['put_wall']['strike']:.2f}" if levels['put_wall']['strike'] else "Put Wall: N/A")
        print(f"Gamma Flip: ${levels['gamma_flip']:.2f}" if levels['gamma_flip'] else "Gamma Flip: N/A")
        print(f"Total GEX: {levels['total_gex']:,.0f}")
        print(f"Regime de Mercado: {levels['market_regime']}")
    
    # 5. Salvar dados processados
    success = save_processed_data(gex_df, levels, symbol)
    
    if success:
        print("\n✓ Processamento concluído com sucesso!")
        sys.exit(0)
    else:
        print("\n✗ Falha ao salvar dados processados.")
        sys.exit(1)

if __name__ == '__main__':
    main()
