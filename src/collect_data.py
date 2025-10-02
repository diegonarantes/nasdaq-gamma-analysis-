"""
Script para coletar dados de opções da API Alpha Vantage.
Salva os dados brutos em formato JSON para processamento posterior.
"""

import os
import sys
import json
import requests
from datetime import datetime
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configurações
API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY', 'demo')
BASE_URL = 'https://www.alphavantage.co/query'

def fetch_options_data(symbol, date=None):
    """
    Busca dados de opções da API Alpha Vantage.
    
    Args:
        symbol (str): Símbolo do ativo (ex: 'QQQ' para Nasdaq-100 ETF)
        date (str): Data no formato YYYY-MM-DD (opcional)
    
    Returns:
        dict: Dados brutos da API
    """
    params = {
        'function': 'HISTORICAL_OPTIONS',
        'symbol': symbol,
        'apikey': API_KEY
    }
    
    if date:
        params['date'] = date
    
    print(f"Buscando dados de opções para {symbol}...")
    
    try:
        response = requests.get(BASE_URL, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        # Verificar se há erro na resposta
        if 'Error Message' in data:
            print(f"Erro da API: {data['Error Message']}")
            return None
        
        if 'Note' in data:
            print(f"Aviso da API: {data['Note']}")
            return None
            
        print(f"Dados coletados com sucesso!")
        return data
        
    except requests.exceptions.RequestException as e:
        print(f"Erro ao fazer requisição: {e}")
        return None

def save_raw_data(data, symbol):
    """
    Salva os dados brutos em arquivo JSON.
    
    Args:
        data (dict): Dados da API
        symbol (str): Símbolo do ativo
    """
    if not data:
        print("Nenhum dado para salvar.")
        return False
    
    # Criar diretório se não existir
    os.makedirs('data/raw', exist_ok=True)
    
    # Nome do arquivo com timestamp
    today = datetime.now().strftime('%Y-%m-%d')
    filename = f"data/raw/{today}_{symbol}.json"
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"Dados salvos em: {filename}")
        return True
        
    except Exception as e:
        print(f"Erro ao salvar arquivo: {e}")
        return False

def main():
    """
    Função principal do script.
    """
    # Símbolo padrão: QQQ (ETF que rastreia o Nasdaq-100)
    # Pode ser alterado para SPY (S&P 500) ou outros
    symbol = os.getenv('TARGET_SYMBOL', 'QQQ')
    
    print(f"=== Coletor de Dados de Opções ===")
    print(f"Símbolo: {symbol}")
    print(f"Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Buscar dados
    data = fetch_options_data(symbol)
    
    # Salvar dados
    if data:
        success = save_raw_data(data, symbol)
        if success:
            print("\n✓ Coleta concluída com sucesso!")
            sys.exit(0)
        else:
            print("\n✗ Falha ao salvar dados.")
            sys.exit(1)
    else:
        print("\n✗ Falha ao coletar dados.")
        sys.exit(1)

if __name__ == '__main__':
    main()
