# Trading View é o site que a B3 usa

import requests
import json
import pandas as pd
from time import sleep


def criar_df_cotacao_tvb3(df_mov_financeiras):

    # Obtendo os valores únicos da coluna 'ATIVO' e convertendo em uma lista
    lista_tickers = df_mov_financeiras['Ativo'].unique().tolist()

    url = "https://scanner.tradingview.com/brazil/scan"

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Content-Type": "application/json",
        "Referer": "https://br.tradingview.com/"
    }

    # Lista para armazenar os dados de todos os tickers
    dados = []

    for ticker in lista_tickers:
        payload = {
            "symbols": {
                "tickers": [f"BMFBOVESPA:{ticker}"],  # Pode colocar BBAS3, PETR4, etc
                "query": {"types": []}
            },
            "columns": ["close", "name"]  # Aqui consigo pegar mais dados, preenchendo o nome dele aqui conforme doc API
        }

        response = requests.post(url, headers=headers, data=json.dumps(payload))
        data = response.json()

        try:
            # Atribuindo os dados pegos a variáveis
            resultados = data['data'][0]['d']
            preco_atual = resultados[0]
            # nome = resultados[1]  # Se quiser usar depois
        except (IndexError, KeyError, TypeError):
            # Se não encontrar o ativo ou algo der errado, preenche com None
            preco_atual = None
            # nome = None

        # Adicionando à lista de dados para o DataFrame
        dados.append({
            "Ticker": ticker,
            "Preço": preco_atual
            # "Nome": nome  # Caso queira incluir, é só descomentar
        })

        sleep(0.5) # Talvez usar 1.0 ****

    # # Criando o DataFrame final
    # df_cotacao_tradview = pd.DataFrame(dados)

    return pd.DataFrame(dados)

