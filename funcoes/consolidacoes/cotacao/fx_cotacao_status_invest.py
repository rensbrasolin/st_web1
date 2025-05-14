# # lista_manual_tickers = ['BBAS3', 'TAEE11', 'BRBI11', 'CSMG3', 'PETR4', 'VALE3', 'BBSE3', 'ISAE4', 'HASH11', 'IVVB11',
# #                         'MXRF11', 'HGLG11', 'MXRF11', 'BTLG11', 'GARE11', 'GGRC11', 'RECR11', 'CPTS11', 'HSLG11',
# #                         'XPLG11', 'XPML11', 'GTWR11', 'TAEE3', 'SAPR4', 'ITSA4']
#
# # -------------------------------------------------------------------------------------------------------------------
# Cada tipo de ativo tem uma url diferente
# Funciona no ambiente local, mas dá erro na nuvem
# -------------------------------------------------------------------------------------------------------------------
import requests
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep


def criar_df_cotacao_statusinvest(df_mov_financeiras):

    # Obtendo os valores únicos da coluna 'ATIVO' e convertendo em uma lista de tuplas (ticker, tipo)
    lista_tickers = df_mov_financeiras[['Ativo', 'Tipo de Ativo']].drop_duplicates().values.tolist()

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Referer": "https://statusinvest.com.br"
    }

    dados = []

    for ticker, tipo in lista_tickers:

        # Definindo a URL com base no tipo de ativo
        if tipo == 'Ação':
            url = f"https://statusinvest.com.br/acoes/{ticker.lower()}"
        elif tipo == 'FII':
            url = f"https://statusinvest.com.br/fundos-imobiliarios/{ticker.lower()}"
        elif tipo == 'ETF':
            url = f"https://statusinvest.com.br/etfs/{ticker.lower()}"
        else:
            url = None  # Tipo indefinido, pode ser tratado conforme necessário

        valor = None

        if url:
            try:
                response = requests.get(url, headers=headers, timeout=10)
                response.raise_for_status()

                soup = BeautifulSoup(response.text, "html.parser")

                # Procurar o primeiro elemento com classe que contém a cotação
                cotacao_elemento = soup.find("strong", {"class": "value"})

                if cotacao_elemento:
                    texto = cotacao_elemento.get_text(strip=True)
                    valor = float(texto.replace("R$", "").replace(".", "").replace(",", "."))

            except Exception as e:
                print(f"Tentativa falhou para {ticker} na URL: {url} | Erro: {e}")

        # Adicionando à lista de dados para o DataFrame
        dados.append({
            "Ticker": ticker,
            "Preço": valor
        })

        sleep(1)  # pausa para evitar bloqueio

    return pd.DataFrame(dados)
